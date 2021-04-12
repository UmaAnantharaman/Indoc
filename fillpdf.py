import os
import time
import argparse
import tempfile
import PyPDF2
import datetime
from reportlab.pdfgen import canvas
import docx2txt
import docx2pdf
from docx2pdf import convert
from pathlib import Path
from PyPDF2 import PdfFileReader
from reportlab.pdfbase import pdfform

### read in word file and print contents
##result = docx2txt.process("sampleworddoc.docx")
##print(result)
##
###convert docx to pdf
#convert("sampleworddoc.docx")

#class PyPDF2.PdfFileReader(stream, strict=True, warndest=None, overwriteWarnings=True)
#Initializes a PdfFileReader object. This operation can take some time, as the PDF stream’s cross-reference tables are read into memory.

#ArgumentParser - recommended command-line parsing module in the Python standard library.
parser = argparse.ArgumentParser("Add signatures to PDF files")
parser.add_argument("pdf", help="The pdf file to annotate")
parser.add_argument("signature", help="The signature file (png, jpg)")
parser.add_argument("--date", action='store_true')
parser.add_argument("--output", nargs='?',
        help="Output file. Defaults to input filename plus '_signed'")
parser.add_argument("--coords", nargs='?', default='1x200x300x135x50',
        help="Coordinates to place signature.")

def get_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name

def sign_pdf(args):
    
    page_num, x1, y1, width, height = [int(a) for a in args.coords.split("x")]
    page_num = page_num - 1
    # Check if _signed is present in output_filename
    output_filename = args.output or "{}_signed{}".format(
        *os.path.splitext(args.pdf)
    )

    pdf_fh = open(args.pdf, 'rb')
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    #class PyPDF2.PdfFileWriter - This class supports writing PDF files out, given pages produced by another class (typically PdfFileReader).
    writer = PyPDF2.PdfFileWriter()
    
    sig_tmp_filename = None
    
    #getNumPages()- Calculates the number of pages in this PDF file.
    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:
            # Create PDF for signature
            sig_tmp_filename = get_filename()

            ## generate a canvas
            # reportlab.pdfgen has a concept of drawing Canvas
            #ReportLab has built-in support for creating interactive forms
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)

            #c = canvas.Canvas(sig_tmp_filename)
    
            c.setFont("Courier", 20)
            c.setFont("Courier", 14)
            form = c.acroForm
            
            c.drawString(10, 650, 'Name:')
            form.textfield(name='fname', tooltip='Name',
                           x=110, y=635, borderStyle='inset',
                           width=300, forceBorder=True)

           
            c.drawImage(args.signature, x1, y1, width, height, mask='auto')
            if args.date:
                # datetime.now() -- current date and time, %Y, %m, %d etc. are format codes. The strftime() method takes one or more format codes as an argument
                c.drawString(x1 + width, y1, datetime.datetime.now().strftime("%Y-%m-%d"))
            c.showPage()
            c.save()

            # Merge PDF into original page
            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)

            #The MediaBox is used to specify the width and height of the PDF page
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)
        writer.addPage(page) # Adds a page to this PDF file.

    with open(output_filename, 'wb') as fh:
        writer.write(fh)

    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)

def main():
    sign_pdf(parser.parse_args())


if __name__ == "__main__":
    main()
