from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from pathlib import Path

BASE_URL = Path(__file__).resolve().parent.parent

credentials_file = os.path.join(BASE_URL, "PDF_to_Speech", "data", "credentials.json")

credentials = service_account.Credentials.from_service_account_file(
    filename=credentials_file,
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build("drive", "v3", credentials=credentials)

class AudioToURL:

    # Upload MP3 File
    def upload_audio(self, file_path=str, file_name=str):

        file_metadata = {"name": file_name}
        media = MediaFileUpload(file_path, mimetype='audio/mpeg')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        data_id = file.get('id')
        return data_id

    # Generate URL for the uploaded audio
    def get_audio_url(self, file_id=str):
        """Returns a url to download mp3 file
        automatically using the google drive key."""
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        drive_service.permissions().create(fileId=file_id, body=permission).execute()
        return f'https://drive.google.com/uc?export=download&id={file_id}'
