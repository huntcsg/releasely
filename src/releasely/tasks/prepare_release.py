import logging
import re

import releasely.git
import releasely.release_info
import releasely.version


major_release_re = re.compile(r'^release-v\d+$')
minor_release_re = re.compile(r'^release-v\d+\.\d+$')

def augment_parser(parent_parser, subparsers):
    parser = subparsers.add_parser(
        "prepare-release", parents=[parent_parser], add_help=False
    )

    parser.add_argument(
        "--no-push",
        action="store_false",
        dest="push",
        default=True,
        help="Prevents pushing to any remote.",
    )
    parser.set_defaults(task=main)


def main(options):
    branch = releasely.version.get_branch()
    if branch == releasely.git.get_default_branch():
        prepare_default_branch(options)
    elif major_release_re.match(branch):
        prepare_minor_release_branch(options)
    elif minor_release_re.match(branch):
        prepare_major_release_branch(options)


def prepare_default_branch(options):
    config = releasely.config.load_project_config()
    default_branch = releasely.git.get_default_branch()
    release_type, release_notes = releasely.release_info.get_release_info()
    if release_type == releasely.release_info.NORELEASE:
        logging.info("No release pending. All Done.")
        return

    current_version = releasely.version.get_current_version()
    new_version = releasely.version.get_new_version(release_type)
    version_data = releasely.version.parse_version(new_version)

    releasely.version.bump(release_type)
    releasely.release_info.update_changelog(new_version, release_notes)
    releasely.git.delete(config["filepaths"]["release_spec"])
    releasely.git.add_tracked()
    releasely.git.commit(
        "Cut Release and Updated changelog: v{current_version} → v{new_version}".format(
            current_version=current_version, new_version=new_version
        )
    )

    tag = "v{}".format(new_version)
    releasely.git.tag(tag)
    if options.push:
        releasely.git.push(tag)

    minor_release_branch_name = "release-v{}.{}".format(
        version_data["major"], version_data["minor"]
    )

    major_release_branch_name = "release-v{}".format(
        version_data["major"],
    )

    for release_branch_name in [minor_release_branch_name, major_release_branch_name]:
        releasely.git.get_or_create_branch(release_branch_name)
        if options.push:
            releasely.git.push(release_branch_name)

    releasely.git.checkout(default_branch)

    if options.push:
        releasely.git.push(default_branch)


def prepare_minor_release_branch(options):
    config = releasely.config.load_project_config()
    default_branch = releasely.git.get_default_branch()
    release_type, release_notes = releasely.release_info.get_release_info()
    if release_type == releasely.release_info.NORELEASE:
        logging.info("No release pending. All Done.")
        return

    if release_type != releasely.release_info.PATCH:
        logging.warning("Only patch releases are allowed on release branches.")
        return

    current_version = releasely.version.get_current_version()
    new_version = releasely.version.get_new_version(release_type)
    version_data = releasely.version.parse_version(new_version)

    releasely.version.bump(release_type)
    releasely.release_info.update_changelog(new_version, release_notes)
    releasely.git.delete(config["filepaths"]["release_spec"])
    releasely.git.add_tracked()
    releasely.git.commit(
        "Cut Release and Updated changelog: v{current_version} → {new_version}".format(
            current_version=current_version, new_version=new_version
        )
    )
    releasely.git.tag("v{}".format(new_version))
    release_branch_name = "release-v{}.{}".format(
        version_data["major"], version_data["minor"]
    )

    if options.push:
        releasely.git.push(release_branch_name)
        releasely.git.push("v{}".format(new_version))


def prepare_major_release_branch(options):
    config = releasely.config.load_project_config()
    default_branch = releasely.git.get_default_branch()
    release_type, release_notes = releasely.release_info.get_release_info()
    if release_type == releasely.release_info.NORELEASE:
        logging.info("No release pending. All Done.")
        return

    if release_type not in (releasely.release_info.MINOR, releasely.release_info.PATCH):
        logging.warning("Only minor and patch releases are allowed on release branches.")
        return

    current_version = releasely.version.get_current_version()
    new_version = releasely.version.get_new_version(release_type)
    version_data = releasely.version.parse_version(new_version)

    releasely.version.bump(release_type)
    releasely.release_info.update_changelog(new_version, release_notes)
    releasely.git.delete(config["filepaths"]["release_spec"])
    releasely.git.add_tracked()
    releasely.git.commit(
        "Cut Release and Updated changelog: v{current_version} -> v{new_version}".format(
            current_version=current_version, new_version=new_version
        )
    )
    tag = "v{}".format(new_version)
    releasely.git.tag(tag)
    if options.push:
        releasely.git.push(tag)

    minor_release_branch_name = "release-v{}.{}".format(
        version_data["major"], version_data["minor"]
    )

    major_release_branch_name = "release-v{}".format(
        version_data["major"],
    )

    releasely.git.get_or_create_branch(minor_release_branch_name, major_release_branch_name)
    if options.push:
        releasely.git.push(minor_release_branch_name)

    releasely.git.checkout(major_release_branch_name)

    if options.push:
        releasely.git.push(major_release_branch_name)
