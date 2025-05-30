import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_credentials():
    """Get valid user credentials from storage.
    
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.
    
    Returns:
        Credentials, the obtained credential.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_service():
    """Get Google Sheets API service instance."""
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f'Error getting service: {e}')
        return None


def read_data(spreadsheet_id, range_name):
    """Read data from a specific range in the spreadsheet."""
    try:
        service = get_service()
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name).execute()
        return result.get('values', [])
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def write_data(spreadsheet_id, range_name, values):
    """Write data to a specific range in the spreadsheet."""
    try:
        service = get_service()
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return True
    except HttpError as error:
        print(f'An error occurred: {error}')
        return False


def append_data(spreadsheet_id, range_name, values):
    """Append data to the end of a specific range in the spreadsheet."""
    try:
        service = get_service()
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
        return True
    except HttpError as error:
        print(f'An error occurred: {error}')
        return False
