import os
import re
import zipfile

import py7zr
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

DOWNLOAD_DIR = "downloading"
EXTRACT_DIR = "finished"
LINKS_FILE = "links.txt"

# Some pages require a logged-in session cookie to allow the download.
# Set it via the VIMM_COOKIE environment variable if you run into 403/redirect errors.
VIMM_COOKIE = os.environ.get("VIMM_COOKIE", "")


def get_media(url):
    print("Fetching media information...")
    print(url)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        media_id_element = soup.find('input', {'name': 'mediaId'})
        url_element = soup.find('form', {'id': 'dl_form'})
        if media_id_element:
            media_id = media_id_element['value']
            download_url = url_element['action']
            return {'id': media_id, 'url': download_url, 'referer': url}
        else:
            print("Unable to find media")
            return None
    else:
        print("Error getting media:", response.status_code)
        return None


def download(media):
    download_url = "https:" + media['url'] + "?mediaId=" + media['id']
    print(download_url)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": media['url'].replace("/", ""),
        "Referer": media['referer'],
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    }
    if VIMM_COOKIE:
        headers["Cookie"] = VIMM_COOKIE

    with requests.get(download_url, headers=headers, stream=True, verify=False) as response:
        if response.status_code in (200, 304):
            total_size = int(response.headers.get('content-length', 0))
            content_disposition = response.headers.get('content-disposition')
            filename = None
            match = re.search(r'filename="(.+?)"', content_disposition)
            if match:
                filename = match.group(1)
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_path) as pbar:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
            print("Download finished!")
            if extract_and_delete(file_path, EXTRACT_DIR):
                print(f"Successfully extracted and deleted {file_path}")
            else:
                print(f"Failed to extract or delete {file_path}")
        else:
            print("Error downloading media:", response.text, response.status_code)
        return response.status_code


def extract_and_delete(archive_path, extract_dir):
    try:
        os.makedirs(extract_dir, exist_ok=True)
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                print(f"Extracted zip: {archive_path} to {extract_dir}")
        elif archive_path.endswith('.7z'):
            with py7zr.SevenZipFile(archive_path, 'r') as seven_zip:
                seven_zip.extractall(extract_dir)
                print(f"Extracted 7z: {archive_path} to {extract_dir}")
        else:
            print(f"Unsupported file format: {archive_path}")
            return False

        os.remove(archive_path)
        print(f"Deleted original file: {archive_path}")
        return True
    except Exception as e:
        print(f"Error extracting {archive_path}: {e}")
        return False


def download_from_txt(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    remaining_lines = []

    for line in lines:
        url = line.strip()
        if not url:
            continue
        print(f"URL: {url}")
        media = get_media(url)
        if media:
            print(f"Media found: {media['id']} {media['url']}")
            download(media)
            # Download succeeded, so this line is dropped from the file
            print("Download complete, removing URL from the queue file")
        else:
            print("Media not found")
            # Keep the line for a future retry
            remaining_lines.append(line)

    with open(file, 'w') as f:
        f.writelines(remaining_lines)


if __name__ == "__main__":
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    download_from_txt(LINKS_FILE)
