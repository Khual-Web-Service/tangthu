# Contributing to Zogam History

Thank you for helping preserve Zomi and Zo history. Every contribution is credited, and nothing is published without the consent of the person it concerns.

## The easiest way: email us
**[tangthu@khual.net](mailto:tangthu@khual.net)**. You don’t need a GitHub account.

| You want to… | Send us |
|---|---|
| **Correct a mistake** | The page, the sentence, and a source (book, article, link or document) |
| **Share an oral history** | A recording or written account, plus the speaker’s name, village, clan, dialect and date, and confirmation that they agree to publication |
| **Share a photo** | The photo, the date, the place, who is in it, and who took it |
| **Suggest a source** | The full citation and a link if one exists |

## Our standards
- **Every fact needs a source.** We can’t publish a claim we can’t cite.
- **We label evidence.** Oral tradition, documented history and scholarly interpretation are kept separate. Oral histories are welcome *as* oral history.
- **We stay neutral** on names, borders and the Manipur conflict. We report what each community says and what official figures show.
- **Consent first.** Testimonies about conflict or displacement can be anonymised. We never publish details that could put someone at risk.

## For developers
1. Fork the repo and edit the files in `content/` (citations are written `[[source-key]]`).
2. Add any new sources to `sources.json`.
3. Run `python3 build.py`. The build fails if a citation key is missing.
4. Open a pull request explaining your change and its source.

By contributing, you agree that your text is licensed under [CC BY-SA 4.0](LICENSE-CONTENT.md) and your code under [MIT](LICENSE). Photos and recordings stay yours; you grant us permission to publish them on the site with credit.
