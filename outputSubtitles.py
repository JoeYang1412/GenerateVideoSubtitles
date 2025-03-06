import pysrt
import time_process
import opencc
class subtitles:
    """
    A class to output the subtitles in txt or srt format.
    Attributes:
        segments (list): A list of segments with the start time, end time, and text.

    Methods:
        outputTxt(output_text_file): Output the subtitles in txt format.
        outputSrt(output_srt_file): Output the subtitles in srt format.
        outputTraditionalTxt(simplified_text): Convert simplified Chinese to traditional Chinese.
    """

    def __init__(self,analyze_result):
        self.segments = analyze_result

    def outputTxt(self, output_text_file):
        # Output the subtitles in txt format
        # The format is [start time -> end time] text
        # .process() is used to convert the time to the correct format
        # The text is converted to traditional Chinese using OpenCC
        with open(output_text_file, 'w', encoding='utf-8') as f:
            for segment in self.segments:
                start = time_process.time_process(segment.start).process()
                end = time_process.time_process(segment.end).process()
                f.write(f"[{start} -> {end}] {self.outputTraditionalTxt(segment.text)}\n")
    
    def onlyTxt(self, output_text_file):
        # Output the subtitles in txt format
        # The text is converted to traditional Chinese using OpenCC
        # only text，no start time and end time
        with open(output_text_file, 'w', encoding='utf-8') as f:
            for segment in self.segments:
                f.write(f"{self.outputTraditionalTxt(segment.text)}\n")
        

    def outputSrt(self, output_srt_file):
        # Output the subtitles in srt format
        # create a new srt file and append each segment to the file
        # .process() is used to convert the time to the correct format
        # The text is converted to traditional Chinese using OpenCC
        srt = pysrt.SubRipFile()
        for i, segment in enumerate(self.segments, start=len(srt) + 1):
            
            start = time_process.time_process(segment.start).process()
            end = time_process.time_process(segment.end).process()
            srt.append(pysrt.SubRipItem(index=i, start=start, end=end, text=self.outputTraditionalTxt(segment.text)))
        # Save the srt file
        srt.save(output_srt_file, encoding='utf-8')


    def outputTraditionalTxt(self, simplified_text):
        # Convert simplified Chinese to traditional Chinese
        converter = opencc.OpenCC('s2t')
        traditional_text = converter.convert(simplified_text)
        return traditional_text