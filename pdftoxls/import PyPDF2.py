import PyPDF2
from pathlib import Path

# Function to extract data from the PDF
def extract_data_from_pdf(pdf_path):
    data = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                if "Mês de referência:" in line:
                    # Extract month and value
                    parts = line.split()
                    try:
                        month_index = parts.index("referência:") + 1
                        value_index = parts.index("R$") + 1
                        month = parts[month_index]
                        value = parts[value_index].replace(".", "").replace(",", ".")
                        data.append((month, float(value)))
                    except ValueError:
                        # Handle case where expected structure is not found
                        pass
    return data

# Path to the PDF file
pdf_path = Path(__file__).with_name("dividas.pdf")

# Extract the data
extracted_data = extract_data_from_pdf(pdf_path)

# Sort data by month (to ensure order)
sorted_data = sorted(extracted_data, key=lambda x: x[0])

# Format the data for display
formatted_data = "\n".join([f"{month}\t{value:.2f}" for month, value in sorted_data])
print(formatted_data)
