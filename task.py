from celery import Celery
from parsers.pdf_parser import parse_pdf
from parsers.pptx_parser import parse_pptx
from models import db, VesterAi
from extension import cache

app = Celery('task', broker='redis://localhost:6379/0')


@app.task
def process_file(file_path, filename):
    """Background task to process the uploaded file."""
    slides = []
    if filename.endswith('.pdf'):
        slides = parse_pdf(file_path)
    elif filename.endswith('.pptx'):
        slides = parse_pptx(file_path)

    # Delete all existing records in the VesterAi table
    db.session.query(VesterAi).delete()
    db.session.commit()

    # Insert new slides into the database
    for slide in slides:
        new_slide = VesterAi(
            filename=filename,
            slide_title=slide['title'],
            slide_content=slide['content'],
            slide_metadata=slide.get('metadata', {})
        )
        db.session.add(new_slide)
        db.session.commit()

    cache.delete('slides')
