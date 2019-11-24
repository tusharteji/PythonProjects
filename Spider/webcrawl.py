# Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Constants
URL1 = 'https://www.sec.gov/Archives/edgar/data/70858/000122520808011733/0001225208-08-011733-index.htm'
URL2 = 'https://www.sec.gov/Archives/edgar/data/72971/000112760217023349/0001127602-17-023349-index.htm'
URL3 = 'https://www.sec.gov/Archives/edgar/data/72971/000112760214018678/0001127602-14-018678-index.htm'

# Variables
list_of_values = []

 
# MAIN CODE #

# Fetch Data
def fetch_form(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for table in soup.find_all('table', {'class': 'tableFile'}):
        links = table.find_all('a')
        for link in links:
            if 'html' in link.string:
                href = link.get('href')
                href = 'https://www.sec.gov/' + href
    fetch_values_to_add(href)


def fetch_values_to_add(doc_url):
    global list_of_values, sum_of_values
    source_code = requests.get(doc_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for table in soup.findAll('table'):
        if 'Non-Derivative Securities' in str(table):
            for value in table.find_all('span', {'class': 'FormData'}):
                value = value.string.strip().replace(',', '')
                try:
                    list_of_values.append(float(value))
                except:
                    pass
    sum_of_values = sum(list_of_values)
    print('Values:', list_of_values)
    print('Sum:', sum_of_values)


# Write to Excel
def write_to_xl(all_values, the_sum):
    all_values.extend(['', 'Total: ' + str(the_sum)])
    df = pd.DataFrame({'Amount': all_values})
    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


# Main Function #
if __name__ == "__main__":
    fetch_form(URL1)
    write_to_xl(list_of_values, sum_of_values)
