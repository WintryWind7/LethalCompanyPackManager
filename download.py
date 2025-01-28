import requests

# Flask API 的 URL
DOWNLOAD_URL = "http://127.0.0.1:5000/download"

# 发送 GET 请求以下载文件
response = requests.get(DOWNLOAD_URL)

if response.status_code == 200:
    # 获取文件名（从响应头中获取）
    content_disposition = response.headers.get('Content-Disposition')
    if 'filename=' in content_disposition:
        file_name = content_disposition.split('filename=')[-1].strip('\"')
    else:
        # 如果没有提供文件名，可以使用默认的文件名
        file_name = "latest_file.zip"

    # 将文件保存到本地
    with open(file_name, 'wb') as f:
        f.write(response.content)

    print(f"File '{file_name}' downloaded successfully.")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
