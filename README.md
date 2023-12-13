# auto_timing_subtitle
auto timing japanese subtitle using [Whisper](https://github.com/openai/whisper) and [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

Program is based on [faster-whisper](https://github.com/SYSTRAN/faster-whisper), a reimplementation of OpenAI's [Whisper](https://github.com/openai/whisper) , a general-prupose speech recognition model. This implementation is up to 4 times faster than original Whisper for the same accuracy while using less memory.

The output file will be in Advanced SubStation Alpha(ass) format with built-in style of selected sub group so it can be directly imported into [Aegisub](https://github.com/Aegisub/Aegisub) for subsequent editing.
## Files
- `auto_timing_subtitle.py`: main program that make japanese subtitle format srt and ass file with tkinter interface
- `process.py`: program that making japanese subtitle process
- `srt2ass.py`: program that convert srt file into ass file
- `requirment.txt`: contains requirement library that must be installed before running the main program
- `ffmpeg.exe`: there's link to download [ffmpeg.exe](https://drive.google.com/file/d/1yQBdXjjCHrxwjbNHvmFazyVv3Mh0ucOa/view?usp=sharing) for running ffmpeg
# requirement
You need to install python (3.11.6) is the latest version of python that can be use in this project. Python range version options is between (3.8 - 3.11.6).
You need to install this package before you run auto_timing_subtitle.py
* use python -i auto_timing_subtitle.py

* Python : You can access this link to install [python](https://www.python.org/downloads/) and using [pip](https://pypi.org/project/pip/) for installing  packages/libraries
* FFMPEG
  ```bash
  pip3 install ffmpeg
* pysubs2
  ```bash
  pip3 install pysubs2
* whisper from openai
  ```bash
  pip3 install -U openai-whisper
* faster-whisper
  ```bash
  pip3 install faster-whisper
* if torch already pre installed, then do 
  pip3 uninstall torch
* install torch with cuda render
  ```bash
  pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121 (for nvidia gpu)
