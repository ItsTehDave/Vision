
import argparse
import io

from google.cloud import vision
from PIL import Image, ImageDraw
# [END imports]


def get_crop_hint(path):
    """Detect crop hints on a single image and return the first result."""
    vision_client = vision.Client()

    with io.open("cat.jpg", 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    # Return bounds for the first crop hint using an aspect ratio of 1.77.
    return image.detect_crop_hints({1.77})[0].bounds.vertices
    # [END get_crop_hint]


def draw_hint(image_file):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_hint]
    vects = get_crop_hint("cat.jpg")

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon([
        vects[0].x_coordinate, vects[0].y_coordinate,
        vects[1].x_coordinate, vects[1].y_coordinate,
        vects[2].x_coordinate, vects[2].y_coordinate,
        vects[3].x_coordinate, vects[3].y_coordinate], None, 'red')
    im.save('output-hint.jpg', 'JPEG')
    # [END draw_hint]


def crop_to_hint(image_file):
    """Crop the image using the hints in the vector list."""
    # [START crop_to_hint]
    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x_coordinate, vects[0].y_coordinate,
                  vects[2].x_coordinate - 1, vects[2].y_coordinate - 1])
    im2.save('output-crop.jpg', 'JPEG')
    # [END crop_to_hint]


if __name__ == '__main__':
    # [START run_crop]
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to crop.')
    parser.add_argument('mode', help='Set to "crop" or "draw".')
    args = parser.parse_args()

    parser = argparse.ArgumentParser()

    if args.mode == 'crop':
        crop_to_hint(args."cat.jpg")
    elif args.mode == 'draw':
        draw_hint(args.image_file)
    # [END run_crop]

