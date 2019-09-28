import releasely.release_info
import releasely.version
import releasely.git
import logging


def main():
    if releasely.version.get_branch() == 'master':
        prepare_default_branch()
    elif releasely.version.get_branch().startswith('release-v'):
        prepare_release_branch()


def prepare_default_branch():
    config = releasely.config.load_project_config()
    release_type, release_notes = releasely.release_info.get_release_info()
    if release_type == releasely.release_info.NORELEASE:
        logging.info('No release pending. All Done.')
        return

    current_version = releasely.version.get_current_version()
    new_version = releasely.version.get_new_version(release_type)
    version_data = releasely.version.parse_version(new_version)

    releasely.version.bump(release_type)
    releasely.release_info.update_changelog(new_version, release_notes)
    releasely.git.delete(config['release_filepath'])
    releasely.git.add_tracked()
    releasely.git.commit(f'Cut Release and Updated changelog: v{current_version} -> v{new_version}')
    releasely.git.tag(f'v{new_version}')
    release_branch_name = 'release-v{}.{}'.format(version_data['major'], version_data['minor'])

    releasely.git.get_or_create_branch(release_branch_name)
    releasely.git.push(release_branch_name)
    releasely.git.push(f'v{new_version}')

    releasely.git.checkout('master')
    releasely.git.push('master')

def prepare_release_branch():
    config = releasely.config.load_project_config()
    release_type, release_notes = releasely.release_info.get_release_info()
    if release_type == releasely.release_info.NORELEASE:
        logging.info('No release pending. All Done.')
        return

    if release_type != releasely.release_info.PATCH:
        logging.warning('Only patch releases are allowed on release branches.')
        return

    # Check if we should use master instead
    if releasely.git.shared_head_with_ref('master'):
        logging.warning('This change appears to have been made on the wrong branch. You should make this change on the master branch.')
        return

    current_version = releasely.version.get_current_version()
    new_version = releasely.version.get_new_version(release_type)
    version_data = releasely.version.parse_version(new_version)

    releasely.version.bump(release_type)
    releasely.release_info.update_changelog(new_version, release_notes)
    releasely.git.delete(config['release_filepath'])
    releasely.git.add_tracked()
    releasely.git.commit(f'Cut Release and Updated changelog: v{current_version} -> v{new_version}')
    releasely.git.tag(f'v{new_version}')
    release_branch_name = 'release-v{}.{}'.format(version_data['major'], version_data['minor'])
    releasely.git.push(release_branch_name)
    releasely.git.push(f'v{new_version}')
