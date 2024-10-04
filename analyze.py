from faster_whisper import WhisperModel
import pysrt
import time_process
import opencc

class speechToTextOnWhisperModel:
    # offset is the time offset in seconds，process long audio in segments
    offset = 0.0
    def __init__(self,  device_setting="cuda", compute_type_setting="float16"):
        self.device = device_setting
        self.compute_type = compute_type_setting
        
    # set model size
    def setModelSize(self, model_size_input):
        self.model_size = model_size_input
    # set device setting
    def setDeviceSetting(self, device_setting):
        self.device = device_setting
    # set compute type setting
    def setComputeTypeSetting(self, compute_type_setting):
        self.compute_type = compute_type_setting

    # run model
    def runModel(self, input_audio):
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5)

    def run_model_with_chinese(self,input_audio):
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="zh")

    def run_model_with_english(self,input_audio):
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="en")  
          
    def run_model_with_japanese(self,input_audio):
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
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
    def outputSrt(self, output_srt_file,count):
        # count is the number of times the function is called
        # if count is 0, create a new file
        # if count is not 0, append to the existing file
        if count == 0:
            srt = pysrt.SubRipFile()
        else:
            try:
                srt = pysrt.open(output_srt_file, encoding='utf-8')
            except FileNotFoundError:
                srt = pysrt.SubRipFile()

        for i, segment in enumerate(self.segments, start=len(srt) + 1):
            start = time_process.time_process(segment.start+self.offset).process()
            end = time_process.time_process(segment.end+self.offset).process()
            srt.append(pysrt.SubRipItem(index=i, start=start, end=end, text=self.outputTraditionalTxt(segment.text)))

        srt.save(output_srt_file, encoding='utf-8')

    # output simplified chines to traditional chinese
    def outputTraditionalTxt(self, simplified_text):
        converter = opencc.OpenCC('s2t')
        traditional_text = converter.convert(simplified_text)
        return traditional_text
    
