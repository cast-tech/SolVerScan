from typing import List
from .remove_comments import remove_comments


class SourceManager:
    def __init__(self, source_file_names: List[str]):
        self._source_file_names = source_file_names
        self._source_codes = [
            self._get_source_code(source_file_name)
            for source_file_name in self._source_file_names
        ]

    def get_source_codes(self) -> List[str]:
        return self._source_codes

    def remove_comments(self) -> None:
        source_codes_without_comments = []
        for source_code in self._source_codes:
            source_codes_without_comments.append(
                "\n".join(remove_comments(source_code.splitlines()))
            )
        self._source_codes = source_codes_without_comments

    def _get_source_code(self, source_file_name: str) -> str:
        lines = []
        with open(source_file_name, "r", encoding="utf8") as source_file:
            lines = source_file.readlines()
        return "".join(lines)
