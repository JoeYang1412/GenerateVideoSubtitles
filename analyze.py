from faster_whisper import WhisperModel

class speechToTextOnWhisperModel:
    # offset is the time offset in seconds，process long audio in segments
    offset = 0.0
    def __init__(self):
        self.model_size = None
        self.device = None
        self.compute_type = None
        self.current_model_size = None
        self.model=None
        self.result=None
        
        
    # set model size
    def setModelSize(self, model_size_input):
        self.model_size = model_size_input
    # set device setting
    def setDeviceSetting(self, device_setting):
        self.device = device_setting
    # set compute type setting
    def setComputeTypeSetting(self, compute_type_setting):
        self.compute_type = compute_type_setting

    def loadModel(self):
        
        if self.model is None:
            # 在重新加載模型前，釋放舊模型的資源
            print("加載模型中...")
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            self.current_model_size = self.model_size  # 更新已加載的模型大小
            print("模型加載完成。")
        else:
            # 如果模型大小未更改，則不重新加載模型
            if self.current_model_size == self.model_size:
                print("模型已加載，無需再次加載。")
            else:
                print("重新加載模型中...")
                self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
                self.current_model_size = self.model_size
                print("模型加載完成。")
            
    
    # run model
    def runModel(self, input_audio):
        
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5)
        self.result = list(self.segments)
        

    def run_model_with_chinese(self,input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="zh")
        self.result = list(self.segments)
        

    def run_model_with_english(self,input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="en")  
        self.result = list(self.segments)
      
    
    def run_model_with_japanese(self,input_audio):
        self.segments, self.info = self.model.transcribe(input_audio, beam_size=5, language="ja")
        self.result = list(self.segments)
    
    def get_result(self):
        return self.result
    
