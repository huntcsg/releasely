import subprocess


def add(*files):
    return subprocess.check_output(['git', 'add'] + files).decode('utf-8').strip()


def delete(filepath):
    return subprocess.check_output(['git', 'rm', filepath]).decode('utf-8').strip()


def commit(message):
    return subprocess.check_output(['git', 'commit', '-m', message]).decode('utf-8').strip()


def tag(name):
    return subprocess.check_output(['git', 'tag', name])


def rev_parse(ref, abbreviated_ref=True):
    command = ['git', 'rev-parse', ref]

    if abbreviated_ref:
        command.insert(-1, '--abbrev-ref')

    return subprocess.check_output(command).decode('utf-8').strip()


def log(n=None, oneline=None):

    command = ['git', 'log']

    if oneline:
        command.append('--oneline')

    if n:
        command.extend(['-n', str(n)])

    return subprocess.check_output(command).decode('utf-8').strip()


def add_tracked():
    subprocess.check_output(['git', 'add', '-u', '.'])


def get_or_create_branch(name):
    branches = subprocess.check_output(['git', 'branch']).decode('utf-8').strip()
    for branch in branches.split('\n'):
        if branch.strip().strip('*').strip() == name:
            subprocess.check_output(['git', 'checkout', name])
            break
    else:
        subprocess.check_output(['git', 'checkout', '-b', name]).decode('utf-8').strip()

    subprocess.check_output(['git', 'merge', 'master', '--ff-only'])


def file_tracked(filepath):
    result = subprocess.run(['git', 'ls-files', '--error-unmatch', filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return False
    else:
        return True
