import os
import random
import shutil
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

# CONFIG
SOURCE_ROOT = Path("data/kaggle_raw")
YOLO_ROOT = Path("data/yolo")
MAPPING_FILE = Path("data/class_mapping.yaml")
TRAIN_SPLIT = 0.8

CLASSES = [
    "user",
    "web_app",
    "gateway",
    "service",
    "database",
    "external_service",
]

CLASS_TO_ID = {c: i for i, c in enumerate(CLASSES)}


def load_mapping():
    with open(MAPPING_FILE, "r") as f:
        return yaml.safe_load(f)


def map_class(original_name, mapping):
    original_name = original_name.lower()
    for target_class, keywords in mapping.items():
        for kw in keywords:
            if kw in original_name:
                return target_class
    return None


def voc_to_yolo_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    xmin, ymin, xmax, ymax = box
    x = (xmin + xmax) / 2.0
    y = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin
    return x * dw, y * dh, w * dw, h * dh


def prepare_dirs():
    for split in ["train", "val"]:
        (YOLO_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
        (YOLO_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)


def main():
    prepare_dirs()
    mapping = load_mapping()

    xml_files = list(SOURCE_ROOT.rglob("*.xml"))
    random.shuffle(xml_files)

    split_index = int(len(xml_files) * TRAIN_SPLIT)

    for idx, xml_file in enumerate(xml_files):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        filename = root.findtext("filename")
        image_path = xml_file.parent / filename

        if not image_path.exists():
            continue

        with Image.open(image_path) as img:
            w, h = img.size

        yolo_lines = []

        for obj in root.findall("object"):
            original_class = obj.findtext("name")
            mapped_class = map_class(original_class, mapping)

            if mapped_class is None:
                continue

            class_id = CLASS_TO_ID[mapped_class]

            bnd = obj.find("bndbox")
            xmin = int(bnd.findtext("xmin"))
            ymin = int(bnd.findtext("ymin"))
            xmax = int(bnd.findtext("xmax"))
            ymax = int(bnd.findtext("ymax"))

            x, y, bw, bh = voc_to_yolo_bbox((w, h), (xmin, ymin, xmax, ymax))
            yolo_lines.append(f"{class_id} {x:.6f} {y:.6f} {bw:.6f} {bh:.6f}")

        if not yolo_lines:
            continue

        split = "train" if idx < split_index else "val"

        new_image_path = YOLO_ROOT / "images" / split / image_path.name
        new_label_path = YOLO_ROOT / "labels" / split / (xml_file.stem + ".txt")

        shutil.copy(image_path, new_image_path)
        with open(new_label_path, "w") as f:
            f.write("\n".join(yolo_lines))

    print("Conversion complete.")


if __name__ == "__main__":
    main()
