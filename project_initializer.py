from datetime import datetime
import json
import os.path
import requests
from typing import Any
import zipfile
import urllib.request

ID_FILENAME = ".qgis-ol-map"

GIT_OWNER = "qgis-ol-map"
GIT_REPO = "qgis-ol-map-template"

SKIP = object()

TEMPLATE_FILE_MAPPING = {
    "README.md": SKIP,
    "README.template.md": "README.md",
}


def get_id_file_path(target_dir: str) -> str:
    return str(target_dir).removesuffix("/") + "/" + ID_FILENAME


def is_project(target_dir: str) -> bool:
    try:
        return os.path.isdir(target_dir) and os.path.exists(
            get_id_file_path(target_dir)
        )
    except FileNotFoundError:
        return False


def is_empty(target_dir: str) -> bool:
    try:
        return os.path.isdir(target_dir) and not os.listdir(target_dir)
    except FileNotFoundError:
        return False


def initialize_project(target_dir: str):
    assert is_empty(target_dir)

    info = fetch_template_info()
    fetch_and_extract_template(info["zipball_url"], target_dir)

    save_project_id(target_dir, info)


def save_project_id(target_dir: str, info: dict[str, Any]):
    id_data = {
        "created": datetime.now().isoformat(),
        "template_version": info["tag_name"],
    }

    with open(get_id_file_path(target_dir), "w") as fp:
        json.dump(id_data, fp, indent=4)


def fetch_template_info() -> dict[str, Any]:
    url = f"https://api.github.com/repos/{GIT_OWNER}/{GIT_REPO}/releases/latest"
    response = requests.get(url, timeout=10)
    return response.json()


def fetch_and_extract_template(template_zip_url: str, target_dir: str):
    zip_path, _ = urllib.request.urlretrieve(template_zip_url)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        names = zip_ref.namelist()
        for name in names:
            if name.endswith("/"):
                continue

            _, target_file_name = name.split("/", maxsplit=1)
            target_file_name = TEMPLATE_FILE_MAPPING.get(target_file_name, target_file_name)
            if target_file_name is SKIP:
                continue

            target_path = target_dir.removesuffix("/") + "/" + target_file_name

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "wb") as target_ref:
                target_ref.write(zip_ref.read(name))
