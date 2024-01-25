import base64
import json
import subprocess
import boto3
import os
import urllib.parse


"""
S3からファイル取得してPDFに変換し、S3にアップするこーど
"""
class Main:
    OUTPUT_BUKET = "libreoffice-out-ten"

    def __init__(self, event):
        self.event = event
        self.s3 = boto3.resource('s3')

    def exec(self):
        if 'Records' in self.event.keys():
            input_bucket = self.event['Records'][0]['s3']['bucket']['name']
            input_key = urllib.parse.unquote_plus(self.event['Records'][0]['s3']['object']['key'], encoding='utf-8')
            in_bucket = self.s3.Bucket(input_bucket)
        else:
            return 'test finished'

        # # TODO
        # self.event = json.loads(self.event['body'])
        # input_key = self.event['key']
        # in_bucket = self.s3.Bucket("libreoffice-input-ten")

        print(input_key)

        # get S3 Object
        file_path = '/tmp/' + input_key
        in_bucket.download_file(input_key, file_path)

        # proc = subprocess.run("/opt/libreoffice7.6/program/soffice --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to pdf:writer_pdf_Export --outdir /tmp {}".format("/tmp/"+input_key), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # コマンドの基本部分をリストに追加
        command = ["/opt/libreoffice7.6/program/soffice"]

        # 各オプションをリストに追加
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
        command.append("/tmp")

        # ファイル名を追加
        input_file = "/tmp/" + input_key  # input_keyは適切に定義されている必要があります
        command.append(input_file)

        # コマンドを実行
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('STDOUT: {}'.format(result.stdout))
        print('STDERR: {}'.format(result.stderr))

        key_list = input_key.split('.')
        pdf_path = "/tmp/" + input_key.replace(key_list[-1], 'pdf')

        # put S3 Object
        if os.path.exists(pdf_path):
            print('PDF: {}'.format(pdf_path.replace("/tmp/", "")))
            print('Size: {}'.format(os.path.getsize(pdf_path)))
            data = open(pdf_path, 'rb')
            out_bucket = self.s3.Bucket(Main.OUTPUT_BUKET)
            out_bucket.put_object(Key=pdf_path.replace("/tmp/", ""), Body=data)
            data.close()
            base64_pdf = self.file_to_base64(pdf_path)
        else:
            print("The PDF file({}) cannot be found".format(pdf_path))

        return base64_pdf

    @classmethod
    def file_to_base64(cls, file_path: str) -> base64:
        with open(file_path, 'rb') as file:
            binary_file = file.read()
        input_base64_file: base64 = base64.b64encode(binary_file)
        return input_base64_file
