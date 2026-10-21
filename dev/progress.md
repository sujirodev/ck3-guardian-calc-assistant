# Guardian Calculation Assistant: progress

Short file: where things stand and what comes next. Rewrite it, do not append history. Lasting decisions go to
`decisions.md`; each feature's state lives in `features.json`.

## Now
- Released: 1.0.2 (GitHub Releases, Nexus Mods)
- Active feature: f06 (release through the shared pipeline)
- State: branch `pipeline-compartilhado` moves the release to the reusable workflow in
  [ck3-mod-maker](https://github.com/sujirodev/ck3-mod-maker) (tag `v1`). The new `pipeline/package.py` builds a zip
  byte-for-byte equal to the old `tools/package.py` one for 1.0.2 (checked 2026-10-21; only README.md differs, since
  this branch edits it). Not pushed yet.
- Blockers: none

## Next
1. Review the branch, merge into main and push (a push without a tag only builds, it does not publish).
2. Check the Package workflow run; mark f06 `done` with the run link as evidence.

## In-game testing
- Test save: (define one)
- Last recorded check: none
