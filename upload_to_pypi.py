#!/usr/bin/env python3
"""
Simple script to upload to PyPI using requests.
"""
import os
import sys
import requests
import getpass
from pathlib import Path

def upload_to_pypi():
    # Get PyPI credentials
    username = input("PyPI username: ")
    password = getpass.getpass("PyPI password: ")
    
    # Find the distribution files
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("No dist/ directory found. Run 'python3 setup.py sdist bdist_wheel' first.")
        return 1
    
    files = list(dist_dir.glob("*"))
    if not files:
        print("No files found in dist/ directory.")
        return 1
    
    print(f"Found {len(files)} files to upload:")
    for f in files:
        print(f"  - {f.name}")
    
    # Upload to PyPI
    url = "https://upload.pypi.org/legacy/"
    
    for file_path in files:
        print(f"\nUploading {file_path.name}...")
        
        with open(file_path, 'rb') as f:
            files_data = {'file': (file_path.name, f, 'application/octet-stream')}
            data = {
                ':action': 'file_upload',
                'name': 'sevn',
                'version': '1.0.2',
            }
            
            response = requests.post(
                url,
                auth=(username, password),
                data=data,
                files=files_data
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully uploaded {file_path.name}")
            else:
                print(f"❌ Failed to upload {file_path.name}")
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                return 1
    
    print("\n🎉 All files uploaded successfully!")
    print("Your package is now available at: https://pypi.org/project/sevn/")
    return 0

if __name__ == "__main__":
    sys.exit(upload_to_pypi())