# Python code to extract text from a PDF
# Author:       Scott Rice
# Created:      2024-01-24

# Will need tika installed if not all ready.
#pip install tika
from tika import parser


raw = parser.from_file('Ulrich.pdf')

with open("ulrich.txt", "a") as file: # "a" appends text to the end of the exisitng file
    print(raw['content'], file=file)
