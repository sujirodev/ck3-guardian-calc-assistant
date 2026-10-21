# Renders docs/images/src/*.html to PNG with headless Chrome or Edge.
# Usage: python tools/render_images.py [name ...]   (default: all)
# Set CHROME to override the browser path.
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "images" / "src"
OUT = ROOT / "docs" / "images"

# (source, output, width, height, scale, extra copy relative to ROOT or None)
# Output size is width x height times scale.
IMAGES = [
    ("banner", "banner", 1920, 480, 1, None),
    ("feature_score", "feature_score", 1600, 820, 1, None),
    ("feature_search", "feature_search", 1600, 720, 1, None),
    ("feature_formula", "feature_formula", 1600, 720, 1, None),
    ("translate", "translate", 1600, 500, 1, None),
    ("thumbnail", "thumbnail", 512, 512, 1, "thumbnail.png"),
    # Nexus Mods page: header 1300x372 (rendered at 2x), gallery 1920x1080.
    ("banner", "nexus_header", 1625, 465, 1.6, None),
    ("cover", "nexus_gallery_0_cover", 1920, 1080, 1, None),
    ("feature_score", "nexus_gallery_1_score", 1600, 900, 1.2, None),
    ("feature_search", "nexus_gallery_2_search", 1600, 900, 1.2, None),
    ("feature_formula", "nexus_gallery_3_formula", 1600, 900, 1.2, None),
]

CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "google-chrome",
    "chromium",
]


def browser():
    for c in CANDIDATES:
        if c and (Path(c).exists() or shutil.which(c)):
            return c
    sys.exit("No Chrome/Edge found; set CHROME")


def main():
    exe = browser()
    wanted = set(sys.argv[1:])
    for src, name, w, h, scale, copy in IMAGES:
        if wanted and name not in wanted and src not in wanted:
            continue
        out = OUT / f"{name}.png"
        subprocess.run(
            [
                exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--force-device-scale-factor={scale}", "--virtual-time-budget=4000",
                f"--window-size={w},{h}", f"--screenshot={out}",
                (SRC / f"{src}.html").as_uri(),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if copy:
            shutil.copyfile(out, ROOT / copy)
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
