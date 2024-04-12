import fitz  # PyMuPDF
import pandas as pd
import re

# Open the provided PDF file
document = fitz.open("/mnt/data/Public_PACE_in_the_States_3.24.pdf")

# Prepare a pattern to capture the relevant data
pattern = re.compile(
    r"(?P<State>[A-Z]{2})\s+(?P<Program>[\w\s]+)\s+(?P<HNumber>H\d+)\s+(?P<City>[\w\s]+)\s+(?P<StartDate>\d{1,2}/\d{1,2}/\d{4})\s+(?P<Census>\d+)"
)

# List to store each row of data
data_rows = []

# Iterate over each page of the PDF
for page_number in range(len(document)):
    page = document[page_number]
    text = page.get_text("text")
    matches = pattern.finditer(text)
    for match in matches:
        row_data = match.groupdict()
        data_rows.append(row_data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data_rows)

# Show a preview of the DataFrame to confirm extraction
df.head(), df.tail()
