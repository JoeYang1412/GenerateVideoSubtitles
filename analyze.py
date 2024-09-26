from faster_whisper import WhisperModel
import pysrt
import time_process
import opencc
class speechToTextOnWhisperModel:
    
    def __init__(self,  device_setting="cuda", compute_type_setting="float16"):
        self.device = device_setting
        self.compute_type = compute_type_setting
        

    def setModelSize(self, model_size_input):
        self.model_size = model_size_input

    def setDeviceSetting(self, device_setting):
        self.device = device_setting

    def setComputeTypeSetting(self, compute_type_setting):
        self.compute_type = compute_type_setting


    def runModel(self, input_audio):
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5)

    def outputTxt(self, output_text_file):
        with open(output_text_file, 'w') as f:
            for segment in self.segments:
                f.write("[%.2fs -> %.2fs] %s \n" % (segment.start, segment.end, segment.text))
    
    
    def outputSrt(self, output_srt_file):
        srt = pysrt.SubRipFile()
        for i, segment in enumerate(self.segments):
            start = time_process.time_process(segment.start).process()
            end = time_process.time_process(segment.end).process()
            srt.append(pysrt.SubRipItem(index=i,start=start ,end=end , text=self.outputTraditionalTxt(segment.text)))
        srt.save(output_srt_file)


    def outputTraditionalTxt(self, simplified_text):
        converter = opencc.OpenCC('s2t')
        traditional_text = converter.convert(simplified_text)
        return traditional_text