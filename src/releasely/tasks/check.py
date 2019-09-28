import re
from releasely.release_info import get_release_info

class Issue:

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        parts = re.findall('[A-Z][^A-Z]*', self.__class__.__name__)
        message = ' '.join([parts[0]] + [part.lower() for part in parts[1:]])
        if self.message:
            message = '{}: {}.'.format(message, self.message)

        return message.strip('.') + '.'


class NoReleaseNotes(Issue):
    pass


def check_release_info():
    try:
        release_type, release_notes = get_release_info()
        if not release_notes.strip():
            return [NoReleaseNotes()]
    except Exception as e:
        return [Issue(e)]

    return []


def check():
    errors = []
    errors.extend(check_release_info())
    if errors:
        return '\n'.join(map(str, errors))
    else:
        return None



