import numpy as np
from PIL import Image


def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    if (
        image_size[0] // tile_size[0] * image_size[1] // tile_size[1] == len(ordering)
        and not image_size[0] % tile_size[0]
        and not image_size[1] % tile_size[1]
        and len(ordering) == len(set(ordering))
    ):
        return True
    return False


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    with Image.open(image_path) as img:
        arr = np.asarray(img)

    if not valid_input(img.size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    vertical = img.height // tile_size[0]
    horizontal = img.width // tile_size[1]
    tiles = []

    for v in range(vertical):
        for h in range(horizontal):
            tiles.append(
                arr[
                    tile_size[1] * v : min(tile_size[1] * v + tile_size[1], img.height),
                    tile_size[0] * h : min(tile_size[0] * h + tile_size[0], img.width),
                ]
            )

    new_order = []
    for order in ordering:
        new_order.append(tiles[int(order)])

    new_img = Image.new(img.mode, img.size)
    x = 0

    for v in range(vertical):
        for h in range(horizontal):
            tile = Image.fromarray(new_order[x])
            new_img.paste(tile, (tile_size[0] * h, tile_size[1] * v))
            x += 1

    new_img.save(out_path)


if __name__ == "__main__":
    with open(
        "qualifiers/Code Jam 10/qualifier/images/pydis_logo_order.txt", "r", newline="", encoding="utf-8"
    ) as file:
        order = file.readlines()

    rearrange_tiles(
        "qualifiers/Code Jam 10/qualifier/images/pydis_logo_scrambled.png", (256, 256), order, "images/user_output.png"
    )
