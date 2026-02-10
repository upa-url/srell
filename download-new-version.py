#!/usr/bin/env python3
#
import http.client
import os
import re
import shutil
import sys
import urllib.request
import zipfile
from urllib.parse import urlparse

url = urlparse('https://www.akenotsuki.com/misc/srell/srell-latest')

version_path = 'version.txt'
archive_path = 'srell-src.zip'
extract_dir = 'srell-src'

# --------------------------------------------------------

def read_version():
    try:
        with open(version_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ''

def write_version(version):
    with open(version_path, 'w', encoding='utf-8') as file:
        file.write(version)

def download_and_unzip(archive_url):
    urllib.request.urlretrieve(archive_url, archive_path)
    print(f"Downloaded to {archive_path}", file=sys.stderr)

    # Replace the contents of extract_dir with the extracted files
    try:
        shutil.rmtree(extract_dir)
    except FileNotFoundError:
        pass
    with zipfile.ZipFile(archive_path, 'r') as file:
        file.extractall(extract_dir)
    os.remove(archive_path)
    print(f"Extracted to {extract_dir}", file=sys.stderr)

# --------------------------------------------------------

try:
    conn = http.client.HTTPConnection(url.netloc)
    conn.request("HEAD", url.path or "/")
    response = conn.getresponse()

    if 300 <= response.status < 400 and 'Location' in response.headers:
        archive_url = response.headers['Location']
        # get version from archive_url
        match = re.search(r"([0-9]+(_[0-9]+)+)\.zip$", archive_url)
        if match is not None:
            version_new = match.group(1).replace('_', '.')
            # local version from file
            version = read_version()

            if version != version_new:
                print(f"Found new version: {version_new}", file=sys.stderr)
                print(f"Download URL: {archive_url}", file=sys.stderr)
                download_and_unzip(archive_url)
                write_version(version_new)
                print(version_new)
        else:
            print(f"ERROR: A version cannot be found in the URL:\n{archive_url}",
                file=sys.stderr)
    else:
        print("ERROR: No redirection", file=sys.stderr)

    conn.close()

except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
