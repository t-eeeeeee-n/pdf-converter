import subprocess
import os

def convert_to_pdf(input_path, output_folder):
    if not os.path.exists(input_path):
        return "Input file does not exist."

    # proc = subprocess.run(
    #     "/opt/libreoffice7.6/program/soffice --headless --norestore --invisible --nodefault --nofirststartwizard "
    #     "--nolockcheck --nologo --convert-to pdf:writer_pdf_Export --outdir {} {}".format(
    #         output_folder, input_path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    command.append(output_folder)  # output_folderは適切に定義されている必要があります

    # 入力ファイルのパスを追加
    command.append(input_path)  # input_pathは適切に定義されている必要があります

    # コマンドを実行
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 変換後のPDFファイルパスを生成
    pdf_filename = os.path.basename(input_path).rsplit('.', 1)[0] + '.pdf'
    pdf_path = os.path.join(output_folder, pdf_filename)

    if os.path.exists(pdf_path):
        print('PDF: {}'.format(pdf_path))
        print('Size: {}'.format(os.path.getsize(pdf_path)))
    else:
        print("The PDF file({}) cannot be found".format(pdf_path))

    return ''

# 例: ファイルを'/path/to/input/file.docx'から読み取り、'/path/to/output/folder'にPDFを保存
convert_to_pdf('./test_document/test.pptx', './output/test.pdf')
