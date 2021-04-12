# Indoc
word to pdf , editable text, digital signature 
Steps to run the program - **Step 1 -** Run these commands in Command prompt pip install docx2txt pip install docx2pdf pip install PyPDF2 pip install reportlab pip install docx
![image](https://user-images.githubusercontent.com/44247436/114426986-9efa6680-9b88-11eb-8e3b-bd5ecd069f24.png)
![image](https://user-images.githubusercontent.com/44247436/114427022-aa4d9200-9b88-11eb-8377-a9fefe4e5f6a.png)

**Step 2 -** Download a sample signature jpg file from net and keep it in path.Create a sample word document with required content. Convert into pdf using the below lines of code.pdf file will be stored in the same path

result = docx2txt.process("sampleworddoc.docx") ###convert docx to pdf convert("sampleworddoc.docx")

**Step 3 -** Comment above lines and run the below fillpdf.py as shown below.

CMD - python fillpdf.py sampleworddoc.pdf image.jpg Python GUI IDLE 3.9.0 - Run Customized Or Shift +F5 - sampleworddoc.pdf image.jpg - click ok

Below signed pdf file will be stored in your directory.It is the outputfile.This document will be able to insert field value(In my example,Name) into the PDF.Last file attached - my current output file 
