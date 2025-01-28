import os
import datetime
import zipfile
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 获取请求中的密码
    password = request.form.get('password')

    if not password:
        return jsonify({"error": "Password is required"}), 400

    # 从本地 ./password 文件读取密码
    try:
        with open('./password', 'r') as f:
            correct_password = f.readline().strip()  # 读取文件中的第一行密码并去掉换行符
    except FileNotFoundError:
        return jsonify({"error": "Password file not found"}), 400

    # 比较密码
    if password != correct_password:
        return jsonify({"error": "Incorrect password"}), 403

    # 生成文件保存路径和文件名，使用当前日期和时间
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{current_time}.{file.filename.rsplit('.', 1)[-1]}"  # 保持文件的扩展名
    file_path = os.path.join('./resource', filename)

    # 确保资源目录存在
    os.makedirs('./resource', exist_ok=True)

    # 保存文件到本地的 /resource 文件夹
    file.save(file_path)

    # # 解压 ZIP 文件（假设文件是 ZIP 格式）
    # if file.filename.endswith('.zip'):
    #     try:
    #         with zipfile.ZipFile(file_path, 'r') as zip_ref:
    #             extract_folder = os.path.join('./resource', current_time)
    #             os.makedirs(extract_folder, exist_ok=True)
    #             zip_ref.extractall(extract_folder)
    #         return jsonify({
    #             "message": "File successfully uploaded and extracted",
    #             "file_path": file_path,
    #             "extracted_folder": extract_folder
    #         }), 200
    #     except zipfile.BadZipFile:
    #         return jsonify({"error": "Bad ZIP file"}), 400
    # else:
    #     return jsonify({
    #         "message": "File successfully uploaded but not extracted, file is not a ZIP file",
    #         "file_path": file_path
    #     }), 200
    return jsonify({"filename": filename}), 200


@app.route('/download', methods=['GET'])
def download():
    # 设置资源文件夹路径
    resource_dir = './resource'

    # 获取该目录下所有的 .zip 文件
    zip_files = [f for f in os.listdir(resource_dir) if f.endswith('.zip')]

    if not zip_files:
        return jsonify({"error": "No zip files found in resource directory"}), 404

    # 获取最新的 .zip 文件
    latest_file = max(zip_files, key=lambda f: os.path.getmtime(os.path.join(resource_dir, f)))

    # 获取文件的完整路径
    file_path = os.path.join(resource_dir, latest_file)

    # 返回最新的文件给用户下载
    return send_file(file_path, as_attachment=True, download_name=latest_file)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
