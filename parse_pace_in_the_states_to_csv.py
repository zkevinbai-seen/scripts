import fitz  # PyMuPDF
import pandas as pd
import re
import pdfplumber

# Path to your PDF file
pdf_path = "pdfs/Public_PACE_in_the_States_3.24.pdf"

# Define the pattern to extract data
pattern = re.compile(
    r"(?P<State>[A-Z]{2})\s+(?P<Program>[^\d]+?)\s+(?P<HNumber>H\d+)\s+(?P<City>[\w\s]+?)\s+(?P<StartDate>\d{1,2}/\d{1,2}/\d{4})\s+(?P<Census>\d+)"
)

data_rows = []
valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", 
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", 
                "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", 
                "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
                "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
current_state = None

# Extract text from each page of the PDF
with pdfplumber.open(pdf_path) as pdf:
    content = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())

# print(content)

# Apply the regex to the consolidated content from all pages
matches = re.finditer(pattern, content)
for match in matches:
    row_data = match.groupdict()
    if row_data['State'] in valid_states:
        current_state = row_data['State']
    row_data['State'] = current_state  # Apply the last known valid state
    
    # Clean the program name if it starts erroneously with a state code
    if row_data['Program'].startswith(row_data['State'] + ' '):
        row_data['Program'] = row_data['Program'][len(row_data['State']) + 1:].strip()
    
    data_rows.append(row_data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data_rows)

print("Preview of DataFrame:")
print(df.head(10))
print(df.tail(10))

# Saving the data to a CSV file
df.to_csv("output_filename.csv", index=False)

# Saving the text to a txt file
with open('output_text_file.txt', 'w', encoding='utf-8') as file:
    file.write(content)