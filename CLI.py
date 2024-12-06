import os
from analyze import speechToTextOnWhisperModel
from download import Download
import convert as now_convert
import sys
import gc
import outputSubtitles 
import time as t
def get_file_name(input_file_path):
    return os.path.splitext(input_file_path)[0]


def initialize_output_result(analyze_result):
    return outputSubtitles.subtitles(analyze_result)
     

def initialize_audio_model(selected_option, count):
    process_audio = speechToTextOnWhisperModel()
    process_audio.offset = count * 300
    process_audio.setDeviceSetting('cuda')
    process_audio.setComputeTypeSetting('float16')
    process_audio.setModelSize(selected_option)
    process_audio.loadModel()
    return process_audio

def run_model(process_audio:speechToTextOnWhisperModel, filename, sel_lang_option):
    
    print("處理中...")
    language_methods = {
        "Chinese": process_audio.run_model_with_chinese,
        "English": process_audio.run_model_with_english,
        "Japanese": process_audio.run_model_with_japanese,
        "Auto": process_audio.runModel
    }
    method = language_methods.get(sel_lang_option)
    if method:
        method(filename)
    else:
        raise ValueError(f"未支援的語言選項: {sel_lang_option}")
    return process_audio.get_result()

def output_result(run_model_result,filename ,count,output_selected_option):
    result=initialize_output_result(run_model_result)
    print("輸出檔案中...")
    output_methods = {
        "txt": lambda: result.outputTxt(get_file_name(filename) + ".txt", count),
        "srt": lambda: result.outputSrt(get_file_name(filename) + ".srt", count)
    }
    method = output_methods.get(output_selected_option)
    if method:
        method()
    else:
        raise ValueError(f"未支援的輸出選項: {output_selected_option}")
    print("完成處理")

def handle_online_input(input_text, selected_option, output_selected_option, sel_lang_option):
    download = Download(input_text, "./")
    time = download.get_time_info()
    
    count = 0
    if time > 300:
        print("影片長度超過5分鐘，分段下載")
        for i in range(0, time, 300):
            print(f"下載第 {count + 1} 段中...")
            filename = download.download_section_m4a(i, i + 300)
            wav_name = convert_to_wav(filename)
            analyze_model=initialize_audio_model( selected_option, count)
            run_model_result=run_model(analyze_model, wav_name, sel_lang_option)
            output_result(run_model_result,wav_name ,count,output_selected_option)
            count += 1
    else:
        print("下載中...")
        filename = download.download_m4a()
        wav_name = convert_to_wav(filename)
        analyze_model=initialize_audio_model(selected_option, count)
        run_model_result=run_model(analyze_model, wav_name, sel_lang_option)
        output_result(run_model_result,wav_name ,count,output_selected_option)
        print("處理完成，返回主選單")
        
        

def convert_to_wav(filename):
    print("轉換格式中...")
    need_process = now_convert.VideoConvert(filename, "./")
    new_name = need_process.m4a_convert_to_wav()
    os.remove(filename)
    return new_name

def process_local_file(input_text:str, selected_option, output_selected_option, sel_lang_option):
    need_process = now_convert.VideoConvert(input_text, "")
    cleaned_input = input_text.strip('"')
    file_extension = cleaned_input.split('.')[-1]
    if input_text.endswith('wav'):
        wav_name = input_text
    else:
        conversion_methods = {
            'mp3': need_process.local_mp3_convert_to_wav,
            'mp4': need_process.local_mp4_convert_to_wav,
            'm4a': need_process.m4a_convert_to_wav
        }
        method = conversion_methods.get(file_extension)
        if method:
            wav_name = method()
        else:
            raise ValueError("無法處理的本地檔案格式")
    count = 0
    #還有超過五分鐘的處理方法未添加
    analyze_model=initialize_audio_model( selected_option, count)
    run_model_result=run_model(analyze_model, wav_name, sel_lang_option)
    output_result(run_model_result,wav_name ,count,output_selected_option)
    print("處理完成，返回主選單")
    


def main():
    # 在主函數中創建 process_audio 實例
    
    
    while True:
        
        print("\n主選單:")
        print("1. 分析影片/音訊")
        print("2. 離開")
        choice = input("請選擇 (1 或 2): ")

        if choice == '1':
            print("歡迎使用語音轉文字系統")
            input_text = input("請輸入影片網址或本地檔案路徑: ")

            # 選擇模型大小
            model_options = ["small", "medium",  "large-v2"]
            print("請選擇模型大小:")
            for idx, option in enumerate(model_options, 1):
                print(f"{idx}. {option}")
            selected_option_index = int(input("輸入選項編號 (默認為 3): ") or 3) - 1
            selected_option = model_options[selected_option_index]
        
            # 選擇語言
            lang_options = ["Auto", "Chinese", "English", "Japanese"]
            print("請選擇語言:")
            for idx, option in enumerate(lang_options, 1):
                print(f"{idx}. {option}")
            sel_lang_option_index = int(input("輸入選項編號 (默認為 1): ") or 1) - 1
            sel_lang_option = lang_options[sel_lang_option_index]

            # 選擇輸出格式
            output_options = ["txt", "srt"]
            print("請選擇輸出格式:")
            for idx, option in enumerate(output_options, 1):
                print(f"{idx}. {option}")
            output_selected_option_index = int(input("輸入選項編號 (默認為 2): ") or 2) - 1
            output_selected_option = output_options[output_selected_option_index]
            
            try:
                if input_text.startswith("https"):
                    try:
                       
                        
                        handle_online_input(input_text, selected_option, output_selected_option, sel_lang_option)
                        
                    except Exception as e:
                        print(f"處理過程中發生錯誤: {str(e)}")
                        with open("error_log.txt", "a") as log_file:
                            log_file.write(f"Process Error: {str(e)}\n")
                else:
                    
                    process_local_file(input_text, selected_option, output_selected_option, sel_lang_option)


            except Exception as e:
                print(f"發生錯誤: {str(e)}")
                with open("error_log.txt", "a") as log_file:
                    log_file.write(f"Error: {str(e)}\n")
        elif choice == '2':
            print("再見！")
            sys.exit(0)
        else:
            print("無效的選項，請重新選擇。")
        
        

      
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序遇到未處理的異常：{e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Unhandled Exception: {e}\n")
