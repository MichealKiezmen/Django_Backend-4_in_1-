import os
import fitz
from gtts import gTTS
from pathlib import Path

BASE_URL = Path(__file__).resolve().parent.parent


def string_to_convert(file):
    """A function that combines every texts in a pdf
    to one string using the pyMuPDF library"""

    string = ""
    with fitz.open(filename=file) as pdf_doc:
        for page in pdf_doc:
            string += page.get_text()

    return string

def speech(text_string, file_name):
    """Converts texts to speech and saves the
    file using google Text To Speech Package.It
    returns the path where the file is saved."""

    tts = gTTS(text=text_string, lang="en")
    audio_save_path = os.path.join(BASE_URL, "media", "audio", f"{file_name}.mp3")
    tts.save(audio_save_path)

    return audio_save_path



def delete_file_after_upload(current_file_path=str):
    """Deletes a file if it exists, Returns True for 'Yes', and False for 'No'."""
    if os.path.exists(current_file_path):
        os.remove(current_file_path)
        return True
    else:
        return False
