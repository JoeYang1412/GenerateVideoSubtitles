import argparse
from analyze import speechToTextOnWhisperModel
from download import Download
import convert as now_convert

def main():
    parser = argparse.ArgumentParser(description="下載並處理音訊文件")
    parser.add_argument('input_text', type=str, help='輸入的網址或是檔案路徑，需使用\"\"包起來')
    parser.add_argument('--model_size', type=str, default='large-v2', help='選擇的模型大小')
    parser.add_argument('--device', type=str, default='cuda', help='設備設置，例如 cuda 或 cpu')
    parser.add_argument('--compute_type', type=str, default='float16', help='計算型態設置，例如 float16 或 float32')
    parser.add_argument('--language', type=str, default='auto', help='選擇語言，例如 auto, zh, en, ja')
    parser.add_argument('--output', type=str, default="output.srt", help='指定輸出文件名')
    args = parser.parse_args()

    model_size = args.model_size
    if model_size not in ['small', 'medium', 'large', 'large-v2', 'large-v3']:
        print("Invalid model size. Please provide a valid model size.")
        return False

    device = args.device
    if device not in ['cuda', 'cpu']:
        print("Invalid device. Please provide a valid device.")
        return False
    
    compute_type = args.compute_type
    language = args.language
    input_text = args.input_text
    output_file = args.output

    count = 0  # 定義計數變量

    if input_text.startswith("https"):
        print("Downloading and processing the audio file from the URL...")
        
        try:
            # 下載和處理音訊
            downloader = Download(input_text, "./")
            filename = downloader.download_m4a()
            converter = now_convert.VideoConvert(filename, "./")
            filename = converter.m4a_convert_to_wav()
        except Exception as e:
            print(f"Error during download or conversion: {e}")
            return False

        # 設置模型參數並處理音訊
        try:
            process_audio = speechToTextOnWhisperModel()
            process_audio.setDeviceSetting(device)
            process_audio.setComputeTypeSetting(compute_type)
            process_audio.setModelSize(model_size)

            # 根據語言設置選擇模型方法
            if language == "zh":
                process_audio.run_model_with_chinese(filename)
            elif language == "en":
                process_audio.run_model_with_english(filename)
            elif language == "ja":
                process_audio.run_model_with_japanese(filename)
            elif language == "auto":
                process_audio.runModel(filename)
            else:
                print("Invalid language. Please provide a valid language.")
                return False

            # 輸出結果
            process_audio.outputSrt(output_file, count)
            return True
        except Exception as e:
            print(f"Error during audio processing: {e}")
            return False
    else:
        print("Invalid input. Please provide a valid URL.")
        return False

if __name__ == "__main__":
    result = main()
    if result:
        print("Process completed.")
    else:
        print("Process failed.")
