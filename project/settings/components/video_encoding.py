VIDEO_ENCODING_FORMATS = {
    'FFmpeg': [
        {
            'name': 'webm',
            'extension': 'webm',
            'params': [
                '-b:v', '1000k', '-maxrate', '1000k', '-bufsize', '2000k',
                '-codec:v', 'libvpx', '-r', '30',
                '-vf', 'scale=640:360', '-qmin', '10', '-qmax', '42',
                '-codec:a', 'libvorbis', '-b:a', '128k', '-f', 'webm',
            ],
        },
        {
            'name': 'mp4',
            'extension': 'mp4',
            'params': [
                '-codec:v', 'libx264', '-crf', '20', '-preset', 'medium', '-b:v',
                '1000k', '-maxrate', '1000k', '-bufsize', '2000k', '-vf', 'scale=640:360',
                '-codec:a', 'aac', '-b:a', '128k', '-strict', '-2',
            ],
        },
    ]
}
