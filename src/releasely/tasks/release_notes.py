import logging
import os

import releasely.config
import releasely.release_info

logger = logging.getLogger(__name__)


def augment_parser(parent_parser, subparsers):
    parser = subparsers.add_parser(
        "release-notes", parents=[parent_parser], add_help=False
    )
    parser.set_defaults(task=main)


def main(options):
    config = releasely.config.load_project_config()

    release_filepath = config["filepaths"]["release_spec"]
    if os.path.exists(release_filepath):
        logger.info("Release spec already exists. Nothing to do.")
        return

    else:
        with open(release_filepath, "w") as f:
            logger.info("Writing release spec.")
            f.write(
                releasely.release_info.template.format(
                    release_type=releasely.release_info.PATCH,
                    message=releasely.release_info.DEFAULT_BLANK_MESSAGE,
                    author=releasely.git.get_current_author(),
                )
            )
