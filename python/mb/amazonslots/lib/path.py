import os


def get_repo_root():
    here = os.path.join(os.getcwd(), __file__)
    parent = os.path.dirname(here)
    while here != parent:
        if os.path.exists(os.path.join(here, ".git")):
            return here
        here, parent = parent, os.path.dirname(parent)
    raise RuntimeError("failed to determine repo root")
