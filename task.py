import os

from celery import Celery
from parsers.pdf_parser import parse_pdf
from parsers.pptx_parser import parse_pptx
from models import db, VesterAi
from extension import redis_client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery app using Redis URL from config
app = Celery('task', broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))


@app.task
def process_file(file_path, filename):
    """
    Background task to process an uploaded file and store its data.

    Args:
        file_path (str): Path to the uploaded file on disk.
        filename (str): Name of the uploaded file.

    Process:
        1. Parse the file (PDF or PPTX) to extract slides.
        2. Clear existing VesterAi records from the database.
        3. Save parsed slides to the database.
        4. Clear the Redis cache for slides.
    """
    slides = []
    try:
        if filename.endswith('.pdf'):
            slides = parse_pdf(file_path)
        elif filename.endswith('.pptx'):
            slides = parse_pptx(file_path)
        logger.info(f"Parsed {len(slides)} slides from {filename}")
    except Exception as e:
        logger.error(f"Error parsing file {filename}: {e}")
        return

    try:
        db.session.query(VesterAi).delete()
        db.session.commit()
        logger.info("Cleared existing VesterAi records")
    except Exception as e:
        logger.error(f"Error clearing database: {e}")
        db.session.rollback()
        return

    for slide in slides:
        try:
            new_slide = VesterAi(
                filename=filename,
                slide_title=slide['title'],
                slide_content=slide['content'],
                slide_metadata=slide.get('metadata', {})
            )
            db.session.add(new_slide)
            db.session.commit()
            logger.info(f"Saved slide '{slide['title']}' from {filename}")
        except Exception as e:
            logger.error(f"Error saving slide from {filename}: {e}")
            db.session.rollback()
            return

    try:
        redis_client.delete('slides')
        logger.info("Cleared Redis cache for slides")
    except Exception as e:
        logger.error(f"Error clearing Redis cache: {e}")
