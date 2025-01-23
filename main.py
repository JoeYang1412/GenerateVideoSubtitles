import os
import sys
import torch
from analyze import speechToTextOnWhisperModel
from download import Download
import convert as now_convert
import outputSubtitles
import multiprocessing
from multiprocessing import Process, Manager
"""
Function:
    get_file_name(input_file_path): Get the file name without the extension.
    initialize_output_result(analyze_result): Initialize the output result.
    convert_to_wav(filename): Convert the file to wav format.
    run_model(filename, sel_lang_option, selected_option): Run the model.
    output_result(run_model_result, filename,output_selected_option): save the output result to a file.
    handle_online_input(input_text, selected_option, output_selected_option, sel_lang_option): process the online input.
    process_local_file(input_text: str, selected_option, output_selected_option, sel_lang_option): process the local file.
    main(): main function.
"""

def get_file_name(input_file_path):
    return os.path.splitext(input_file_path)[0]

def initialize_output_result(analyze_result):
    return outputSubtitles.subtitles(analyze_result)


def convert_to_wav(filename):
    print("轉換格式中...")
    need_process = now_convert.AudioConvert(filename, "./")
    new_name = need_process.convert_to_wav()
    os.remove(filename)
    return new_name

def run_model(filename, sel_lang_option, selected_option):
    
    with Manager() as manager:
        # Create a shared list to store the result
        return_list = manager.list()
        print("初始化...")
        processor = speechToTextOnWhisperModel()
        processor.setDeviceSetting('cuda')
        processor.setComputeTypeSetting('float16')
        processor.setModelSize(selected_option)

        # Create a new process to run the model
        # Why use multiprocessing, please refer to "why_use_multithread.txt"
        # args: the arguments passed to the function
        p = Process(target=processor.run_analyze, args=(filename, sel_lang_option, return_list))
        p.start()
        p.join()
        p.close()
        normal_list = list(return_list)
        return normal_list
    
def output_result(run_model_result, filename,output_selected_option):
    result = initialize_output_result(run_model_result)
    print("輸出檔案中...")
    output_methods = {
        "txt": lambda: result.outputTxt(get_file_name(filename) + ".txt"),
        "srt": lambda: result.outputSrt(get_file_name(filename) + ".srt")
    }
    method = output_methods.get(output_selected_option)
    if method:
        method()
    else:
        raise ValueError(f"未支援的輸出選項: {output_selected_option}")
    print("完成處理")


def process_online_input(input_text, selected_option, output_selected_option, sel_lang_option):
    """
    step 1: download the file
    step 2: convert the file to wav format
    step 3: run the model
    step 4: output the result to a file
    """
    download = Download(input_text, "./")
    print("下載中...")
    filename = download.download_m4a()
    wav_name = convert_to_wav(filename)
    run_model_result = run_model(wav_name, sel_lang_option, selected_option)
    output_result(run_model_result, wav_name, output_selected_option)
    print("處理完成，返回主選單")



def process_local_file(input_text: str, selected_option, output_selected_option, sel_lang_option):
    # cleaned_input means the input text without the double quotes
    cleaned_input = input_text.strip('"')
    need_process = now_convert.AudioConvert(cleaned_input, "./")
    # get the file extension
    file_extension = cleaned_input.split('.')[-1]
    if file_extension=="wav":
        wav_name = cleaned_input
    else:
        # convert the file to wav format
        conversion_methods = {
            'mp3': need_process.convert_to_wav,
            'mp4': need_process.convert_to_wav,
            'm4a': need_process.convert_to_wav
        }
        method = conversion_methods.get(file_extension)
        if method:
            wav_name = method()
        else:
            raise ValueError("無法處理的本地檔案格式")
    # run the model and output the result to a file
    run_model_result = run_model(wav_name, sel_lang_option, selected_option)
    output_result(run_model_result, wav_name, output_selected_option)
    print("處理完成，返回主選單")


def main():
    """
    Main function

    args:
        input_text: str: the input text. It can be a video URL or a local file path.
        selected_option: str: the selected model size.
        selected_option_index (int): the index of the selected model size.
        sel_lang_option: str: the selected language option.
        sel_lang_option_index (int): the index of the selected language option.
        output_selected_option: can be "txt" or "srt".
        output_selected_option_index (int): the index of the selected output option.
    steps:
        1. show the main menu
        2. get the user's choice
        3. if the user chooses 1
            3.1 get the input text
            3.2 get the selected model size
            3.3 get the selected language option
            3.4 get the output selected option
            3.5 if the input text is a URL
                3.5.1 download the file
                3.5.2 convert the file to wav format
                3.5.3 run the model
                3.5.4 output the result to a file
            3.6 if the input text is a local file path
                3.6.1 convert the file to wav format
                3.6.2 run the model
                3.6.3 output the result to a file
        4. if the user chooses 2, exit the program
    """

    # check if CUDA is available
    if torch.cuda.is_available():
        print("CUDA is available")
    else:
        print("CUDA is not available")
        exit()

    # show the main menu
    while True:
        print("\n主選單:")
        print("1. 分析影片/音訊")
        print("2. 離開")
        choice = input("請選擇 (1 或 2): ")
        if choice == '1':
            print("歡迎使用語音轉文字系統")
            input_text = input("請輸入影片網址或本地檔案路徑: ")

            model_options = ["tiny", "small", "medium", "large", "large-v2", "large-v3", "large-v3-turbo", "turbo"]
            print("請選擇模型大小:")
            for idx, option in enumerate(model_options, 1):
                print(f"{idx}. {option}")
            selected_option_index = int(input("輸入選項編號 (默認為 5): ") or 5) - 1
            selected_option = model_options[selected_option_index]


            lang_options = ["Auto", "Chinese", "English", "Japanese"]
            print("請選擇語言:")
            for idx, option in enumerate(lang_options, 1):
                print(f"{idx}. {option}")
            sel_lang_option_index = int(input("輸入選項編號 (默認為 1): ") or 1) - 1
            sel_lang_option = lang_options[sel_lang_option_index]


            output_options = ["txt", "srt"]
            print("請選擇輸出格式:")
            for idx, option in enumerate(output_options, 1):
                print(f"{idx}. {option}")
            output_selected_option_index = int(input("輸入選項編號 (默認為 2): ") or 2) - 1
            output_selected_option = output_options[output_selected_option_index]


            try:
                if input_text.startswith("https"):
                    try:
                        process_online_input(input_text, selected_option, output_selected_option, sel_lang_option)
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
        # Resolve the issue where multiprocessing does not work after packaging with pyinstaller
        multiprocessing.freeze_support()
        main()
    except Exception as e:
        print(f"程序遇到未處理的異常：{e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Unhandled Exception: {e}\n")
