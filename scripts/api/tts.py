from gtts import gTTS
import os
import sys

# TODO:
# - add args
#     - input text
#     - flag to specify language
# - add other TTS libraries
    # - pyttsx3 is a fully OFFLINE text to speech conversion
    #     - https://pypi.org/project/pyttsx3/

language_list = ["en", "fr"]
cur_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(cur_dir)
tts_dir = os.path.join(scripts_dir, 'data', 'api', 'tts')

default_text = """
gTTS utilizes the Google Translate text-to-speech API to generate natural-sounding speech. It requires an internet connection to function.
"""

if os.path.exists(tts_dir):
    input_text_list = []
    for filename in os.listdir(tts_dir):
        filepath = os.path.abspath(os.path.join(tts_dir, filename))
        if os.path.isfile(filepath) and filename.endswith('.txt'):
            with open(filepath, "r") as f:
                content = f.read()
                input_text_list.append(content)
    text = "\n".join(input_text_list)
else:
    text = default_text

# output MP3 file
output_dir = os.path.join(scripts_dir, 'data', 'api', 'tts', 'mp3s', '')
if os.path.exists(output_dir) is False:
    os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'output.mp3')

# TTS
tts = gTTS(text=text, lang=language_list[0], slow=False)
tts.save(output_file)


# To play the audio (requires a media player installed)
# os.system("start output.mp3") # For Windows
# os.system("mpg321 output.mp3") # For Linux
os.system(f"open {os.path.abspath(output_dir)}") # macOS, open output directory