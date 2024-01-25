import base64
import json
import subprocess
import os


class Main:
    TEMP_DIR = "/tmp"

    def __init__(self, event):
        self.body = json.loads(event["body"])

    def exec(self):
        input_base64_file: bytes = self.body["file"]
        file_name: str = self.body["fileName"]

        # Base64データを文字列に変換（オプション）
        decoded_file: bytes = base64.b64decode(input_base64_file)
        with open(f"{Main.TEMP_DIR}{file_name}", 'wb') as file:
            file.write(decoded_file)

        command = ["/opt/libreoffice7.6/program/soffice"]
        command.append("--headless")
        command.append("--norestore")
        command.append("--invisible")
        command.append("--nodefault")
        command.append("--nofirststartwizard")
        command.append("--nolockcheck")
        command.append("--nologo")
        command.append("--convert-to")
        command.append("pdf:writer_pdf_Export")
        command.append("--outdir")
        command.append(Main.TEMP_DIR)
        command.append(f"{Main.TEMP_DIR}/{file_name}")

        # コマンドを実行
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('STDOUT: {}'.format(result.stdout))
        print('STDERR: {}'.format(result.stderr))

        key_list = file_name.split('.')
        pdf_path = f"{Main.TEMP_DIR}" + file_name.replace(key_list[-1], 'pdf')

        base64_pdf: bytes
        if os.path.exists(pdf_path):
            print('PDF: {}'.format(pdf_path))
            print('Size: {}'.format(os.path.getsize(pdf_path)))
            base64_pdf = self.file_to_base64(pdf_path)
        else:
            raise Exception("The PDF file({}) cannot be found".format(pdf_path))

        return base64_pdf

    @classmethod
    def file_to_base64(cls, file_path: str) -> base64:
        with open(file_path, 'rb') as file:
            binary_file = file.read()
        input_base64_file: base64 = base64.b64encode(binary_file)
        return input_base64_file
