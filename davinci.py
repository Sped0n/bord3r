from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.Image import Image as PILImage
from PIL.ImageDraw import ImageDraw as PILDraw

from exif import ExifDict, get_exif


class Davinci:
    def __init__(self, filepath: str, location: str | None = None) -> None:
        # location of the image (e.g. "Paris")
        self.__location: str = location if location is not None else "N/A"
        # image and exif data
        self.__img: PILImage = Image.open(filepath)
        self.__exif: ExifDict = get_exif(filepath)
        # original width and height of the image
        self.__original_width: int
        self.__original_height: int
        # if we met vertically postioned pic, we rotate it
        # and treat it like hortizontal pic, after all process,
        # we rotate it back
        if self.__img.size[0] >= self.__img.size[1]:
            self.__vertical: bool = False
        else:
            self.__vertical = True
            self.__img = self.__img.rotate(-90, expand=True)
        self.__original_width, self.__original_height = self.__img.size
        # short and long side of the image
        # since we will always get a hortizontal pisitioned pic (width > length)
        # we can just assume long side is w, short side is h
        self.__long_side: int = self.__original_width
        self.__short_side: int = self.__original_height
        # half side length of the expanded square, used as a scale for watermark
        self.__hsl = int((self.__long_side + 0.15 * self.__short_side) / 2)
        # hortizontal and vertical fill
        hor_fill: int = int(self.__hsl - self.__original_width / 2)
        ver_fill: int = int(self.__hsl - self.__original_height / 2)
        # border
        self.__border: tuple[int, int, int, int] = (
            hor_fill,
            ver_fill,
            hor_fill,
            ver_fill,
        )
        # expanded image
        self.__plate: PILImage = ImageOps.expand(
            self.__img, border=self.__border, fill="white"
        )
        # PIL draw object
        self.__draw: PILDraw = ImageDraw.Draw(self.__plate)
        # fonts
        self.__font_size: int = int(0.04 * self.__hsl)
        self.__font = ImageFont.truetype("./fonts/Geist-Medium.ttf", self.__font_size)

    def __add_capture_time(self) -> None:
        # capture time, on top left corner
        text: str = str(self.__exif["EXIF:CreateDate"])
        x: int = int(self.__hsl - self.__original_width / 2)
        y: int = int(self.__hsl - self.__original_height / 2 - 0.018 * self.__hsl)
        self.__draw.text((x, y), text, anchor="lb", font=self.__font, fill="black")  # pyright: ignore[reportUnknownMemberType]

    def __add_location(self) -> None:
        # location, on top right corner
        text: str = self.__location
        x: int = int(self.__hsl + self.__original_width / 2)
        y: int = int(self.__hsl - self.__original_height / 2 - 0.015 * self.__hsl)
        self.__draw.text((x, y), text, anchor="rb", font=self.__font, fill="black")  # pyright: ignore[reportUnknownMemberType]

    def __add_camera_model(self) -> None:
        # camera model, on bottom left corner row 1
        text: str = str(self.__exif["EXIF:Make"]) + " " + str(self.__exif["EXIF:Model"])
        x: int = int(self.__hsl - self.__original_width / 2)
        y: int = int(self.__hsl + self.__original_height / 2 + 0.018 * self.__hsl)
        self.__draw.text((x, y), text, anchor="lt", font=self.__font, fill="black")  # pyright: ignore[reportUnknownMemberType]

    def __add_artist(self) -> None:
        # artist, on bottom right corner
        try:
            text = str(self.__exif["EXIF:Artist"])
        except KeyError:
            text = "@sped0n"
        x = int(self.__hsl + self.__original_width / 2 - 0.007 * self.__hsl)
        y: int = int(self.__hsl + self.__original_height / 2 + 0.016 * self.__hsl)
        self.__draw.text((x, y), text, anchor="rt", font=self.__font, fill="black")  # pyright: ignore[reportUnknownMemberType]

    def process(self) -> PILImage:
        self.__add_capture_time()
        self.__add_location()
        self.__add_camera_model()
        self.__add_artist()
        if self.__vertical:
            return self.__plate.rotate(90, expand=True)
        return self.__plate
