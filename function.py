import os
import requests


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

        file_name = "latest.zip"

        # 将文件保存到本地
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f"File '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")