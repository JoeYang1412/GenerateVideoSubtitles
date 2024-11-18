from faster_whisper import WhisperModel
import pysrt
import time_process
import time
import opencc
import torch
import gc
class speechToTextOnWhisperModel:
    # offset is the time offset in seconds，process long audio in segments
    offset = 0.0
    def __init__(self):
        self.offset = 0.0
        self.model_size = None
        self.device = None
        self.compute_type = None
        self.model = None
        self.current_model_size = None
        
    # set model size
    def setModelSize(self, model_size_input):
        self.model_size = model_size_input
    # set device setting
    def setDeviceSetting(self, device_setting):
        self.device = device_setting
    # set compute type setting
    def setComputeTypeSetting(self, compute_type_setting):
        self.compute_type = compute_type_setting

    def loadModel(self):
        if self.model is None:
            # 在重新加載模型前，釋放舊模型的資源
            print("加載模型中...")
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            self.current_model_size = self.model_size  # 更新已加載的模型大小
            print("模型加載完成。")
        else:
            # 如果模型大小未更改，則不重新加載模型
            if self.current_model_size == self.model_size:
                print("模型已加載，無需再次加載。")
            else:
                print("重新加載模型中...")
                del self.model
                gc.collect()
                self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
                self.current_model_size = self.model_size
                print("模型加載完成。")
        

    # run model
    def runModel(self, input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5)

    def run_model_with_chinese(self,input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="zh")

    def run_model_with_english(self,input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="en")  
          
    def run_model_with_japanese(self,input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="ja")
    
    # output file type is txt
    def outputTxt(self, output_text_file,count):
        # count is the number of times the function is called
        # if count is 0, create a new file
        # if count is not 0, append to the existing file
        if count == 0:
            with open(output_text_file, 'w', encoding='utf-8') as f:
                for segment in self.segments:
                    start = time_process.time_process(segment.start+self.offset).process()
                    end = time_process.time_process(segment.end+self.offset).process()
                    f.write(f"[{start} -> {end}] {self.outputTraditionalTxt(segment.text)}\n")
        else:
            with open(output_text_file, 'a', encoding='utf-8') as f:
                for segment in self.segments:
                    start = time_process.time_process(segment.start+self.offset).process()
                    end = time_process.time_process(segment.end+self.offset).process()
                    f.write(f"[{start} -> {end}] {self.outputTraditionalTxt(segment.text)}\n")
        
    # output file type is srt
    def outputSrt(self, output_srt_file, count):
        mode = 'w' if count == 0 else 'a'
        with open(output_srt_file, mode, encoding='utf-8') as f:
            for i, segment in enumerate(self.segments, start=1):
                start = time_process.time_process(segment.start + self.offset).process()
                end = time_process.time_process(segment.end + self.offset).process()
                text = self.outputTraditionalTxt(segment.text)
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


    # output simplified chines to traditional chinese
    def outputTraditionalTxt(self, simplified_text):
        converter = opencc.OpenCC('s2t')
        traditional_text = converter.convert(simplified_text)
        return traditional_text
    
