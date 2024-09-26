import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QRadioButton, QLineEdit, QTextEdit, QPushButton, QGroupBox, QHBoxLayout, QLabel, QWidget, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from analyze import speechToTextOnWhisperModel
from download import Download
import convert as now_convert

class DownloadAndProcessThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, input_text, selected_option, voice_separation, output_selected_option):
        super().__init__()
        #input_text: 輸入的網址或是檔案
        #selected_option: 選擇的模型大小
        #voice_separation: 是否啟用音訊分離
        #output_selected_option: 輸出的格式
        self.input_text = input_text
        self.selected_option = selected_option
        self.voice_separation = voice_separation
        self.output_selected_option = output_selected_option

    def model_process(self, filename):
        #speechToTextOnWhisperModel是個class，處理語音轉文字，這邊是初始化
        #設定使用cuda，計算型態為float16
        process_audio = speechToTextOnWhisperModel()
        process_audio.setDeviceSetting('cuda')
        process_audio.setComputeTypeSetting('float16')

        #設定模型種類
        self.progress.emit(f"選擇的選項是: {self.selected_option}")
        self.progress.emit("處理中")
        process_audio.setModelSize(self.selected_option)

        #執行模型
        process_audio.runModel(filename)

        #輸出檔案
        if self.output_selected_option == "文字檔(.txt)":
            process_audio.outputTxt("./result.txt")
        elif self.output_selected_option == "字幕檔(.srt)":
            process_audio.outputSrt("./result.srt")
    
    def run(self):
        #這邊是執行緒的主要程式
        try:
            #如果input_text是網址，就下載檔案
            if self.input_text.startswith("https"):
                self.progress.emit("下載中")
                #Download是個class，處理下載檔案
                download = Download(self.input_text, "./")
                #下載音訊檔案
                filename = download.download_m4a()
                self.progress.emit("下載完成")
                #將下載的音訊檔案轉換成wav
                need_process=now_convert.VideoConvert(filename, "./")
                self.progress.emit(need_process.m4a_convert_to_wav())
                #執行模型
                self.model_process(filename)
            else:
                #如果input_text是本地檔案，就直接轉換成wav
                need_process = now_convert.VideoConvert(self.input_text, "./")
                if self.input_text[-3:] == 'wav':
                    filename = self.input_text
                #如果是mp3就轉換成wav
                elif self.input_text[-3:] == 'mp3':
                    filename = need_process.local_mp3_convert_to_wav()
                #如果是mp4就轉換成wav
                elif self.input_text[-3:] == 'mp4':
                    filename = need_process.local_mp4_convert_to_wav()

        
                self.progress.emit("轉換完成")
                #執行模型
                self.model_process(filename)
            

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
        self.setWindowTitle('語音轉文字系統')
        self.setGeometry(100, 100, 600, 400)

        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QVBoxLayout()
        

        input_group_box = QGroupBox("選擇來源")
        input_layout = QVBoxLayout()

        self.url_radio = QRadioButton("線上來源")
        self.url_radio.setChecked(True)
        self.url_radio.toggled.connect(self.toggle_input_method)
        input_layout.addWidget(self.url_radio)

        self.file_radio = QRadioButton("本地檔案")
        self.file_radio.toggled.connect(self.toggle_input_method)
        input_layout.addWidget(self.file_radio)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("輸入要處理的影片網址")
        input_layout.addWidget(self.url_input)

        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("選擇要處理的本地影片檔案")
        self.file_input.setEnabled(False)
        input_layout.addWidget(self.file_input)

        self.file_button = QPushButton("瀏覽", self)
        self.file_button.setEnabled(False)
        self.file_button.clicked.connect(self.browse_file)
        input_layout.addWidget(self.file_button)

        input_group_box.setLayout(input_layout)
        main_layout.addWidget(input_group_box)


        groupBox = QGroupBox("選擇模型大小")
        vbox = QVBoxLayout()
        self.radio_buttons = []
        options = ["small", "medium", "large", "large-v2", "large-v3"]
        for option in options:
            radio_button = QRadioButton(option)
            self.radio_buttons.append(radio_button)
            vbox.addWidget(radio_button)
        groupBox.setLayout(vbox)
        main_layout.addWidget(groupBox)

        #選擇輸出txt或是srt

        groupBox2 = QGroupBox("輸出格式")
        vbox1 = QVBoxLayout()
        self.outputSel_buttons = []
        selOptions = ["文字檔(.txt)", "字幕檔(.srt)"]
        for selOption in selOptions:
            outputSel_button = QRadioButton(selOption)
            self.outputSel_buttons.append(outputSel_button)
            vbox1.addWidget(outputSel_button)
        groupBox2.setLayout(vbox1)
        main_layout.addWidget(groupBox2)




        groupBox3 = QGroupBox("音訊分離")
        vbox2 = QVBoxLayout()
        self.radio_buttons2 = []
        radio_buttons2 = QRadioButton("啟用音訊分離")
        self.radio_buttons2.append(radio_buttons2)
        vbox2.addWidget(radio_buttons2)
        groupBox3.setLayout(vbox2)
        main_layout.addWidget(groupBox3)


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
        file_name, _ = QFileDialog.getOpenFileName(self, "選擇檔案", "", "影片檔案 (*.mp4 *.avi *.mov), 音訊檔案 (*.wav *.mp3)")
        if file_name:
            self.file_input.setText(file_name)

    def startButtonClicked(self):
        selected_option = self.get_selected_option()
        voice_separation = self.get_voice_separation_selected_option()
        output_selected_option = self.get_output_selected_option()
        if selected_option is None:
            self.progress_display.append("請選擇一個選項")
            return
        if output_selected_option is None:
            self.progress_display.append("請選擇一個輸出選項")
            return
        
        if voice_separation:
            self.progress_display.append("音訊分離已啟用")

        input_text = self.url_input.text() if self.url_radio.isChecked() else self.file_input.text()
        
        if input_text == "":
            self.progress_display.append("請輸入一個有效的輸入")
            return

        self.start_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.file_input.setEnabled(False)
        self.file_button.setEnabled(False)

        self.download_thread = DownloadAndProcessThread(input_text, selected_option, voice_separation, output_selected_option)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_finished)
        self.download_thread.start()

    def update_progress(self, message):
        self.progress_display.append(message)

    def on_finished(self):
        self.start_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.file_input.setEnabled(True)
        self.file_button.setEnabled(True)
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



    def get_voice_separation_selected_option(self):
        for radio_buttons2 in self.radio_buttons2:
            if radio_buttons2.isChecked():
                return True
        return None
    
    
   
if __name__ == '__main__':
    

    app = QApplication(sys.argv)
    ex = MyApp()
    
    ex.show()
    sys.exit(app.exec_())
    
    
