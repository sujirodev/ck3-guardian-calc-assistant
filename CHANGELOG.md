# Changelog

One section per version, newest first. The release workflow publishes the section matching the tag as the GitHub Release notes and the Nexus Mods changelog, and fails if it is missing.

Each entry is one line starting with `- ` (one changelog line on Nexus Mods).

## [1.0.2] - 2026-10-21

- The score now shows the icon of the projected education trait instead of ~R1-~R4.
- The tooltip names the projected education trait, with its icon.
- Children without an education focus yet now get a projection too, assuming the guardian's best skill as the focus; the icon shows a ? and the tooltip names the assumed focus.
- With an assumed focus, the child's childhood trait now counts for or against it, as it will once that focus is chosen.
- The projection now adds the average coming-of-age bonuses that already apply: university, dynasty kin legacy, the ward's culture and the court tutor at the guardian's court, shown factor by factor in the tooltip.

## [1.0.1] - 2026-10-20

- Added a launcher thumbnail.

## [1.0.0] - 2026-10-20

- GCA score on every candidate in Educate Child, Offer Guardianship and Offer Ward: the vanilla chance of education progress per birthday, plus the projected education rank.
- Tooltip with the full breakdown: progress and no-progress weights, point projection, and notes for Beacon of Learning, Pedagogy, commander trait transfer, Knighthood and different faith or culture.
- New Find Guardian (GCA) interaction: searches your court and every court in diplomatic range, then opens Educate Child or Offer Ward pre-filled.
- Find Guardian opens sorted by score, with GCA: by score and Default list buttons under the native sort dropdown.
- Quick / Intelligent / Genius filter, and the native Traits filter added to the filter panel.
- English and Brazilian Portuguese (Portuguese needs the community PT-BR translation).
