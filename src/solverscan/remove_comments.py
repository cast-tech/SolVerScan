from sys import argv


def remove_comments(lines: list) -> list:
    modified_lines = []
    is_in_block_comment = False
    is_in_double_quoted_string = False
    is_in_single_quoted_string = False
    for line in lines:
        modified_lines.append("")
        ignore_a_symbol = False
        for index, symbol in enumerate(line):
            if ignore_a_symbol:
                ignore_a_symbol = False
                continue

            if is_in_double_quoted_string:
                if symbol == "\\":
                    modified_lines[-1] += line[index : index + 2]
                    ignore_a_symbol = True
                    continue
                if symbol == '"':
                    is_in_double_quoted_string = False
                modified_lines[-1] += symbol
                continue

            if is_in_single_quoted_string:
                if symbol == "\\":
                    modified_lines[-1] += line[index : index + 2]
                    ignore_a_symbol = True
                    continue
                if symbol == "'":
                    is_in_single_quoted_string = False
                modified_lines[-1] += symbol
                continue

            if is_in_block_comment:
                if line[index : index + 2] == "*/":
                    is_in_block_comment = False
                    ignore_a_symbol = True
                continue
            if line[index : index + 2] == "/*":
                is_in_block_comment = True
                ignore_a_symbol = True
                continue
            if line[index : index + 2] == "//":
                ignore_a_symbol = True
                break
            if symbol == '"':
                is_in_double_quoted_string = True
            if symbol == "'":
                is_in_single_quoted_string = True
            modified_lines[-1] += symbol
    return modified_lines


if __name__ == "__main__":
    with open(argv[1], "r") as file:
        lines = file.read().splitlines()
    modified_lines = [line + "\n" for line in remove_comments(lines)]
    print(*modified_lines, sep="")
