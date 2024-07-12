from typing import TypeAlias

import exiftool  # pyright: ignore[reportMissingTypeStubs]

ExifDict: TypeAlias = dict[str, str | int | float]


def get_exif(path: str) -> ExifDict:
    with exiftool.ExifToolHelper() as et:
        metadata: list[ExifDict] = et.get_metadata(path)  # pyright: ignore[reportUnknownMemberType]
        return metadata[0]
