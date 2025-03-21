from PyPDF2 import PdfReader


def parse_pdf(file_path):
    """Parse a PDF file and return a list of slides.

    Args:
        file_path (str): The path to the PDF file to be parsed.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing the title, content,
        and metadata of the slides in the PDF.
    """
    reader = PdfReader(file_path)
    slides = []

    # Extract metadata from the PDF file
    metadata = reader.metadata or {}  # Fallback to empty dict if not available

    for page_number, page in enumerate(reader.pages):
        slides.append({
            'title': f'Slide {page_number + 1}',
            'content': page.extract_text() or '',
            'slide_metadata': metadata
        })

    return slides
