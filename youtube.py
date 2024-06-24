from yt_dlp import YoutubeDL
import re
import os

def get_vid(url):
    pattern = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)?/|.*[?&]v=)|youtu\.be/|youtube.com/user/[^#]*#([^/]+/)*([^/]+))([^"&?/\s]{11})')
    match = pattern.search(url)

    return match.group(3) if match else url

def get_info(v):
    try:
        print("getinfo")
        opts = {
            'quiet': True,
            'skip_download': True,
        }

        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(v, download=False)
            dur = info.get('duration', None)
            formats = info.get('formats', [])

        res = []
        for format in formats:
            if format['ext'] == 'mp4' or format['ext'] =='webm':
                if 'vcodec' in format:
                    if format['vcodec'] != 'none':
                        height = format['height']
                        # size = format['filesize_approx']
                        if height not in res:
                            res.append(height)

        res = sorted(res)

        return {
            'res': res,
            'dur': dur
        }

    except Exception as e:
        print(e)

def getFile(v, res, db):
    try:
        opts = {'extract_flat': 'discard_in_playlist',
                'outtmpl': os.path.join("download", f'{v}-{res}.mp4'),
                'preferedformat': 'mp4',
                'format': 'bv*+ba/b',
                'format_sort': [f'res:{res}', 'ext:mp4:m4a'],
                'fragment_retries': 10,
                'ignoreerrors': 'only_download',
                'postprocessors': [{'key': 'FFmpegConcat',
                                    'only_multi_video': True,
                                    'when': 'playlist'
                                    }],
                'retries': 10,
                'merge_output_format': 'mp4'
        }

        db.add(v, res, 0)
        with YoutubeDL(opts) as ydl:
            ydl.download(v)
        db.add(v, res, 1)

    except Exception as e:
        print(e)