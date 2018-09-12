import logging
import os
from collections import namedtuple
from glob import glob
from logging.handlers import RotatingFileHandler

from flask import (
    Flask,
    jsonify,
    abort,
    url_for,
    send_from_directory
)

app = Flask(__name__)

WALLPAPERS_PATH = 'media/wallpapers'
MEDIA_FOLDER = 'media'


def _get_categories():
    """
    Search for directories in wallpapers dir.
    Skip files and other garbage.
    :rtype: list
    """
    try:
        directories = set()
        for path in os.listdir(WALLPAPERS_PATH):
            full_path = os.path.join(WALLPAPERS_PATH, path)
            if os.path.isdir(full_path):
                directories.add(path)
    except (OSError, IOError):
        logging.exception("Unable to get list of folders "
                          "in directory, check logs for details")
        return abort(500, "Internal server error, check logs for details")
    return list(directories)


def _get_wallpapers_for_category(category):
    """
    Get list of VALID wallpapers in directory
    :type category: str
    :rtype: list[Wallpaper]
    """
    Wallpaper = namedtuple('Wallpaper', ('image', 'video'))

    category_path = os.path.join(WALLPAPERS_PATH, category)
    images = os.path.join(category_path, '*.jpg')
    contents = glob(images, recursive=False)

    wallpapers = []
    for image_path in contents:
        # '/path/to/image.jpg' -> 'image'
        filename = os.path.basename(image_path).rsplit('.', 1)[0]
        video_path = os.path.join(category_path, filename + '.mov')
        if not os.path.isfile(video_path):
            logging.warning("%s exists, but no video pair %s", image_path, video_path)
            continue
        wallpapers.append(Wallpaper(
            image=os.path.relpath(image_path, 'media'),
            video=os.path.relpath(video_path, 'media')
        ))
    return wallpapers


@app.route('/wallpapers/', methods=['GET'])
def get_categories():
    categories = []
    for dir_ in _get_categories():
        categories.append({
            'name': dir_,
            'url': url_for('get_wallpapers', category=dir_, _external=True)
        })

    return jsonify({
        'status': 'ok',
        'categories': categories
    })


@app.route('/wallpapers/<category>/', methods=['GET'])
def get_wallpapers(category):
    available = _get_categories()
    # in order to filter path's like '../securedir' or '//etc/passwd'
    if category not in available:
        return abort(400, "Unknown wallpapers category")

    wallpapers = []
    for wallpaper in _get_wallpapers_for_category(category):
        wallpapers.append({
            'image_url': url_for('download_file', filename=wallpaper.image, _external=True),
            'video_url': url_for('download_file', filename=wallpaper.video, _external=True),
        })

    return jsonify({
        'status': 'ok',
        'wallpapers': wallpapers
    })


@app.route('/media/<path:filename>')
def download_file(filename):
    """Only for easy url reverse in debug mode"""
    raise NotImplementedError("use nginx instead")


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=1024 ** 2, backupCount=2)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
