from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from pathlib import Path


class DriveClass:

    def __init__(self):
        self.mimetype = "application/pdf"
        BASE_URL = Path(__file__).resolve().parent.parent

        credentials_file = os.path.join(BASE_URL, "PDF_to_Speech", "data", "credentials.json")

        credentials = service_account.Credentials.from_service_account_file(
            filename=credentials_file,
            scopes=['https://www.googleapis.com/auth/drive']
        )

        self.drive_service = build("drive", "v3", credentials=credentials)

    def mimetype_func(self, file_name):

        splitted_filename = file_name.split(".")

        if splitted_filename[1] == "mp3":
            self.mimetype = "audio/mpeg"
        elif splitted_filename[1] == "txt":
            self.mimetype = "text/plain"
        elif splitted_filename[1] == "xls":
            self.mimetype = "application/vnd.ms-excel"
        elif splitted_filename[1] == "xlsx":
            self.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif splitted_filename[1] == "json":
            self.mimetype = "application/json"
        elif splitted_filename[1] == "csv":
            self.mimetype = "text/csv"

        return self.mimetype

    def upload_file(self, file_path=str, file_name=str):
        """ Uploads a file to google drive and returns an ID e.g: 1R3NOr2sYg4dTmkaXHO3l6eotdAAOAVuB
        Input:
        file_name = Consent Form.txt
        file_path = media/uploads/Consent Form.txt
        """
        mimetype = self.mimetype_func(file_name)

        file_metadata = {"name": file_name}
        media = MediaFileUpload(file_path, mimetype=mimetype)
        file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        data_id = file.get('id')
        return data_id

        # Generate URL for the uploaded audio
    def get_file_url(self, file_id=str):
        """Returns a url to download file
        automatically using the google drive key."""
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.drive_service.permissions().create(fileId=file_id, body=permission).execute()
        return f'https://drive.google.com/uc?export=download&id={file_id}'

    def delete_file_after_upload(self,current_file_path):
        if os.path.exists(current_file_path):
            os.remove(current_file_path)
            return True
        else:
            return False

    def delete_file_from_google_drive(self, file_id):
        try:
            self.drive_service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
