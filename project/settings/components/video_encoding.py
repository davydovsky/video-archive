from project.settings.components import config

VIDEO_WIDTH = config('VIDEO_WIDTH', cast=int, default=640)
VIDEO_HEIGHT = config('VIDEO_HEIGHT', cast=int, default=360)
VIDEO_SCALE = f'{VIDEO_WIDTH}:{VIDEO_HEIGHT}'

VIDEO_MAX_UPLOAD_SIZE = config('VIDEO_HEIGHT', cast=int, default=10485760)

VIDEO_ENCODING_BACKEND = 'project.apps.video_archive.encoding_backends.VideoEncodingBackend'
VIDEO_ENCODING_FORMATS = {
    'FFmpeg': [
        {
            'name': 'webm',
            'extension': 'webm',
            'params': [
                '-b:v', '1000k', '-maxrate', '1000k', '-bufsize', '2000k',
                '-codec:v', 'libvpx', '-r', '30',
                '-vf', f'scale={VIDEO_SCALE}', '-qmin', '10', '-qmax', '42',
                '-codec:a', 'libvorbis', '-b:a', '128k', '-f', 'webm',
            ],
        },
        {
            'name': 'mp4',
            'extension': 'mp4',
            'params': [
                '-codec:v', 'libx264', '-crf', '20', '-preset', 'medium', '-b:v',
                '1000k', '-maxrate', '1000k', '-bufsize', '2000k', '-vf', f'scale={VIDEO_SCALE}',
                '-codec:a', 'aac', '-b:a', '128k', '-strict', '-2',
            ],
        },

    ]
}
