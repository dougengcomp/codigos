import PyPDF2
import re
from pathlib import Path
import xlwt

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

def search_keyword_date_and_amount_in_text(text):
    pattern = r"Mês de referência:\s*(\d{2}/\d{4})\s*R\$\s*([\d.,]+)"
    matches = re.findall(pattern, text)
    return matches

def save_to_excel(matches, script_dir):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Dividas')
    sheet.write(0, 0, 'Date')
    sheet.write(0, 1, 'Amount')

    amount_style = xlwt.easyxf(num_format_str='#,##0.00')

    for i, (date, amount) in enumerate(matches, start=1):
        sheet.write(i, 0, date)  # Write the date as pure text
        # Convert the amount to a float, handling the formatting
        amount = amount.replace('.', '').replace(',', '.')  # Replacing '.' with '' and ',' with '.'
        try:
            amount = float(amount)
            sheet.write(i, 1, amount, amount_style)  # Apply amount formatting
        except ValueError:
            print(f"Error converting amount to float: {amount}")

    excel_file_path = script_dir / 'dividas.xls'
    workbook.save(excel_file_path)
    print(f"Data saved to: {excel_file_path}")

def main(pdf_path):
    script_dir = Path(__file__).resolve().parent
    text = extract_text_from_pdf(pdf_path)
    
    if text:
        matches = search_keyword_date_and_amount_in_text(text)
        if matches:
            print(f"Found {len(matches)} occurrence(s) of the keyword 'Mês de referência:'.")
            save_to_excel(matches, script_dir)
        else:
            print("No occurrences of the keyword 'Mês de referência:' found.")
    else:
        print("No text extracted from the PDF.")

# Path to the PDF file
pdf_path = Path(__file__).with_name("dividas.pdf")

if __name__ == "__main__":
    main(pdf_path)
