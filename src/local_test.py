import subprocess
import os
import base64


def convert_to_pdf(input_path, output_folder):
    if not os.path.exists(input_path):
        raise Exception("Input file does not exist.")

    # TODO API GatewayからのINPUT生成
    input_base64_file: base64 = file_to_base64(input_path)
    file_name: str = os.path.basename(input_path)

    # Base64データを文字列に変換（オプション）
    decoded_file: bytes = base64.b64decode(input_base64_file)
    with open(f"./tmp/{file_name}", 'wb') as file:
        file.write(decoded_file)

    # コマンドの基本部分をリストに追加
    command: list = ["/opt/libreoffice7.6/program/soffice"]

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
    command.append(output_folder)
    # 入力ファイルのパスを追加
    command.append(f"/tmp/{file_name}")

    # コマンドを実行
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 変換後のPDFファイルパスを生成
    pdf_filename: str = os.path.basename(input_path).rsplit('.', 1)[0] + '.pdf'
    pdf_path: str = os.path.join(output_folder, pdf_filename)
    print('STDOUT: {}'.format(result.stdout))
    print('STDERR: {}'.format(result.stderr))

    base64_pdf: bytes

    if os.path.exists(pdf_path):
        print('PDF: {}'.format(pdf_path))
        print('Size: {}'.format(os.path.getsize(pdf_path)))
        base64_pdf = file_to_base64(pdf_path)
    else:
        raise Exception("The PDF file({}) cannot be found".format(pdf_path))

    return base64_pdf


def file_to_base64(file_path: str) -> base64:
    with open(file_path, 'rb') as file:
        binary_file = file.read()
    # バイナリーデータをBase64にエンコード
    input_base64_file: base64 = base64.b64encode(binary_file)
    return input_base64_file


convert_to_pdf('./test_document/test.pptx', './output/test.pdf')
