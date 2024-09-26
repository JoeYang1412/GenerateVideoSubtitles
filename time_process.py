# We will create a class that will take the time in seconds and convert it into hours, minutes and seconds.
import datetime
class time_process:
    def __init__(self,need_process):
        self.secondsProcess = need_process
    def process(self):
        hours = self.secondsProcess // 3600
        minutes = (self.secondsProcess % 3600) // 60
        seconds = self.secondsProcess % 60
        milliseconds = (seconds - int(seconds)) * 1000
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"