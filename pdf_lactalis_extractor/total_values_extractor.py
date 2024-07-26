import os
import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def find_total_value(text):
    pattern = re.compile(r'VALOR TOTAL DA NOTA[:\s]*[\d,.]+')
    match = pattern.search(text)
    if match:
        return match.group(0)
    return None

def find_date(text):
    date_pattern = re.compile(r'\b\d{2}\.\d{2}\.\d{4}\b')
    date_match = date_pattern.search(text)
    if date_match:
        return date_match.group(0)
    return None

def extract_total_values_and_dates_from_pdfs(pdf_dir):
    total_values_and_dates = {}
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith('.PDF'):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            total_value = find_total_value(text)
            date = find_date(text)
            if total_value or date:
                total_values_and_dates[pdf_file] = {
                    'total_value': total_value,
                    'date': date
                }
    return total_values_and_dates

# Define the directory containing the PDF files
pdf_directory = '.'  # Update this with your directory path

# Extract total values and dates
total_values_and_dates = extract_total_values_and_dates_from_pdfs(pdf_directory)

# Print the results
for pdf_file, data in total_values_and_dates.items():
    total_value = data.get('total_value', 'N/A')
    date = data.get('date', 'N/A')
    print(f'{pdf_file}: Total Value: {total_value}, Date: {date}')
