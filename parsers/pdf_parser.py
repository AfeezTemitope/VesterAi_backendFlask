from PyPDF2 import PdfReader


def parse_pdf(file_path):
    """Parse a PDF file and return a list of slides.

    Args:
        file_path (str): The path to the PDF file to be parsed.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing the title,
        content, and metadata of the slides in the PDF.
    """
    reader = PdfReader(file_path)
    slides = []

    metadata = reader.metadata or {}

    metadata_dict = {key: metadata[key] for key in metadata}

    for page_number, page in enumerate(reader.pages):
        slides.append({
            'title': f'Slide {page_number + 1}',
            'content': page.extract_text() or '',
            'slide_metadata': metadata_dict
        })

    return slides
