import textwrap
import os
from releasely.config import load_project_config

template = textwrap.dedent("""\
RELEASE_TYPE: {release_type}

{message}
""")


def main():
    config = load_project_config()

    release_filepath = config['release_filepath']
    if os.path.exists(release_filepath):
        return

    else:
        with open(release_filepath, 'w') as f:
            f.write(template.format(release_type='patch', message='< PUT RELEASE NOTES HERE >'))
