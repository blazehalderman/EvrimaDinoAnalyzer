import yt_dlp
ydl = yt_dlp.YoutubeDL({'quiet': True})
info = ydl.extract_info('https://www.youtube.com/watch?v=rNVGFXtD8BM', download=False)
chapters = info.get('chapters') or []
for c in chapters:
    print(str(int(c['start_time'])).rjust(4) + 's - ' + c['title'])
