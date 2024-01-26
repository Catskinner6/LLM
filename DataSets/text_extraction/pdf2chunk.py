# pip install PyPDF2
# Ulrich_Beyond Make‐Buy_Internalization and Integration of Design and Production_2009.pdf
import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def preprocess_text(text):
    # Replace newlines and other unwanted characters
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text

def split_text_into_sections(text, section_size, overlap_size):
    words = text.split()
    sections = []
    start_idx = 0
    end_idx = section_size

    while start_idx < len(words):
        section = ' '.join(words[start_idx:end_idx])
        sections.append(section)

        start_idx = end_idx - overlap_size
        end_idx = start_idx + section_size

    return sections

def save_sections_to_files(sections, output_prefix='section'):
    for i, section in enumerate(sections):
        output_filename = f'{output_prefix}_{i + 1}.txt'
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(section)

if __name__ == "__main__":
    pdf_path = 'Ulrich_Beyond Make‐Buy_Internalization and Integration of Design and Production_2009.pdf'  # Replace with the path to your PDF file
    section_size = 3000
    overlap_size = 100

    pdf_text = extract_text_from_pdf(pdf_path)
    cleaned_text = preprocess_text(pdf_text)
    text_sections = split_text_into_sections(cleaned_text, section_size, overlap_size)
    save_sections_to_files(text_sections)
