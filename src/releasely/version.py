import subprocess
import releasely.git
import configparser


def get_branch():
    return releasely.git.rev_parse('HEAD')


def get_last_commit():
    return releasely.git.log(n=1, oneline=True)


def get_current_version():
    output = subprocess.check_output(['bumpversion', '--dry-run', '--list', 'patch']).decode('utf-8').strip()
    for line in output.split('\n'):
        if line.startswith('current_version='):
            return line.split('=')[-1].strip()
    else:
        raise RuntimeError('Current version not found :(')


def get_new_version(part):
    output = subprocess.check_output(['bumpversion', '--dry-run', '--list', part]).decode('utf-8').strip()
    for line in output.split('\n'):
        if line.startswith('new_version='):
            return line.split('=')[-1].strip()
    else:
        raise RuntimeError('Current version not found :(')


def bump(part):
    return subprocess.check_output(['bumpversion', part]).decode('utf-8').strip()


def parse_version(version):
    version_parts = version.split('.')
    return {
        'major': version_parts[0],
        'minor': version_parts[1],
        'patch': version_parts[2],
    }