import requests
from bs4 import BeautifulSoup

# Define the URL of the HTML page
url = 'https://siapi.bombeiros.go.gov.br/paginaInicialWeb.jsf'

# Define the protocolo and cpf_cnpj values
protocolo = "142009/23"
cpf_cnpj = "33786438000104"

# Send a GET request to fetch the HTML content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the CPF/CNPJ field and fill it with the value
cpf_cnpj_field = soup.find('input', id='cpf_cnpj')
cpf_cnpj_field['value'] = cpf_cnpj

# Find the Protocolo field and fill it with the value
protocolo_field = soup.find('input', id='protocolo')
protocolo_field['value'] = protocolo

# Find the Pesquisar button and click it by submitting the form
form = soup.find('form')
response = requests.post(url, data=form)

# Print the response content to verify if the button was clicked successfully
print(response.content)
