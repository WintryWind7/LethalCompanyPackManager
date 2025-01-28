import os
import requests
import zipfile

def extract_and_delete(zip_file_name="lastest.zip"):
    # 确保文件存在
    if not os.path.exists(zip_file_name):
        print(f"Error: {zip_file_name} does not exist.")
        return
    yield 88
    # 解压文件
    try:
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall()  # 解压到当前目录
        print(f"Successfully extracted {zip_file_name}.")
    except zipfile.BadZipFile:
        print(f"Error: {zip_file_name} is not a valid zip file.")
        return
    yield 93
    # 删除压缩包
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)
        print(f"Deleted {zip_file_name} after extraction.")
        yield 100


def check_location():
    """
    检查指定目录下是否存在指定的文件。

    :param directory: 要检查的目录路径
    :param files_to_check: 文件名列表，包含需要检查的文件名
    :return: 如果所有文件都存在，返回 True；否则程序退出
    """
    files = ['Lethal Company.exe', 'UnityCrashHandler64.exe']

    for file in files:
        file_path = os.path.join('.', file)
        if os.path.exists(file_path):
            continue
        else:
            return False
    return True


def download():
    DOWNLOAD_URL = "http://127.0.0.1:5000/download"

    # 发送 GET 请求以下载文件
    response = requests.get(DOWNLOAD_URL)

    if response.status_code == 200:
        total_size = int(response.headers.get('Content-Length', 0))
        downloaded_size = 0
        file_name = "latest.zip"

        # 将文件保存到本地
        with open(file_name, 'wb') as f:
            # 分块下载文件
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # 计算下载进度
                    download_progress = (downloaded_size / total_size) * 100
                    # 映射进度到 10% - 85%
                    mapped_progress = 10 + (download_progress * 0.75)

                    # 返回进度
                    yield mapped_progress

        print(f"File '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")