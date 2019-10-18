import collections
import subprocess


def add(*files):
    return subprocess.check_output(["git", "add"] + files).decode("utf-8").strip()


def delete(filepath):
    return subprocess.check_output(["git", "rm", filepath]).decode("utf-8").strip()


def checkout(branch):
    return subprocess.check_output(["git", "checkout", branch]).decode("utf-8").strip()


def push(ref):
    return subprocess.check_output(["git", "push", "origin", ref])


def get_refs_by_commit():
    output = (
        subprocess.check_output(["git", "show-ref", "--head", "--heads"])
        .decode("utf-8")
        .strip()
    )
    refs_by_commit = collections.defaultdict(set)
    for line in output.split("\n"):
        commit, ref = line.split(" ")
        refs_by_commit[commit].add(ref)
    return refs_by_commit


def fetch():
    return subprocess.check_output(["git", "fetch"])


def show_ref(ref, remote="origin"):
    if remote:
        ref = "{}/{}".format(remote, ref)

    return (
        subprocess.check_output(["git", "show-ref", ref])
        .decode("utf-8")
        .strip()
        .split(" ")[0]
    )


def shared_head_with_ref(reference_ref="master"):
    fetch()
    branch = rev_parse("HEAD")
    remote_branch_ref = show_ref(branch, remote="origin")
    master_ref = show_ref(reference_ref, remote="origin")
    return remote_branch_ref == master_ref


def commit(message):
    return (
        subprocess.check_output(["git", "commit", "-m", message])
        .decode("utf-8")
        .strip()
    )


def tag(name):
    return subprocess.check_output(["git", "tag", name])


def rev_parse(ref, abbreviated_ref=True):
    command = ["git", "rev-parse", ref]

    if abbreviated_ref:
        command.insert(-1, "--abbrev-ref")

    return subprocess.check_output(command).decode("utf-8").strip()


def log(n=None, oneline=None):

    command = ["git", "log"]

    if oneline:
        command.append("--oneline")

    if n:
        command.extend(["-n", str(n)])

    return subprocess.check_output(command).decode("utf-8").strip()


def add_tracked():
    subprocess.check_output(["git", "add", "-u", "."])


def get_or_create_branch(name):
    branches = subprocess.check_output(["git", "branch"]).decode("utf-8").strip()
    for branch in branches.split("\n"):
        if branch.strip().strip("*").strip() == name:
            subprocess.check_output(["git", "checkout", name])
            break
    else:
        subprocess.check_output(["git", "checkout", "-b", name]).decode("utf-8").strip()

    subprocess.check_output(["git", "merge", "master", "--ff-only"])


def file_tracked(filepath):
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return False
    else:
        return True


def get_current_author():
    return subprocess.check_output(["git", "config", "--get", "user.name"]).decode("utf-8").strip()
