#!/usr/bin/env python3
"""Make web versions of the photos in images.json and upload any that R2 does not have yet.

Each photo gets 1600 px and 800 px versions, in WebP and JPG, with EXIF removed. They are stored as
tangthu/img/<key>-<width>.<ext> in the bucket behind https://assets.khual.net.

    python3 scripts/upload_images.py --dry-run   show the plan, change nothing in R2
    python3 scripts/upload_images.py             generate what is missing and upload it

Rules: nothing is deleted. An existing key with the same content is skipped. An existing key
with different content stops the run: pick a new filename instead. If any key is in conflict,
nothing is uploaded at all. Credentials come from .env or the environment:
R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET.
"""
import argparse, hashlib, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = json.loads((ROOT / "images.json").read_text())
WEB_DIR = ROOT / "images" / "web"          # generated locally, git-ignored
WIDTHS = (1600, 800)
FORMATS = {"webp": ("WEBP", "image/webp"), "jpg": ("JPEG", "image/jpeg")}
PREFIX = "tangthu/img"
CACHE = "public, max-age=31536000, immutable"

def load_env():
    env = dict(os.environ)
    path = ROOT / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip("\"'"))
    return env

def make_versions(key, rec):
    """Create missing web versions. Returns {(width, ext): (path, dims)}; never upscales."""
    from PIL import Image, ImageOps
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    src = ROOT / rec["file"]
    out = {}
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)  # honour the camera rotation, then drop metadata below
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        for w in WIDTHS:
            target = min(w, im.width)
            h = round(im.height * target / im.width)
            resized = im if target == im.width else im.resize((target, h), Image.LANCZOS)
            for ext, (fmt, _) in FORMATS.items():
                path = WEB_DIR / f"{key}-{w}.{ext}"
                if not path.exists() or path.stat().st_mtime < src.stat().st_mtime:
                    save_kwargs = {"quality": 82, "method": 6} if ext == "webp" else {"quality": 85, "optimize": True, "progressive": True}
                    flat = resized.convert("RGB") if fmt == "JPEG" else resized
                    flat.save(path, fmt, **save_kwargs)  # no exif= argument, so no EXIF is written
                out[(w, ext)] = (path, resized.size)
    return out

def object_key(key, width, ext):
    return f"{PREFIX}/{key}-{width}.{ext}"

def md5_hex(path):
    return hashlib.md5(path.read_bytes()).hexdigest()

def remote_state(s3, bucket, okey, local):
    """'new', 'same', or 'conflict'. Single-part uploads have ETag == MD5, which is what we compare."""
    from botocore.exceptions import ClientError
    try:
        head = s3.head_object(Bucket=bucket, Key=okey)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"): return "new"
        raise
    etag = head["ETag"].strip('"')
    return "same" if etag == md5_hex(local) else "conflict"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="show the plan; change nothing in R2")
    args = ap.parse_args()
    env = load_env()
    needed = ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET"]
    missing = [k for k in needed if not env.get(k)]
    if missing:
        sys.exit(f"Missing {', '.join(missing)} in .env. See the R2 section of README.md.")
    try:
        import boto3
    except ImportError:
        sys.exit("boto3 is not installed. Run: python3 -m venv .venv && .venv/bin/pip install boto3 pillow")
    s3 = boto3.client("s3", endpoint_url=f"https://{env['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
                      aws_access_key_id=env["R2_ACCESS_KEY_ID"], aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"],
                      region_name="auto")
    bucket = env["R2_BUCKET"]

    plan, problems = [], []
    for key, rec in IMAGES.items():
        if not (ROOT / rec["file"]).exists():
            problems.append(f"{key}: original {rec['file']} not found"); continue
        versions = make_versions(key, rec)
        # Auto-fill the intrinsic size of the 1600 px WebP, so the page can reserve space before the image loads.
        rec["width"], rec["height"] = versions[(1600, "webp")][1]
        for (w, ext), (path, _) in sorted(versions.items()):
            okey = object_key(key, w, ext)
            state = remote_state(s3, bucket, okey, path)
            if state == "conflict":
                problems.append(f"{okey} already exists with different content. Use a new key, e.g. {key}-v2.")
            plan.append((state, okey, path, FORMATS[ext][1]))
    (ROOT / "images.json").write_text(json.dumps(IMAGES, ensure_ascii=False, indent=2) + "\n")
    # Fonts and their licence files (fonts.json): same rules, same never-overwrite check.
    for item in json.loads((ROOT / "fonts.json").read_text()):
        path = ROOT / item["file"]
        okey = f"tangthu/{item['key']}"  # fonts live beside img/, not inside it
        state = remote_state(s3, bucket, okey, path)
        if state == "conflict":
            problems.append(f"{okey} already exists with different content. Use a new key.")
        plan.append((state, okey, path, item["content_type"]))

    if problems:
        print("STOPPED. Nothing was uploaded.")
        for p in problems: print("  - " + p)
        sys.exit(1)

    for state, okey, path, _ in plan:
        label = {"new": "UPLOAD", "same": "SKIP (already in R2, same content)"}[state]
        print(f"{label:<36} {bucket}/{okey}")
    if args.dry_run:
        print(f"Dry run: {sum(s == 'new' for s, *_ in plan)} to upload, {sum(s == 'same' for s, *_ in plan)} already there. Nothing uploaded.")
        return

    for state, okey, path, ctype in plan:
        if state != "new": continue
        s3.put_object(Bucket=bucket, Key=okey, Body=path.read_bytes(), ContentType=ctype, CacheControl=CACHE)
        print(f"uploaded {okey}")
    print(f"Done. {sum(s == 'new' for s, *_ in plan)} uploaded.")

if __name__ == "__main__":
    main()
