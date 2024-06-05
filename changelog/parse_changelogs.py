#!/bin/python3

import logging
import os
import re
from collections import OrderedDict

logger = logging.getLogger(__name__)


def combine_sections_in_folder(folder_path):
    """Parser for changelog files following the https://keepachangelog.com
    format.
    """
    allowed_section_headers = [
        "Added",
        "Changed",
        "Deprecated",
        "Removed",
        "Fixed",
        "Security",
    ]
    sections = OrderedDict()

    for filename in os.listdir(folder_path):
        if filename.endswith(".md") and filename != "README.md":
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r") as file:
                current_section = None
                for line in file:
                    # find all headings starting with # (they should always
                    # start with ### but we seem to sometimes use # or ##)
                    match = re.match(r"^#+ (.*)", line)
                    if match:
                        section_header = match.group(1).strip().capitalize()
                        if section_header not in allowed_section_headers:
                            logger.warning(
                                f"warning: section_header {section_header} "
                                f"in file {filename} is invalid, "
                                "see https://keepachangelog.com for a list of "
                                "allowed types."
                            )
                        current_section = sections.get(section_header, [])
                    elif current_section is not None and line.strip():
                        current_section.append(line)
                        sections[section_header] = current_section

    combined_md = ""
    for section_header, lines in sections.items():
        combined_md += "### " + section_header + "\n\n"
        combined_md += "".join(lines) + "\n"

    return combined_md


if __name__ == "__main__":
    folder_path = "."
    combined_md = combine_sections_in_folder(folder_path)
    print(combined_md)
