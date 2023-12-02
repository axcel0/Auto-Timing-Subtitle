from pathlib import Path
import subprocess
import os
from tqdm import tqdm
import time
from urllib.parse import quote_plus
import pysubs2
import torch 
import whisper
from faster_whisper import WhisperModel
from srt2ass import srt2ass

def auto_sub_jp(file_type, model_size, is_split, split_method, beam_size, file_name):
    language = 'ja'
    sub_style = "default"
    is_vad_filter = "False"
    set_beam_size = int(beam_size)
    file_basename = Path(file_name).stem
    output_dir = Path(file_name).parent.resolve()
    print('Loading model...')

    if model_size == 'large-v3':
        model = whisper.load_model("large-v3")
        is_whisperv3 = True
    else:
        model = WhisperModel(model_size)
        is_whisperv3 = False

    #Transcribe
    if file_type == "video":
        print('Extracting audio from video file...')
        ffmpeg_path = "./ffmpeg.exe"
        ffmpeg_command = [ffmpeg_path, '-i', file_name, '-f', 'mp3', '-ab', '192000', '-vn', f'{file_basename}.mp3']
        try:
            subprocess.run(ffmpeg_command,check=True)
        except Exception as e:
            print(f"Error occurred while extracting audio: {e}")
        print('Done.')
    tic = time.time()
    print('Transcribe in progress...')

    if is_whisperv3:
        results = model.transcribe(audio = f'{file_basename}.mp3', language= language, verbose=False)
    else:
        segments, info = model.transcribe(audio = f'{file_basename}.mp3',
                                            beam_size=set_beam_size,
                                            language=language,
                                            vad_filter=is_vad_filter,
                                            vad_parameters=dict(min_silence_duration_ms=1000))
        total_duration = round(info.duration, 2)
        results= []
        with tqdm(total=total_duration, unit=" seconds") as pbar:
            for s in segments:
                segment_dict = {'start':s.start,'end':s.end,'text':s.text}
                results.append(segment_dict)
                segment_duration = s.end - s.start
                pbar.update(segment_duration)

    toc = time.time()
    print('Done')
    print(f'Time consumpution {toc-tic}s')
    time_comsumtion = toc-tic
    subs = pysubs2.load_from_whisper(results)
    subs.save(f'{output_dir}/{file_basename}.srt')

    ass_sub = srt2ass(f"{output_dir}/{file_basename}.srt", sub_style, is_split,split_method)
    print(f'ASS subtitle saved as: {ass_sub}')
    if file_type == "video":
        os.remove(f'{file_basename}.mp3')

    torch.cuda.empty_cache()
    return time_comsumtion