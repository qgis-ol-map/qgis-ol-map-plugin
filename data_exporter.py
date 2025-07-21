from pathlib import Path


class DataExporter:
    def __init__(self, data_dir_path: str) -> None:
        self.data_dir_path = data_dir_path

    def process_url(self, url: str) -> str:
        if not self.is_local_file(url):
            return url

        source = Path(url)
        target = Path(self.data_dir_path) / source.name

        with source.open("rb") as source_fp:
            with target.open("wb") as target_fp:
                target_fp.write(source_fp.read())

        return "./data/" + source.name

    def is_local_file(self, url: str) -> bool:
        return url.startswith("/")
