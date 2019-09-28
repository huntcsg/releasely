import sys
from releasely.tasks import prepare_release
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    if sys.argv[1] == 'prepare-release':
        prepare_release.main()


if __name__ == '__main__':
    main()
