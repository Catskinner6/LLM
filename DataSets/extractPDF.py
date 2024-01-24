# Python code to extract text from a PDF
# Author:       Scott Rice
# Created:      2024-01-24

from tika import parser


raw = parser.from_file('sample.pdf')

with open("output.txt", "a") as file:
    print(raw['content'], file=file)
