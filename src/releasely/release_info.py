import datetime
import re
import textwrap

from releasely.config import load_project_config
from releasely.git import file_tracked

DEFAULT_BLANK_MESSAGE = "< PUT RELEASE NOTES HERE >"

template = textwrap.dedent(
    """\
RELEASE_TYPE: {release_type}

{message}

Authors:

* {author}

"""
)

RELEASE_TYPE = re.compile(r"^RELEASE_TYPE: +(major|minor|patch|norelease)")

MAJOR = "major"
MINOR = "minor"
PATCH = "patch"
NORELEASE = "norelease"

VALID_RELEASE_TYPES = (MAJOR, MINOR, PATCH, NORELEASE)


def parse_release_file(contents):
    lines = contents.split("\n")
    matched = RELEASE_TYPE.match(lines[0])
    if matched:
        release_type = matched.group(1)
    else:
        raise ValueError("Unknown release type")

    if release_type not in VALID_RELEASE_TYPES:
        raise ValueError("Unknown release type")

    return release_type, "\n".join(lines[2:])


def get_release_info():
    config = load_project_config()
    release_file = config["filepaths"]["release_spec"]

    if not file_tracked(release_file):
        return NORELEASE, ""

    try:
        with open(release_file, "r") as f:
            return parse_release_file(f.read())
    except FileNotFoundError:
        return NORELEASE, ""


def update_changelog(new_version, release_notes):
    config = load_project_config()

    with open(config["filepaths"]["changelog"], "r") as f:
        current_contents = f.read()

    heading_for_new_version = "{} - {}".format(
        "v{}".format(new_version), datetime.datetime.now().date().isoformat()
    )

    border_for_new_version = "-" * len(heading_for_new_version)

    changelog_contents = """\
.. _v{new_version}:

{border_for_new_version}
{heading_for_new_version}
{border_for_new_version}

{release_notes}

{current_contents}
""".format(
        new_version=new_version,
        border_for_new_version=border_for_new_version,
        heading_for_new_version=heading_for_new_version,
        release_notes=release_notes.strip(),
        current_contents=current_contents.strip(),
    )

    with open(config["filepaths"]["changelog"], "w") as f:
        f.write(changelog_contents)
