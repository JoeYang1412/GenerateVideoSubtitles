import pysrt
import time_process
import time
import opencc
import torch
import gc

class subtitles:
    def __init__(self,analyze_result):
        self.segments = analyze_result
        self.offset = 0.0

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
                    self.offset = count * 300
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
            self.offset = count * 300
            start = time_process.time_process(segment.start+self.offset).process()
            end = time_process.time_process(segment.end+self.offset).process()
            srt.append(pysrt.SubRipItem(index=i, start=start, end=end, text=self.outputTraditionalTxt(segment.text)))

        srt.save(output_srt_file, encoding='utf-8')


    # output simplified chines to traditional chinese
    def outputTraditionalTxt(self, simplified_text):
        converter = opencc.OpenCC('s2t')
        traditional_text = converter.convert(simplified_text)
        return traditional_text