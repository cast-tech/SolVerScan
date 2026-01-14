from typing import List

from .source_manager import SourceManager
from .version_detector import VersionDetector


def detect_version(file_paths: List[str]) -> tuple:
    source_manager = SourceManager(file_paths)
    source_manager.remove_comments()
    compatible_versions = VersionDetector.get_compatible_compiler_versions(
        source_manager.get_source_codes()
    )

    if len(compatible_versions) == len(VersionDetector._VERSIONS):
        # pragma solidity line missing
        return (compatible_versions[-1], compatible_versions[-1])

    if not compatible_versions:
        return ((0, 0, 0), (0, 0, 0))
    return (compatible_versions[0], compatible_versions[-1])
