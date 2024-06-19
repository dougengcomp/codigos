import csv
import PyPDF2
import re

def find_link_in_csv():
    data = open('find_the_link.csv',encoding="utf-8")
    csv_data = csv.reader(data)
    data_lines=list (csv_data)

    i=0
    link=''
    for line in data_lines:
        link=link+line[i]
        i+=1
        
    print(link)

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
                
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        
    return text

pdf_text=extract_text_from_pdf("Find_the_Phone_Number.pdf")
pattern=r'\d{3}.\d{3}.\d{4}'
objeto_pesquisa=re.findall(pattern,pdf_text)
print (objeto_pesquisa[0])


'''
all_emails=[]
for line in data_lines:
    print(line[3])
'''
