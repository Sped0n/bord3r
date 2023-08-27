from typing import TypeAlias

import exiftool

ExifDict: TypeAlias = dict[str, str | int | float]


def get_exif(path: str) -> ExifDict:
    with exiftool.ExifToolHelper() as et:
        metadata: list[ExifDict] = et.get_metadata(path)
        return metadata[0]
