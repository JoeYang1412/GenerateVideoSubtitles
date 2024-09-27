from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
class VideoConvert:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        
    # 將 mp4 轉換成 wav
    def local_mp4_convert_to_wav(self):
        
        self.final_output_path = self.output_path + self.input_path[:-4]+'.wav'
        
        video = VideoFileClip(self.input_path)
        video.audio.write_audiofile(self.final_output_path)
        return self.final_output_path
        
    def local_mp3_convert_to_wav(self):
        # 將 mp3 轉換成 wav
        self.final_output_path = self.output_path + self.input_path[:-4]+'.wav'
        audio = AudioFileClip(self.input_path)
        audio.write_audiofile(self.final_output_path)
        return self.final_output_path
    
    def m4a_convert_to_wav(self):
        # 將 m4a 轉換成 wav
        if self.input_path[-3:] == 'wav':
            return "已經是wav檔案"
        
        self.final_output_path = self.output_path + self.input_path[:-4]+'.wav'
        audio=AudioFileClip(self.input_path)
        audio.write_audiofile(self.final_output_path)
        return self.final_output_path
    
