# dlsite-rename

抓取 dlsite 的資料來重新命名資料夾或檔案名稱，並移動到指定資料夾。  
只支援 RJ 系列。

## Getting Started

1. 下載 dist 資料夾到你的電腦
2. 編輯 config.yaml
3. 執行 main.exe

## config 說明

```
# 處理 from_dir 裡的檔案與資料夾，並移動到 to_dir
from_dir: 'D:/workspace'
to_dir: 'D:/workspace/done'

# 可用的關鍵字 code, title, maker
name_format: "[{maker}_{code}] {title}"

# 是否只處理資料夾
only_dir: true

# 是否建立 dlsite 捷徑
create_shortcut: true
shortcut_filename: "dlsite"

# 是否下載封面
download_cover: true
cover_filename: "cover"

# 替換檔案名稱
replace_filename_patterns:
- from: ".wav.vtt"
  to: ".vtt"
- from: ".wav.srt"
  to: ".srt"
- from: ".flac.vtt"
  to: ".vtt"
- from: ".flac.srt"
  to: ".srt"
- from: ".mp3.vtt"
  to: ".vtt"
- from: ".mp3.srt"
  to: ".srt"
```


## Dependencies

python3 -m venv venv  
.\venv\Scripts\activate  
deactivate

pip freeze > requirements.txt  
pip install -r requirements.txt
