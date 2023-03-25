import re
import logging
from hashlib import md5


class FileManipulator:
    """
    Edit files inside project
    """
    def __init__(self, file_path: str):
        """

        :param file_path:
        """
        self.file_path = file_path

    @property
    def contents(self) -> str:
        """
        Get file contents
        :return:
        """
        with open(self.file_path, encoding="utf-8") as file:
            return file.read()

    @property
    def lines(self) -> list:
        """
        Get file lines
        :return:
        """
        with open(self.file_path, encoding="utf-8") as file:
            return [line.rstrip() for line in file]

    def define(self, key, value, prepend: bool = True):
        """
        Define constant
        :param prepend:
        :param key:
        :param value:
        :return:
        """
        define = f"#define {key}"
        contents = self.contents
        lines = [line.strip() for line in contents.split("\n")]
        existing = next(line for line in lines if line.startswith(define))

        if existing:
            logging.info(f"replacing existing {existing}")

            return self.replace_line(existing, f"#define {key} ({value})")
        else:
            logging.info(f"adding new #define {key} ({value})")

            if prepend:
                contents = f"#define {key} ({value})\n\n{contents}"
            else:
                contents += f"\n\n#define {key} ({value})"

        return self.write(contents)

    def replace(self, find: str, replace: str, all: bool = False):
        """
        Replace occurrences of given string
        :param all:
        :param find:
        :param replace:
        :return:
        """
        return self.write(self.contents.replace(find, replace, 99999 if all else 1))

    def replace_line(self, find: str, replace: str):
        """
        Replace line that starts with given string
        :param find:
        :param replace:
        :return:
        """
        lines = self.lines
        match = -1

        for i, line in enumerate(lines):
            if line.strip().startswith(find):
                match = i
                break

        if match == -1:
            return self

        lines[match] = replace
        self.writelines(lines)

        return self

    def append_once(self, line: str, alias: str = ""):
        """
        Short for append_line(line, once=True)
        :param alias:
        :param line:
        :return:
        """
        return self.append_line(line, once=True, alias=alias)

    def append_line(self, line: str, once: bool = False, alias: str = ""):
        """
        Append line to the end of file
        :param alias:
        :param line:
        :param once:
        :return:
        """
        return self.append_lines(line, once=once or alias != "", alias=alias)

    def append_lines(self, *args, once: bool = False, alias: str = ""):
        """
        Append lines to the end of file
        :param alias:
        :param args:
        :param once:
        :return:
        """
        if once:
            hash, appends = self.wrap_once(*args, alias=alias)
        else:
            hash, appends = "", args

        self.writelines(self.lines + list(appends), hash=hash, keep="last")

    def add_after(self, find: str, contents: str, alias: str = ""):
        """
        Add contents after given string
        :param alias:
        :param find:
        :param contents:
        :return:
        """
        try:
            lines = self.lines
            plain_lines = [line.strip() for line in lines]
            match = plain_lines.index(find) + 1
            hash, appends = self.wrap_once(*contents.split("\n"), alias=alias)

            return self.writelines(lines[:match] + appends + lines[match:], hash=hash, keep="first")
        except ValueError:
            logging.warning(f"Cannot find line `{find}`")

    def comment_line(self, find: str):
        """
        Comment out line with //
        :param find:
        :return: self
        """
        return self.replace_line(find=find, replace=f"// {find}")

    def writelines(self, lines: list, hash: str = "", keep: str = ""):
        """
        Write given lines to file
        :param hash:
        :param keep:
        :param lines:
        :return:
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines))

        if hash:
            self.deduplicate(hash, keep=keep)

        return self

    def write(self, contents: str):
        """

        :param contents:
        :return:
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(contents)

        return self

    def wrap_once(self, *args, alias: str = "") -> tuple:
        """

        :param alias:
        :param args:
        :return:
        """
        hashable = alias.strip() if len(alias.strip()) > 0 else "\n".join(args)
        hash = md5(hashable.encode()).hexdigest()

        return hash, [
            "\n"
            f"#ifndef APPEND_LINES_{hash}",
            f"#define APPEND_LINES_{hash}",
            *args,
            f"#endif // APPEND_LINES_{hash}"
        ]

    def deduplicate(self, hash: str, keep: str):
        """
        Remove duplicates of #once blocks
        :return:
        """
        if not hash:
            return

        assert keep in ("first", "last"), "deduplicate() keep must be one of first or last"

        contents = self.contents
        pattern = f"#ifndef APPEND_LINES_{hash}[\s\S]+?#endif // APPEND_LINES_{hash}\s*"
        repeat_pattern = f"((?:{pattern})+)({pattern})" if keep == "last" else f"({pattern})((?:{pattern})+)"
        search = re.search(repeat_pattern, contents)

        if search is None:
            return

        if keep == "last":
            replace = search.group(2)
        else:
            replace = search.group(1)

        find = search.group(0)
        contents = contents.replace(find, replace)
        self.writelines(contents.split("\n"))
