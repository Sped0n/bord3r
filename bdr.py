import os
from argparse import ArgumentParser

from PIL import Image
from tqdm.contrib.concurrent import process_map  # pyright: ignore[reportUnknownVariableType]

from davinci import Davinci
from scheduler import load_jobs


def parse_args():
    parser = ArgumentParser()
    _ = parser.add_argument("-d", "--dir", type=str, help="Path of dir")
    _ = parser.add_argument(
        "-l", "--location", type=str, required=False, help="Watermark geo location"
    )
    _ = parser.add_argument(
        "-w", "--workers", type=int, default=2, required=False, help="Number of workers"
    )
    _ = args = parser.parse_args()
    return args


class saver:
    def __init__(self, location: str, op_dir: str) -> None:
        self.__location = location
        # preprocess the dir path
        if op_dir[-1] != "/":
            self.__op_dir = op_dir
        else:
            self.__op_dir = op_dir[:-1]
        # if we don't have a save dir, create one
        try:
            os.mkdir(self.__op_dir + "/bord3r")
        except FileExistsError:
            pass

    def run(self, fp: str) -> None:
        d = Davinci(fp, self.__location).process()
        # resize image if width greater than 5000
        if d.size[0] > 5000:
            d = d.resize((5000, 5000), resample=Image.Resampling.LANCZOS)
        # save jpeg image
        d.save(
            self.__op_dir + "/bord3r/" + str(os.path.basename(fp)),
            "JPEG",
            quality=80,
            optimize=True,
        )


if __name__ == "__main__":
    # argparse
    args = parse_args()
    # intialize saver
    s = saver(args.location, args.dir)  # pyright: ignore[reportAny]
    # load jobs(tasks)
    jobs = load_jobs(args.dir)  # pyright: ignore[reportAny]

    # muultiprocessing with tqdm
    r = process_map(s.run, jobs, max_workers=args.workers)  # pyright: ignore[reportAny, reportUnknownVariableType]
