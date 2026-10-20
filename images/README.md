# Site images

Photos for Zogam History are not stored in git. The originals live in this folder on the author's machine. `scripts/upload_images.sh` converts them to WebP and uploads them to the R2 bucket `kws-assets`, served at `https://assets.khual.net/tangthu/img/`.

## Naming rules

- Lowercase letters, numbers and hyphens only: `puan-tedim.jpg`, not `Puan Tedim (2).JPG`.
- Organise files by the page they illustrate, in one folder per chapter:
  `origins/`, `stories/`, `culture/`, `colonial/`, `faith/`, `modern/`, `diaspora/`, `evidence/`.
- The photo id in `photos.json` is the folder and file name without the extension: `culture/puan-tedim`.
- Never reuse a file name for a different picture. If an image changes, save it under a new name, or let the script add `-v2`, `-v3` and so on. Published files are never overwritten.

## Adding a photo

1. Save the image as `images/<chapter>/<name>.jpg` (or `.png`, `.webp`).
2. Run `scripts/upload_images.sh`. It converts to WebP, at most 1600 px wide, and uploads the file.
3. Add an entry to `photos.json` with the published `file` path, `alt`, `caption`, `credit`, `source` (a key from `sources.json`), `width` and `height`.
4. Use `{{photo:<id>}}` in the chapter HTML where the picture should go.

A photo that is still wanted uses `"status": "wanted"` and a `caption` that describes the picture needed. It renders as the placeholder box and needs no file, alt text or source.
