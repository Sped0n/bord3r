import os


def load_jobs(root: str) -> list[str]:
    jobs: list[str] = []
    # robust path handling
    try:
        assert os.path.exists(root) is True
    except AssertionError:
        raise FileNotFoundError(f"Path {root} does not exist.")
    # use os.walk to traverse files inside target dir
    for path, _, files in os.walk(root):
        for name in files:
            fpath = os.path.join(path, name)
            # only treat jpeg image as task
            if str.lower(fpath).endswith(".jpg") or str.lower(fpath).endswith(".jpeg"):
                jobs.append(str(fpath))
        # break here because we don't want to walk into subdirs
        break
    return jobs
