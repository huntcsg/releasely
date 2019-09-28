import sys
from releasely.tasks import prepare_release
from releasely.tasks import release_notes
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    if sys.argv[1] == 'prepare-release':
        prepare_release.main()

    if sys.argv[1] == 'release-notes':
        release_notes.main()


if __name__ == '__main__':
    main()
