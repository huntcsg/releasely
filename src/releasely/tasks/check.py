import logging
import os
import re

import releasely.git
import releasely.release_info

logger = logging.getLogger(__name__)


def augment_parser(parent_parser, subparsers):
    parser = subparsers.add_parser("check", parents=[parent_parser], add_help=False)
    parser.set_defaults(task=main)


def main(options):
    errors = check()
    if errors:
        for error in errors:
            logger.critical(str(error))
            raise SystemExit(1)
    else:
        return


class Issue:
    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        parts = re.findall("[A-Z][^A-Z]*", self.__class__.__name__)
        message = " ".join([parts[0]] + [part.lower() for part in parts[1:]])
        if self.message:
            message = "{}: {}.".format(message, self.message)

        return message.strip(".") + "."


class NoReleaseNotes(Issue):
    pass


class NoReleaseSpec(Issue):
    pass


class ReleaseSpecNotTracked(Issue):
    pass


def check_release_info():
    config = releasely.config.load_project_config()
    errors = []

    release_spec_filepath = config["filepaths"]["release_spec"]

    if not os.path.exists(release_spec_filepath):
        errors.append(NoReleaseSpec())

    elif not releasely.git.file_tracked(release_spec_filepath):
        errors.append(ReleaseSpecNotTracked())

    else:
        release_type, release_notes = releasely.release_info.get_release_info()

        parts = release_notes.split('\n\nAuthors:\n\n')
        logger.debug(repr(parts))
        notes, authorship = parts

        if (
            not notes.strip()
            or notes.strip() == releasely.release_info.DEFAULT_BLANK_MESSAGE
        ):
            errors.append(NoReleaseNotes())

    return errors


def check():
    errors = []
    errors.extend(check_release_info())

    return errors
