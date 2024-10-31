import sys
from analyze import speechToTextOnWhisperModel
from download import Download
import convert as now_convert
import os

def main():
    if len(sys.argv) == 2:
        input_text = sys.argv[1]
        if input_text.startswith("https"):
            print("Downloading and processing the audio file from the URL...")
            count = 0
            need_download = Download(input_text,"./")
            filename=need_download.download_m4a()
            need_process=now_convert.VideoConvert(filename, "./")
            filename=need_process.m4a_convert_to_wav()
            process_audio = speechToTextOnWhisperModel()
            process_audio.setDeviceSetting('cuda')
            process_audio.setComputeTypeSetting('float16')
            process_audio.setModelSize('large-v2')
            process_audio.runModel(filename)
            process_audio.outputSrt("./result.srt",count)
            print("Done")
    else:
        print("Please provide a valid URL")
    return 0      

if __name__ == "__main__":
    main()

        
        