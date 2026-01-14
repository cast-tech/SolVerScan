from typing import List, Tuple
import re


class VersionDetector:
    _VERSIONS = (
        [(0, 4, i) for i in range(0, 27)]
        + [(0, 5, i) for i in range(0, 18)]
        + [(0, 6, i) for i in range(0, 13)]
        + [(0, 7, i) for i in range(0, 7)]
        + [(0, 8, i) for i in range(0, 34)]
    )

    __pragma_solidity_parser = re.compile(
        r"^(\s*pragma\s+solidity\s*"
        r'["\']?(((\^|>|>=|<|<=|=|~)?[\s?]*\d+\s*\.\s*\d+(\s*\.\s*\d+)?\s*)+)["\']?;)',
        re.M,
    )

    __compiler_version_part_injector = re.compile(
        r"^\s*pragma\s+solidity\s*"
        r'["\']?(((\^|>|>=|<|<=|=|~)?[\s?]*\d+\s*\.\s*\d+(\s*\.\s*\d+)?\s*)+)["\']?;',
        re.M,
    )

    __compiler_version_parser = re.compile(
        r"(\^|>|>=|<|<=|=|~)?[\s?]*(\d+)\s*\.\s*(\d+)(\s*\.\s*(\d+))?"
    )

    def __init__(
        self, major_version: int, patch_version_head: int, patch_version_tail: int
    ):
        self._patch = (major_version, patch_version_head, patch_version_tail)

    @classmethod
    def get_compatible_compiler_versions(cls, sources: list) -> list:
        version_restrictions = set()
        for source in sources:
            version_restrictions |= cls._get_module_version_restrictions(source)

        return cls._get_all_restrictions_meeting_versions(version_restrictions)

    @classmethod
    def _get_module_version_restrictions(cls, source_code: str) -> set:
        pragma_solidity_parts = cls.__get_source_code_pragma_solidity_parts(source_code)
        if not pragma_solidity_parts:
            return set()

        version_restrictions = set()
        for pragma_solidity_part in pragma_solidity_parts:
            compiler_version_part = cls.__get_source_code_compiler_version_part(
                pragma_solidity_part
            )
            version_restrictions |= cls.__get_one_pragma_compiler_version_restrictions(
                compiler_version_part
            )
        return version_restrictions

    @classmethod
    def _get_all_restrictions_meeting_versions(cls, version_restrictions: set) -> list:
        compatible_versions = []
        for version in cls._versions():
            if all(
                cls(*version)._meets_compare_conditions(*restriction)
                for restriction in version_restrictions
            ):
                compatible_versions.append(version)
        return compatible_versions

    @classmethod
    def _versions(cls) -> List[Tuple[int, int, int]]:
        return cls._VERSIONS

    def _meets_compare_conditions(self, comp: str, other: "VersionDetector") -> bool:
        if comp in {"^", "~"}:
            return self ^ other
        if comp == ">":
            return self > other
        if comp == ">=":
            return self >= other
        if comp == "<":
            return self < other
        if comp == "<=":
            return self <= other
        if comp in {"=", ""}:
            return self == other
        raise ValueError(f"Unknown compare type {comp}")

    @classmethod
    def __get_source_code_pragma_solidity_parts(cls, source_code: str) -> list:
        pragma_solidity_parts_parsed = []
        for line in source_code.split("\n"):
            pragma_solidity_parts_parsed += cls.__pragma_solidity_parser.findall(line)

        pragma_solidity_parts = []
        for pragma_solidity_part_parsed in pragma_solidity_parts_parsed:
            if not pragma_solidity_part_parsed:
                continue
            pragma_solidity_parts.append(pragma_solidity_part_parsed[0])
        return pragma_solidity_parts

    @classmethod
    def __get_source_code_compiler_version_part(cls, pragma_solidity_part: str) -> str:
        compiler_version_match = cls.__compiler_version_part_injector.match(
            pragma_solidity_part
        )
        if not compiler_version_match:
            return ""
        compiler_version_parsed = compiler_version_match.groups()
        if not compiler_version_match:
            return ""

        return compiler_version_parsed[0]

    @classmethod
    def __get_one_pragma_compiler_version_restrictions(
        cls, compiler_version_part: str
    ) -> set:
        version_restrictions_match_string = cls.__compiler_version_parser.findall(
            compiler_version_part
        )
        version_restrictions = set()
        for version_restriction in version_restrictions_match_string:
            operator = version_restriction[0]
            version = None
            if version_restriction[4] == "":
                version = VersionDetector(
                    int(version_restriction[1]), int(version_restriction[2]), 0
                )
            else:
                version = VersionDetector(
                    int(version_restriction[1]),
                    int(version_restriction[2]),
                    int(version_restriction[4]),
                )

            version_restrictions.add((operator, version))
        return version_restrictions

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VersionDetector):
            return self._patch == other._patch
        return False

    def __gt__(self, other: "VersionDetector") -> bool:
        return self._patch > other._patch

    def __lt__(self, other: "VersionDetector") -> bool:
        return self._patch < other._patch

    def __le__(self, other: "VersionDetector") -> bool:
        return self._patch <= other._patch

    def __ge__(self, other: "VersionDetector") -> bool:
        return self._patch >= other._patch

    def __xor__(self, other: "VersionDetector") -> bool:  # for ^ comparison
        return (
            self._patch[0] == other._patch[0]
            and self._patch[1] == other._patch[1]
            and self._patch[2] >= other._patch[2]
        )

    def __hash__(self) -> int:
        return hash(self._patch)
