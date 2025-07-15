import zipfile
import requests
from settings import SETTING_SESSIONID_300W

# Visit the URL in a browser to get the latest session ID
# If the website ask to fill a form, do it and then copy the session ID from the cookies
url = 'https://ibug.doc.ic.ac.uk/download/annotations/helen.zip'

cookies = {
    'sessionid': SETTING_SESSIONID_300W,
}

download_path = '300W.zip'

response = requests.get(url, allow_redirects=True, cookies=cookies, stream=True)

with open(download_path, 'wb') as file:
    id = 0
    for chunk in response.iter_content(chunk_size=8192):
        id += 1
        print(f"Received chunk {id} of size: {len(chunk)} bytes")
        if chunk:  # filter out keep-alive new chunks
            file.write(chunk)

print("Download completed. Extracting files...")
with zipfile.ZipFile(download_path, 'r') as zip_ref:
    zip_ref.extractall(download_path.replace('.zip', ''))