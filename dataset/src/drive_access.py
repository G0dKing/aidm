# drive_access.py

from dotenv import load_dotenv
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
from io import BytesIO
import fitz

# Initialize
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_google_doc(file_id, drive_service):
    export_mime_type = 'text/plain'
    request = drive_service.files().export_media(fileId=file_id, mimeType=export_mime_type)
    file_content = BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return file_content.getvalue().decode('utf-8')

def read_text_file(file_id, drive_service):
    request = drive_service.files().get_media(fileId=file_id)
    file_content = BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return file_content.getvalue().decode('utf-8')

def read_pdf_file(file_id, drive_service):
    request = drive_service.files().get_media(fileId=file_id)
    file_content = BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    pdf_text = ""
    doc = fitz.open(stream=file_content, filetype='pdf')
    for page in doc:
        pdf_text += page.get_text()

    return pdf_text

def extract_files_from_drive(folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_DRIVE_API_KEY')

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=credentials)

    def extract_files(folder_id):
        query = f"'{folder_id}' in parents"
        results = drive_service.files().list(q=query).execute()
        items = results.get('files', [])

        extracted_texts = []

        for item in items:
            file_id = item['id']
            file_name = item['name']
            mime_type = item['mimeType']

            if mime_type == 'application/vnd.google-apps.folder':
                # Recursively extract contents of the folder
                extracted_texts.extend(extract_files(file_id))
            elif mime_type == 'application/vnd.google-apps.document':
                # Read Google Docs content
                doc_text = read_google_doc(file_id, drive_service)
                extracted_texts.append(doc_text)
            elif mime_type == 'text/plain':
                # Read plain text file content
                text_file_text = read_text_file(file_id, drive_service)
                extracted_texts.append(text_file_text)
            elif mime_type == 'application/pdf':
                # Read PDF content
                pdf_text = read_pdf_file(file_id, drive_service)
                extracted_texts.append(pdf_text)

        return extracted_texts

    return extract_files(folder_id)
