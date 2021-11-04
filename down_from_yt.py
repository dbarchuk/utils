"""
Needed packages:
pytube
requests
awesome-slugify
"""

from pytube import YouTube
import os
from slugify import slugify
import requests
from dotenv import load_dotenv

# Загружаем в переменные PATH_TO_SAVE_FILE для сохранения в другую папку
load_dotenv('.env')

def get_video_from_yt(url: str, filename=None):

    video_url = url
    path_to_save = os.environ.get('PATH_TO_SAVE_FILE', 'downloads/')
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    yt = YouTube(video_url)

    if not filename:
        filename = slugify(yt.title[:100]).lower() + '.mp4'
    else:
        filename += '.mp4'

    # processing thumbs
    thumb_url = yt.thumbnail_url
    thumb_format = thumb_url.split('/')[-1].split('.')[-1]
    thumb_name = filename.split('.')[0] + '.' + thumb_format
    r = requests.get(thumb_url, allow_redirects=True)
    with open(f'{path_to_save}/{thumb_name}', 'wb') as f:
        f.write(r.content)

    try:
        yt = yt.streams.filter(
            progressive=True,
            file_extension='mp4').order_by('resolution').last()
        res = yt.resolution
        print(f'saving file in {res}')
        yt.download(path_to_save, filename)
        print(filename)
        return "ok"
    except BaseException as e:
        print(e)
    finally:
        print('successfully done')


if __name__ == '__main__':
    url = str(input('Enter Youtube url> '))
    filename = str(input(
        'Enter filename for tube (optional)> ')
    )
    get_video_from_yt(url, filename)
