import requests
import yt_dlp

from .step import Step


# from .step import StepException

class DownloadCaptions(Step):
    def process(self, data, inputs):
        for url in data:
            # 你要下載的YouTube影片網址
            video_url = url

            # 設定下載選項
            ydl_opts = {
                'skip_download': True,  # 不下載影片，只提取字幕
                'subtitleslangs': ['en'],  # 設定要提取的字幕語言
                'writesubtitles': True,  # 啟用字幕下載
                'writeautomaticsub': True,  # 啟用自動生成字幕下載（如果沒有手動字幕）
                'subtitlesformat': 'srt',  # 設定字幕格式為 srt
                'outtmpl': '%(id)s.%(ext)s',  # 設定輸出的文件模板
            }

            # 使用 yt-dlp 下載字幕
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                subtitles = info_dict.get('requested_subtitles')

            # 檢查是否有自動生成字幕或手動字幕
            if subtitles and 'en' in subtitles:
                en_subtitle_url = subtitles['en']['url']
                response = requests.get(en_subtitle_url)
                en_caption_convert_to_srt = response.content.decode('utf-8')
            else:
                en_caption_convert_to_srt = 'NONE'

            # 輸出字幕內容到 Output.txt
            with open("Output.txt", "w", encoding='utf-8') as text_file:
                text_file.write(en_caption_convert_to_srt)

            print(en_caption_convert_to_srt)

            break
