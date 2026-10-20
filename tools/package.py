# Builds the distributable zip:
#   guardian_calc_assistant.mod          launcher entry, relative path
#   guardian_calc_assistant/...          mod files (no tools/, no git files)
# Extract it into Documents/Paradox Interactive/Crusader Kings III/mod/.
#
# Usage: python tools/package.py [--tag vX.Y.Z] [--out dist]
# With --tag, fails unless the tag matches the descriptor.mod version.
import argparse
import re
import sys
import zipfile
from pathlib import Path

MOD_DIR = "guardian_calc_assistant"
ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["descriptor.mod", "README.md", "thumbnail.png", "common", "gui", "localization"]
# Fixed timestamp so identical sources give identical zips.
STAMP = (2020, 1, 1, 0, 0, 0)


def descriptor_field(text, key):
    m = re.search(rf'^{key}="([^"]*)"', text, re.M)
    if not m:
        sys.exit(f"descriptor.mod has no {key}")
    return m.group(1)


def add(zf, arcname, data):
    info = zipfile.ZipInfo(arcname, STAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag")
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()

    descriptor = (ROOT / "descriptor.mod").read_text(encoding="utf-8")
    version = descriptor_field(descriptor, "version")
    if args.tag and args.tag.removeprefix("v") != version:
        sys.exit(f"tag {args.tag} does not match descriptor.mod version {version}")

    # The launcher entry is the descriptor plus a path relative to the game's user folder.
    launcher_entry = descriptor.rstrip("\n") + f'\npath="mod/{MOD_DIR}"\n'

    files = []
    for name in INCLUDE:
        p = ROOT / name
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(f for f in p.rglob("*") if f.is_file())
    files.sort(key=lambda f: f.relative_to(ROOT).as_posix())

    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    zip_path = out / f"{MOD_DIR}-{version}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        add(zf, f"{MOD_DIR}.mod", launcher_entry.encode("utf-8"))
        for f in files:
            add(zf, f"{MOD_DIR}/{f.relative_to(ROOT).as_posix()}", f.read_bytes())
    print(zip_path)


if __name__ == "__main__":
    main()
