"""Compare the old dlib HOG detector with YuNet on a folder of photos.

HOG runs inside the last dlib-based image, YuNet runs from this checkout.
Both use the service's logic: try the photo as is, then rotate by 90 degrees
up to three times until a face is found.

    uv run python -m scripts.compare_detectors ~/Pictures/some-folder

Writes one side-by-side PNG per photo (HOG in red on the left, YuNet in
green on the right) and a summary.md table into compare-out/.
"""

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from fuzzyoctodisco.pic import find_faces, image2raw

HOG_IMAGE = "ghcr.io/dixneuf19/fuzzy-octo-disco@sha256:92b7b6a9da09fd25cb03240fba88c2070c1578ba041136b8afdc2cad3303f79f"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

# Same rotate-until-found loop as fuzzyoctodisco.main.find_faces, run inside
# the HOG image. Prints {file name: [rotations, boxes]} as JSON.
HOG_SNIPPET = """
import json, os
from PIL import Image
from fuzzyoctodisco.pic import find_faces, image2raw
out = {}
for name in sorted(os.listdir("/pics")):
    if os.path.splitext(name)[1].lower() not in %r:
        continue
    im = Image.open(os.path.join("/pics", name)).convert("RGB")
    for rotations in range(4):
        boxes = find_faces(image2raw(im))
        if boxes:
            break
        im = im.transpose(Image.Transpose.ROTATE_90)
    out[name] = [rotations if boxes else 0, [list(b) for b in boxes]]
print(json.dumps(out))
""" % (sorted(EXTENSIONS),)


def detect_yunet(path):
    im = Image.open(path).convert("RGB")
    for rotations in range(4):
        boxes = find_faces(image2raw(im))
        if boxes:
            return rotations, boxes
        im = im.transpose(Image.Transpose.ROTATE_90)
    return 0, []


def detect_hog(folder, image):
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "python",
            "-v",
            f"{folder.resolve()}:/pics:ro",
            image,
            "-W",
            "ignore",
            "-c",
            HOG_SNIPPET,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return {
        name: (rot, boxes) for name, (rot, boxes) in json.loads(result.stdout).items()
    }


def draw(path, rotations, boxes, color, label):
    im = Image.open(path).convert("RGB")
    for _ in range(rotations):
        im = im.transpose(Image.Transpose.ROTATE_90)
    img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    thickness = max(2, img.shape[1] // 300)
    for left, top, right, bottom in boxes:
        cv2.rectangle(img, (left, top), (right, bottom), color, thickness)
    cv2.putText(
        img,
        f"{label}: {len(boxes)}",
        (10, 10 + 30 * thickness),
        cv2.FONT_HERSHEY_SIMPLEX,
        thickness,
        color,
        thickness,
    )
    return img


def side_by_side(left, right, height=600):
    def fit(img):
        scale = height / img.shape[0]
        return cv2.resize(img, (int(img.shape[1] * scale), height))

    return np.hstack([fit(left), fit(right)])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", type=Path)
    parser.add_argument("--out", type=Path, default=Path("compare-out"))
    parser.add_argument("--hog-image", default=HOG_IMAGE)
    args = parser.parse_args()

    photos = sorted(p for p in args.folder.iterdir() if p.suffix.lower() in EXTENSIONS)
    args.out.mkdir(parents=True, exist_ok=True)
    hog = detect_hog(args.folder, args.hog_image)

    rows = [
        "| photo | HOG faces | YuNet faces | rotations HOG / YuNet |",
        "|---|---|---|---|",
    ]
    totals = {"hog": 0, "yunet": 0, "differ": 0}
    for photo in photos:
        hog_rot, hog_boxes = hog[photo.name]
        yu_rot, yu_boxes = detect_yunet(photo)
        totals["hog"] += len(hog_boxes)
        totals["yunet"] += len(yu_boxes)
        differ = len(hog_boxes) != len(yu_boxes)
        totals["differ"] += differ
        rows.append(
            f"| {photo.name} | {len(hog_boxes)} | {len(yu_boxes)} | {hog_rot} / {yu_rot} |"
            + (" differs" if differ else "")
        )
        cv2.imwrite(
            str(args.out / f"{photo.stem}.png"),
            side_by_side(
                draw(photo, hog_rot, hog_boxes, (0, 0, 255), "HOG"),
                draw(photo, yu_rot, yu_boxes, (0, 200, 0), "YuNet"),
            ),
        )

    rows.append(
        f"\n{len(photos)} photos: HOG found {totals['hog']} faces, YuNet {totals['yunet']}, "
        f"face count differs on {totals['differ']}."
    )
    (args.out / "summary.md").write_text("\n".join(rows) + "\n")
    print("\n".join(rows))
    print(f"\nSide-by-side images in {args.out}/")


if __name__ == "__main__":
    main()
