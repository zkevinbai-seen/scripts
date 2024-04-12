import fitz  # PyMuPDF
import pandas as pd
import re

# Open the provided PDF file
document = fitz.open("pdfs/Public_PACE_in_the_States_3.24.pdf")

pattern = re.compile(
    r"(?:(?P<State>[A-Z]{2})\s)?(?P<Program>[^\d]+?)\s+(?P<HNumber>H\d+)\s+(?P<City>[\w\s]+?)\s+(?P<StartDate>\d{1,2}/\d{1,2}/\d{4})\s+(?P<Census>\d+)"
)

# List of valid U.S. state codes
valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", 
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", 
                "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", 
                "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
                "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# List to store each row of data
data_rows = []
current_state = None  # To store the last valid state encountered

# Iterate over each page of the PDF
for page_number in range(len(document)):
    page = document[page_number]
    text = page.get_text("text").replace('\n', ' ')  # Normalize the text by removing newlines
    matches = pattern.finditer(text)
    for match in matches:
        row_data = match.groupdict()
        # Update current_state if a valid state is found
        if row_data['State']:
            current_state = row_data['State']
        row_data['State'] = current_state  # Assign the current state
        data_rows.append(row_data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data_rows)

# Print to debug
print("Preview of DataFrame:")
print(df.head(10))
print(df.tail(10))


# If you want to save the extracted data to a file
df.to_csv("output_filename.csv", index=False)
