import sys
from os import path, walk

from .compiler_version_getter import detect_version


def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write("Wrong argument count.\n")
        sys.exit(1)

    arg = sys.argv[1]
    if path.isfile(arg):
        if not arg.endswith(".sol"):
            sys.stderr.write("Wrong file extension.\n")
            sys.exit(1)
        oldest_version, newest_version = detect_version([arg])
    elif path.isdir(arg):
        files = []
        for root, _, filenames in walk(arg):
            for filename in filenames:
                if filename.endswith(".sol"):
                    files.append(path.join(root, filename))
        if not files:
            sys.stderr.write("No file found in the directory.\n")
            sys.exit(1)
        oldest_version, newest_version = detect_version(files)
    else:
        sys.stderr.write("File not found.\n")
        sys.exit(1)

    print("{}.{}.{}".format(*oldest_version), "{}.{}.{}".format(*newest_version))
