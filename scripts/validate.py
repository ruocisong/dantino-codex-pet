#!/usr/bin/env python3
import json
import math
from pathlib import Path

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "package" / "pet.json"
ATLAS = ROOT / "package" / "spritesheet.webp"
CHROMA_KEY = (255, 0, 255)  # Dantino uses magenta; green belongs to the laurel.
CHROMA_FRINGE_THRESHOLD = 96.0
CHROMA_FRINGE_EDGE_RADIUS = 2
CHROMA_FRINGE_ALPHA_MINIMUM = 16


def chroma_fringe_count(image: Image.Image) -> int:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    alpha_pixels = (
        alpha.get_flattened_data()
        if hasattr(alpha, "get_flattened_data")
        else alpha.getdata()
    )
    visible = [value > 0 for value in alpha_pixels]
    transparent = Image.new("L", alpha.size)
    transparent.putdata([0 if value else 255 for value in visible])
    expanded = transparent.filter(
        ImageFilter.MaxFilter(CHROMA_FRINGE_EDGE_RADIUS * 2 + 1)
    )
    rgba_pixels = (
        rgba.get_flattened_data()
        if hasattr(rgba, "get_flattened_data")
        else rgba.getdata()
    )
    alpha_pixels = (
        alpha.get_flattened_data()
        if hasattr(alpha, "get_flattened_data")
        else alpha.getdata()
    )
    nearby_pixels = (
        expanded.get_flattened_data()
        if hasattr(expanded, "get_flattened_data")
        else expanded.getdata()
    )
    return sum(
        alpha_value >= CHROMA_FRINGE_ALPHA_MINIMUM
        and nearby_transparency > 0
        and math.dist(color[:3], CHROMA_KEY) <= CHROMA_FRINGE_THRESHOLD
        for color, alpha_value, nearby_transparency in zip(
            rgba_pixels,
            alpha_pixels,
            nearby_pixels,
        )
    )


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
    magenta_fringe = chroma_fringe_count(image)
    assert magenta_fringe == 0, f"#FF00FF chroma fringe pixels: {magenta_fringe}"

    print("Dantino package validation passed")
    print("atlas=1536x2288 RGBA WebP, grid=8x11, cell=192x208, version=2")
    print("chroma_key=#FF00FF, chroma_fringe_pixels=0")


if __name__ == "__main__":
    main()
