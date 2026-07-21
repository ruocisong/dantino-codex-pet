#!/usr/bin/env python3
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "package" / "pet.json"
ATLAS = ROOT / "package" / "spritesheet.webp"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["id"] == "dantino"
    assert manifest["spriteVersionNumber"] == 2
    assert manifest["spritesheetPath"] == "spritesheet.webp"

    image = Image.open(ATLAS).convert("RGBA")
    assert image.size == (1536, 2288), image.size
    assert image.width % 8 == 0 and image.height % 11 == 0
    assert (image.width // 8, image.height // 11) == (192, 208)

    pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
    residue = sum(
        1
        for red, green, blue, alpha in pixels
        if alpha == 0 and (red or green or blue)
    )
    assert residue == 0, f"transparent RGB residue pixels: {residue}"

    print("Dantino package validation passed")
    print("atlas=1536x2288 RGBA WebP, grid=8x11, cell=192x208, version=2")


if __name__ == "__main__":
    main()
