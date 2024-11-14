import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QRadioButton, QLineEdit, QTextEdit, QPushButton, QGroupBox, QHBoxLayout, QLabel, QWidget, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from analyze import speechToTextOnWhisperModel
from download import Download
import convert as now_convert
import os
class DownloadAndProcessThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, input_text, selected_option, output_selected_option,sel_lang_option):
        super().__init__()
        #input_text: 輸入的網址或是檔案
        #selected_option: 選擇的模型大小
        #output_selected_option: 輸出的格式
        self.input_text = input_text
        self.selected_option = selected_option
        self.output_selected_option = output_selected_option
        self.sel_lang_option=sel_lang_option

    def get_file_name(self,input_file_path):
        # 移除副檔名
        base = os.path.splitext(input_file_path)[0]
        return base

    def model_process(self, filename,count):
        
        #speechToTextOnWhisperModel是個class，處理語音轉文字，這邊是初始化
        #設定使用cuda，計算型態為float16
        process_audio = speechToTextOnWhisperModel()
        process_audio.offset = count*300
        process_audio.setDeviceSetting('cuda')
        process_audio.setComputeTypeSetting('float16')

        #設定模型種類
        self.progress.emit(f"選擇的選項是: {self.selected_option}")
        self.progress.emit(f"選擇的語言: {self.sel_lang_option}")
        self.progress.emit("處理中")
        process_audio.setModelSize(self.selected_option)

        #執行模型
        if self.sel_lang_option == "中文(Chinese)":
            process_audio.run_model_with_chinese(filename)
        elif self.sel_lang_option == "英文(English)":
            process_audio.run_model_with_english(filename)
        elif self.sel_lang_option == "日文(Japanese)":
            process_audio.run_model_with_japanese(filename)
        elif self.sel_lang_option == "自動(Auto)":
            process_audio.runModel(filename)

        #輸出檔案
        if self.output_selected_option == "文字檔(.txt)":
            result_filename=self.get_file_name(filename)+".txt"
            process_audio.outputTxt(result_filename,count)
            
        elif self.output_selected_option == "字幕檔(.srt)":
            result_filename=self.get_file_name(filename)+".srt"
            process_audio.outputSrt(result_filename,count)
           
    
    def run(self):
        #這邊是執行緒的主要程式
        try:
            count=0
            #如果input_text是網址，就下載檔案
            if self.input_text.startswith("https"):
                self.progress.emit("下載中")
                #Download是個class，處理下載檔案
                download = Download(self.input_text, "./")
                #下載音訊檔案
                time=download.get_time_info()
                if time>300:
                    self.progress.emit("影片長度超過5分鐘")
                    for i in range(0,time,300):
                        filename = download.download_section_m4a(i, i+300)
                        self.progress.emit("下載完成")
                        #將下載的音訊檔案轉換成wav
                        need_process=now_convert.VideoConvert(filename, "./")
                        new_name=need_process.m4a_convert_to_wav()
                        #移除m4a檔案
                        os.remove(filename)
                        #執行模型
                        self.model_process(new_name,count)
                        count=count+1
                else:
                    filename = download.download_m4a()
                    self.progress.emit("下載完成")
                    #將下載的音訊檔案轉換成wav
                    need_process=now_convert.VideoConvert(filename, "./")
                    filename=need_process.m4a_convert_to_wav()
                    #執行模型
                    self.model_process(filename,count)
            else:
                #如果input_text是本地檔案，就直接轉換成wav
                need_process = now_convert.VideoConvert(self.input_text, "")
                if self.input_text[-3:] == 'wav':
                    filename = self.input_text
                #如果是mp3就轉換成wav
                elif self.input_text[-3:] == 'mp3':
                    filename = need_process.local_mp3_convert_to_wav()
                #如果是mp4就轉換成wav
                elif self.input_text[-3:] == 'mp4':
                    filename = need_process.local_mp4_convert_to_wav()
                elif self.input_text[-3:] == 'm4a':
                    filename = need_process.m4a_convert_to_wav()

                self.progress.emit("轉換完成")
                #執行模型
                self.model_process(filename,count)
            

            self.progress.emit("完成")
        except Exception as e:
            self.progress.emit(f"發生錯誤: {str(e)}")
        finally:
            self.finished.emit()
        
            

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('語音轉文字系統(Speech to Text System)')
        self.setGeometry(100, 100, 600, 400)

        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QVBoxLayout()
        

        input_group_box = QGroupBox("選擇來源(select source)")
        input_layout = QVBoxLayout()

        self.url_radio = QRadioButton("線上來源(Online Source)")
        self.url_radio.setChecked(True)
        self.url_radio.toggled.connect(self.toggle_input_method)
        input_layout.addWidget(self.url_radio)

        self.file_radio = QRadioButton("本地檔案(Local File)")
        self.file_radio.toggled.connect(self.toggle_input_method)
        input_layout.addWidget(self.file_radio)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("輸入要處理的影片網址(Enter the video URL to process)")
        input_layout.addWidget(self.url_input)

        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("選擇要處理的本地影片檔案(Choose the local video file to process)")
        self.file_input.setEnabled(False)
        input_layout.addWidget(self.file_input)

        self.file_button = QPushButton("瀏覽(Browse)", self)
        self.file_button.setEnabled(False)
        self.file_button.clicked.connect(self.browse_file)
        input_layout.addWidget(self.file_button)

        input_group_box.setLayout(input_layout)
        main_layout.addWidget(input_group_box)


        groupBox = QGroupBox("選擇模型大小(Select model size)")
        vbox = QVBoxLayout()
        self.radio_buttons = []
        options = ["small", "medium", "large", "large-v2", "large-v3"]
        for option in options:
            radio_button = QRadioButton(option)
            self.radio_buttons.append(radio_button)
            vbox.addWidget(radio_button)
        groupBox.setLayout(vbox)
        main_layout.addWidget(groupBox)

        groupBoxSelLang = QGroupBox("選擇語言(Select language)")
        vboxSelLang = QVBoxLayout()
        self.lang_buttons = []
        langOptions = ["自動(Auto)","中文(Chinese)", "英文(English)","日文(Japanese)"]
        
        for langOption in langOptions:
            lang_button = QRadioButton(langOption)
            self.lang_buttons.append(lang_button)
            vboxSelLang.addWidget(lang_button)
        self.lang_buttons[0].setChecked(True)
        groupBoxSelLang.setLayout(vboxSelLang)
        main_layout.addWidget(groupBoxSelLang)



        #選擇輸出txt或是srt

        groupBox2 = QGroupBox("輸出格式(Select output format)")
        vbox1 = QVBoxLayout()
        self.outputSel_buttons = []
        selOptions = ["文字檔(.txt)", "字幕檔(.srt)"]
        for selOption in selOptions:
            outputSel_button = QRadioButton(selOption)
            self.outputSel_buttons.append(outputSel_button)
            vbox1.addWidget(outputSel_button)
        groupBox2.setLayout(vbox1)
        main_layout.addWidget(groupBox2)


        self.progress_display = QTextEdit(self)
        self.progress_display.setReadOnly(True)
        main_layout.addWidget(self.progress_display)

        self.start_button = QPushButton('啟動', self)
        self.start_button.clicked.connect(self.startButtonClicked)
        main_layout.addWidget(self.start_button)

        widget.setLayout(main_layout)

    def toggle_input_method(self):
        if self.url_radio.isChecked():
            self.url_input.setEnabled(True)
            self.file_input.setEnabled(False)
            self.file_button.setEnabled(False)
        else:
            self.url_input.setEnabled(False)
            self.file_input.setEnabled(True)
            self.file_button.setEnabled(True)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "選擇檔案", "", "影片檔案 (*.mp4 *.avi *.mov), 音訊檔案 (*.wav *.mp3 *.m4a)")
        if file_name:
            self.file_input.setText(file_name)

    def startButtonClicked(self):
        selected_option = self.get_selected_option()
        output_selected_option = self.get_output_selected_option()
        sel_lang_option = self.get_sel_lang()
        if selected_option is None:
            self.progress_display.append("請選擇一個選項")
            return
        if output_selected_option is None:
            self.progress_display.append("請選擇一個輸出選項")
            return
        

        input_text = self.url_input.text() if self.url_radio.isChecked() else self.file_input.text()
        
        if input_text == "":
            self.progress_display.append("請輸入一個有效的輸入")
            return

        self.url_radio .setEnabled(False)
        self.file_radio.setEnabled(False)
        self.start_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.file_input.setEnabled(False)
        self.file_button.setEnabled(False)
        
        for radio_button in self.radio_buttons:
            radio_button.setEnabled(False)
        for outputSel_button in self.outputSel_buttons:
            outputSel_button.setEnabled(False)
        for lang_button in self.lang_buttons:
            lang_button.setEnabled(False)
    
        

        self.download_thread = DownloadAndProcessThread(input_text, selected_option, output_selected_option,sel_lang_option)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_finished)
        self.download_thread.start()

    def update_progress(self, message):
        self.progress_display.append(message)

    def on_finished(self):
        self.start_button.setEnabled(True)
        if self.url_radio.isChecked():
            self.url_input.setEnabled(True)
        else:
            self.file_input.setEnabled(True)
            self.file_button.setEnabled(True)
        for radio_button in self.radio_buttons:
            radio_button.setEnabled(True)
        for outputSel_button in self.outputSel_buttons:
            outputSel_button.setEnabled(True)
        for lang_button in self.lang_buttons:
            lang_button.setEnabled(True)

        self.url_radio .setEnabled(True)
        self.file_radio.setEnabled(True)
        self.progress_display.append("可以進行下一次操作")
    
                                            

    def get_selected_option(self):
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                return radio_button.text()
        return None
    
    def get_output_selected_option(self):
        for outputSel_button in self.outputSel_buttons:
            if outputSel_button.isChecked():
                return outputSel_button.text()
        return None

    def get_sel_lang(self):
        for lang_button in self.lang_buttons:
            if lang_button.isChecked():
                return lang_button.text()
        return None
        
    
    
   
if __name__ == '__main__':
    

    app = QApplication(sys.argv)
    ex = MyApp()
    
    ex.show()
    sys.exit(app.exec_())
    
    
