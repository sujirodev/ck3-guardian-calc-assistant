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

# name: (width, height, extra copy destination relative to ROOT or None)
IMAGES = {
    "banner": (1920, 480, None),
    "feature_score": (1600, 820, None),
    "feature_search": (1600, 720, None),
    "feature_formula": (1600, 720, None),
    "translate": (1600, 500, None),
    "thumbnail": (512, 512, "thumbnail.png"),
}

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
    names = sys.argv[1:] or list(IMAGES)
    for name in names:
        w, h, copy = IMAGES[name]
        out = OUT / f"{name}.png"
        subprocess.run(
            [
                exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--virtual-time-budget=4000",
                f"--window-size={w},{h}", f"--screenshot={out}",
                (SRC / f"{name}.html").as_uri(),
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if copy:
            shutil.copyfile(out, ROOT / copy)
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
