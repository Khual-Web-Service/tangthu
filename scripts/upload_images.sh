#!/usr/bin/env bash
# Convert images/ to WebP (max 1600 px wide) and upload them to the R2 bucket kws-assets
# under tangthu/img/. The site serves them from https://assets.khual.net/tangthu/img/.
#
# Usage:
#   scripts/upload_images.sh                 convert and upload what is new or changed
#   DRY_RUN=1 scripts/upload_images.sh       show the wrangler commands, upload nothing
#
# Never overwrites a published file. Each original is recorded in images/.uploaded
# (source path, sha256 of the original, published key). Files already recorded with the
# same hash are skipped. A changed original is published under a new key (-v2, -v3 ...).
# A new key is checked against the bucket first, and the script stops if that check fails.
#
# Requires: cwebp (brew install webp) or Pillow (pip install pillow), and `npx wrangler`
# logged in (npx wrangler login). cwebp does not apply EXIF rotation, so rotate phone
# photos before adding them.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMG="$ROOT/images"
OUT="$IMG/.webp"
MANIFEST="$IMG/.uploaded"
BUCKET="kws-assets"
PREFIX="tangthu/img"
MAX_WIDTH=1600
CACHE="public, max-age=31536000, immutable"
DRY_RUN="${DRY_RUN:-0}"

mkdir -p "$OUT"
touch "$MANIFEST"

sha() { shasum -a 256 "$1" | awk '{print $1}'; }

# Field $2 (hash) or $3 (published key) of the manifest line for source path $1.
manifest_lookup() {
  awk -F'\t' -v s="$1" -v f="$2" '$1 == s { print $f; exit }' "$MANIFEST"
}

# Returns 0 if an object exists in the bucket, 1 if it is confirmed absent.
# Any other failure stops the script, so an unknown state never leads to an overwrite.
remote_exists() { # key relative to the bucket prefix
  local tmp rc=0 err
  tmp="$(mktemp)"
  err="$(npx wrangler r2 object get "$BUCKET/$PREFIX/$1" --remote --file="$tmp" 2>&1)" || rc=$?
  rm -f "$tmp"
  if (( rc == 0 )); then return 0; fi
  if grep -qiE 'not ?found|does not exist|10007' <<<"$err"; then return 1; fi
  echo "Could not check whether $PREFIX/$1 exists in R2, so nothing was uploaded: $err" >&2
  exit 1
}

# True if a published key is already in use: recorded in the manifest, or in the bucket.
key_taken() {
  awk -F'\t' -v k="$1" '$3 == k { found = 1 } END { exit !found }' "$MANIFEST" && return 0
  remote_exists "$1"
}

# First free key with a -vN suffix before the extension, e.g. culture/puan.webp -> culture/puan-v2.webp.
versioned_key() {
  local key="$1" dir base ext stem n=2 cand
  dir="$(dirname "$key")"
  base="$(basename "$key")"
  ext="${base##*.}"
  stem="$(sed -E 's/-v[0-9]+$//' <<<"${base%.*}")"
  while :; do
    cand="$stem-v$n.$ext"
    [[ "$dir" != "." ]] && cand="$dir/$cand"
    if ! key_taken "$cand"; then printf '%s' "$cand"; return; fi
    n=$((n + 1))
  done
}

to_webp() { # source dst
  local src="$1" dst="$2" w=""
  mkdir -p "$(dirname "$dst")"
  if command -v cwebp >/dev/null 2>&1; then
    w="$(sips -g pixelWidth "$src" 2>/dev/null | awk '/pixelWidth/ { print $2 }')" || true
    if [[ -n "$w" && "$w" -gt "$MAX_WIDTH" ]]; then
      cwebp -quiet -q 82 -resize "$MAX_WIDTH" 0 "$src" -o "$dst"
    else
      cwebp -quiet -q 82 "$src" -o "$dst"
    fi
  elif python3 -c "import PIL" 2>/dev/null; then
    python3 - "$src" "$dst" "$MAX_WIDTH" <<'PY'
import sys
from PIL import Image, ImageOps

src, dst, max_w = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = ImageOps.exif_transpose(Image.open(src))
if im.mode not in ("RGB", "RGBA"):
    im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
if im.width > max_w:
    im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
im.save(dst, "WEBP", quality=82, method=6)
PY
  else
    echo "Need cwebp (brew install webp) or Pillow (pip install pillow)." >&2
    exit 1
  fi
}

uploaded=0
skipped=0
while IFS= read -r -d '' src; do
  rel="${src#"$IMG"/}"
  h="$(sha "$src")"
  prev_hash="$(manifest_lookup "$rel" 2)"
  if [[ -n "$prev_hash" && "$prev_hash" == "$h" ]]; then
    skipped=$((skipped + 1))
    continue
  fi

  if [[ -n "$prev_hash" ]]; then
    # The original changed. Keep the published object and publish the new one under a new key.
    key="$(versioned_key "$(manifest_lookup "$rel" 3)")"
    echo "changed: $rel -> $key (update photos.json if it uses the old file)"
  else
    key="${rel%.*}.webp"
    if key_taken "$key"; then
      key="$(versioned_key "$key")"
      echo "name in use: $rel -> $key"
    fi
  fi

  dst="$OUT/$key"
  to_webp "$src" "$dst"
  cmd=(npx wrangler r2 object put "$BUCKET/$PREFIX/$key" --file="$dst" --content-type=image/webp --cache-control="$CACHE" --remote)
  if [[ "$DRY_RUN" == 1 ]]; then
    echo "[dry-run] ${cmd[*]}"
    continue
  fi
  "${cmd[@]}"
  {
    awk -F'\t' -v s="$rel" '$1 != s' "$MANIFEST"
    printf '%s\t%s\t%s\n' "$rel" "$h" "$key"
  } > "$MANIFEST.tmp" && mv "$MANIFEST.tmp" "$MANIFEST"
  echo "uploaded: $PREFIX/$key"
  uploaded=$((uploaded + 1))
done < <(find "$IMG" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.tif' -o -iname '*.tiff' \) -not -path '*/.*' -print0 | sort -z)

if [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run. Nothing uploaded or recorded. Already uploaded: $skipped."
else
  echo "Done. Uploaded: $uploaded. Already uploaded: $skipped."
fi
