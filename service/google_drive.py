from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings

from appointment.models import GoogleCredSettings


def upload_to_google_drive(file_path, file_name):
    credential = GoogleCredSettings.objects.filter().first()
    credentials = service_account.Credentials.from_service_account_file(
        credential.drive_cred_file.path,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': file_name,
        'parents': [settings.GOOGLE_DRIVE_PARENT_FOLDER_ID]
    }
    media = MediaFileUpload(file_path)

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    file_id = file.get('id')

    return f"https://drive.google.com/uc?id={file_id}"
