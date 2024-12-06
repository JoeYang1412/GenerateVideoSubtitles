import yt_dlp
from yt_dlp.utils import download_range_func
import re
class Download:
    def __init__(self, url, output_path):
        self.url = url
        self.output_path = output_path
        self.fixed_filename = self.remove_special_characters(url.split('=')[-1])
    
    #移除特殊字元    
    def remove_special_characters(self, filename):
        # 使用Regular Expression移除非英文及數字的字元
        # remove non-alphanumeric characters using Regular Expression
        return re.sub(r'[^a-zA-Z0-9]', '', filename)
        
    # 下載 m4a 檔案
    # download m4a file
    def download_m4a(self):

        # options
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/best[ext=m4a]',
            'outtmpl': f'{self.output_path}/{self.fixed_filename}.%(ext)s',  
            'postprocessors': [],  # 不使用任何後處理器
            'nooverwrites': False,  # 覆蓋已存在的檔案
        }
        # download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            info = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info)
            
            return filename
    # download m4a file by section
    def download_section_m4a(self, start_time, end_time):
        # options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.output_path}/{self.fixed_filename}.%(ext)s', 
            'postprocessors': [],  # 不使用任何後處理器
            'nooverwrites': False,  # 覆蓋已存在的檔案
            'download_ranges': download_range_func(None, [(start_time, end_time)]),
            'force_keyframes_at_cuts': True,
        }
        # download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            info = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info)
            
            return filename
    # get time info
    def get_time_info(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.output_path}/{self.fixed_filename}.%(ext)s', 
            'postprocessors': [],  # 不使用任何後處理器
            'nooverwrites': False,  # 覆蓋已存在的檔案
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            info = ydl.extract_info(self.url, download=False)
            return info['duration'] 

