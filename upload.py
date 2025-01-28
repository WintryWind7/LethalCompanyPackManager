import os
import zipfile
import requests
from datetime import datetime

# Flask API 的 URL 和密码
UPLOAD_URL = "http://127.0.0.1:5000/upload"  # 上传到 Flask API，服务器将存放到 ./resource 目录

PASSWORD_FILE = "./password"  # 存储密码的文件
with open(PASSWORD_FILE, 'r') as file:
    password = file.read().strip()

# 要打包的目录
SOURCE_DIRECTORY = r"C:\Users\22721\AppData\Roaming\r2modmanPlus-local\LethalCompany\profiles\template"  # 替换为你要打包的目录
ZIP_FILE_NAME = f"archive_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"  # 动态生成压缩包名称


def create_zip(source_dir, zip_file_name):
    """
    将指定目录下的所有文件打包成一个 ZIP 文件。
    """
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 将文件写入 ZIP，并保留相对路径
                zipf.write(file_path, os.path.relpath(file_path, source_dir))
    print(f"Created zip file: {zip_file_name}")


def upload_zip(zip_file_name, upload_url, password):
    """
    上传 ZIP 文件到指定的 Flask API，并附带密码验证。
    """
    if not os.path.exists(zip_file_name):
        raise FileNotFoundError(f"Zip file '{zip_file_name}' does not exist.")

    with open(zip_file_name, 'rb') as f:
        files = {'file': (zip_file_name, f, 'application/zip')}
        data = {'password': password}  # 密码作为表单数据
        response = requests.post(upload_url, files=files, data=data)

        if response.status_code == 200:
            print("Upload successful!")
            print("Response:", response.json())
        else:
            print(f"Upload failed! Status code: {response.status_code}")
            print("Error message:", response.text)


if __name__ == "__main__":
    # 创建压缩包
    try:
        create_zip(SOURCE_DIRECTORY, ZIP_FILE_NAME)
    except Exception as e:
        print(f"Error creating zip file: {e}")
        exit(1)

    # 上传压缩包到 Flask 服务器的 ./resource 目录
    try:
        upload_zip(ZIP_FILE_NAME, UPLOAD_URL, password)
    except Exception as e:
        print(f"Error uploading zip file: {e}")
        exit(1)

    # 可选：删除本地生成的压缩包（如果不需要保留）
    if os.path.exists(ZIP_FILE_NAME):
        os.remove(ZIP_FILE_NAME)
        print(f"Deleted local zip file: {ZIP_FILE_NAME}")
