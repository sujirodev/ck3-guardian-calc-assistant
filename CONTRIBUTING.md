# Contributing

Bug reports, translations and pull requests are welcome.

- **Bugs:** open a [bug report](../../issues/new?template=bug_report.yml) with your game version, GCA version and mod list.
- **Translations:** see below, or open a [translation request](../../issues/new?template=translation_request.yml) if you only want to ask for one.

## Translations

GCA has 40 short strings in one file per language. To add a language:

1. Copy `localization/english/tnt_ga_l_english.yml` to `localization/<folder>/tnt_ga_l_<folder>.yml`, using a folder from the table.
2. Change the first line from `l_english:` to `l_<folder>:`.
3. Translate only the text between the quotes. Keep the keys (`tnt_ga_...:0`) and everything inside `[...]` exactly as they are. Codes like `#P`, `#N` and `#!` are colours; keep them around the same words.
4. Save the file as **UTF-8 with BOM**. CK3 ignores localization files without the BOM.
5. Open a pull request, or attach the file to a [translation request](../../issues/new?template=translation_request.yml).

| Language | Folder |
|---|---|
| French | `french` |
| German | `german` |
| Spanish | `spanish` |
| Russian | `russian` |
| Polish | `polish` |
| Simplified Chinese | `simp_chinese` |
| Korean | `korean` |
| Japanese | `japanese` |

Languages outside this list only work if a community translation mod adds them to the game, the way the PT-BR translation adds `braz_por`. Mention which mod in the request.

Use the terms the game itself uses in your language for "guardian", "ward", "education" and the trait names, so the mod reads like part of the game. They are in the game's `localization/<folder>/` files.

## Code

The two GUI files are generated; see [Development](README.md#development) in the README. Test with `-debug_mode` and check `logs/error.log` before opening a pull request.
