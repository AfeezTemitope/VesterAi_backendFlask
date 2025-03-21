from PyPDF2 import PdfReader


def parse_pdf(file_path):
    """Parse a PDF file and return a list of slides."""

    reader = PdfReader(file_path)
    slides = []
    for page in reader.pages:
        slides.append({
            'title': f'Slide {reader.get_page_number(page) + 1}',
            'content': page.extract_text(),
            'metadata': page.metadata
        })
    return slides
