from PyPDF2 import PdfFileMerger
import os


def pdf_joiner(input_path, output_path=None, file_name='output.pdf'):
    '''
    takes all pdf files from input_path and merges them into a file
    'output.pdf' located in out
    input_path: directory where all the pdf files are
    output_path: directory where all the pdf files should go
    file_name: name of output file located inside output_path
    '''
    file_count = 0
    if not output_path:
        output_path = input_path

    pdf_merger = PdfFileMerger()
    for file in os.listdir(input_path):
        if not file.endswith('.pdf'):
            print(file + ' not a pdf')  # handles non-pdf files
            continue
        file_path = os.path.join(input_path, file)
        file_count += 1
        pdf_merger.append(file_path)

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if not file_name.endswith('.pdf'):
        file_name += '.pdf'

    output_file = os.path.join(output_path, file_name)
    with open(output_file, 'wb') as f:
        pdf_merger.write(f)

    print("{} files merged into {}".format(file_count, output_file))


pdf_joiner(input_path='pdf', file_name='JC CCA Records.pdf')
