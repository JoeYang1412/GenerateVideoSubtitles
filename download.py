import yt_dlp
from yt_dlp.utils import download_range_func
class Download:
    def __init__(self, url, output_path):
        self.url = url
        self.output_path = output_path
        self.fixed_filename = url.split('=')[-1]
        

    def download_m4a(self):
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.output_path}/{self.fixed_filename}.%(ext)s',  
            'postprocessors': [],  # 不使用任何後處理器
            'nooverwrites': False,  # 覆蓋已存在的檔案
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            info = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info)
            
            return filename
        
    def download_section_m4a(self, start_time, end_time):
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.output_path}/{self.fixed_filename}.%(ext)s', 
            'postprocessors': [],  # 不使用任何後處理器
            'nooverwrites': False,  # 覆蓋已存在的檔案
            'download_ranges': download_range_func(None, [(start_time, end_time)]),
            'force_keyframes_at_cuts': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            info = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info)
            
            return filename
        
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

