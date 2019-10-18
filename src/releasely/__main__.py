import argparse
import logging
import sys

import releasely.tasks


def get_parser():
    parser = argparse.ArgumentParser()

    # Verbosity
    parser.set_defaults(loglevel=logging.INFO)
    verbosity_group = parser.add_mutually_exclusive_group(required=False)
    verbosity_group.add_argument(
        "--verbose", dest="loglevel", action="store_const", const=logging.DEBUG
    )
    verbosity_group.add_argument(
        "--quiet", dest="loglevel", action="store_const", const=logging.CRITICAL
    )

    subparsers = parser.add_subparsers()

    for task_module in releasely.tasks.task_modules:
        if hasattr(task_module, "augment_parser"):
            task_module.augment_parser(parser, subparsers)

    return parser


def main():
    parser = get_parser()
    options = parser.parse_args()
    logging.basicConfig(level=options.loglevel)
    if hasattr(options, "task"):
        return options.task(options)
    else:
        parser.print_help()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
