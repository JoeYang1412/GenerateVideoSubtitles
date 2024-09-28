# GenerateVideoSubtitles
This project can convert audio from videos into text. The functionalities include:

1. Users can choose between online or local sources; currently, only YouTube is supported for online sources.
2. The model used is faster-whisper, and users can select the model size. For better accuracy, it is recommended to use large-v3. If performance is insufficient, small can be selected.
3. The output can be chosen as either srt or txt format.
4. The language of the video is generally not restricted, but English works best, and Chinese will be output in Traditional Chinese.
5. When processing videos longer than 5 minutes, the video is processed in segments to help the model recognize the audio better.

Requirements: 
CUDA installation is required, 
and at least 3-4 GB of memory is recommended for better performance.

Issues:
1. It is unclear if the dependencies in the requirements file are complete.
2. The functionality for local sources is actually incomplete.
3. When processing videos longer than 5 minutes, sometimes only the first 5 minutes are processed.
4. When processing certain videos, the program may suddenly stop and only output partial results.
5. There may be other issues not mentioned.


本專案可以將影片中的聲音，轉換成文字
功能有
1. 可選擇線上或是本地來源，線上目前僅支援Youtube
2. 模型為faster-whisper，可以選擇模型大小，若要精準，建議large-v3，若效能不足，可選擇small
3. 可選擇輸出成srt或是txt
4. 影片語言基本上不限，但英文效果最好，中文則會輸出成繁體中文
5. 處理超過5分鐘以上影片時，會分段處理，讓模型較好辨識

需求:
需要安裝cuda
且記憶體最少需要3-4G會比較好


目前有以下幾個問題
1. dependcy不太確定是不是只有requirements中的那些
2. 來源為本地的功能其實並不完整
3. 處理超過5分鐘影片時，有時候只會處理到前五分鐘
4. 處理特定影片時，程式可能會突然中斷，並且僅輸出部分結果
5. 可能有其他未提及的問題