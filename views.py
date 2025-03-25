import json
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from config import Config
from models import db, VesterAi
from task import process_file
from extension import redis_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def allowed_file(filename):
    """
    Check if the uploaded file has a valid extension (PDF or PowerPoint).

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is a PDF or PowerPoint, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def upload_file():
    """
    Handle file uploads and enqueue processing in the background.

    Steps:
        1. Validate the presence and name of the file in the request.
        2. Check if the file extension is allowed.
        3. Save the file to the upload folder.
        4. Enqueue a Celery task to process the file.
        5. Return a response indicating processing has started.

    Returns:
        JSON response with a message and HTTP status:
        - 202: File accepted for processing.
        - 400: Invalid file or no file selected.
        - 500: Error saving the file.
    """
    if 'file' not in request.files:
        logger.warning("No file selected in request")
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['file']

    if file.filename == '':
        logger.warning("Empty filename in request")
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOADER_FOLDER, filename)
            file.save(file_path)
            logger.info(f"Saved file {filename} to {file_path}")

            # Enqueue the file processing task
            process_file.delay(file_path, filename)
            logger.info(f"Enqueued processing for {filename}")

            return jsonify({'message': 'Your file is being processed'}), 202
        except Exception as e:
            logger.error(f"Error saving file {filename}: {e}")
            return jsonify({'error': 'File processing failed'}), 500

    logger.warning(f"Unsupported file format: {file.filename}")
    return jsonify({'error': 'Unsupported file format'}), 400


def get_data():
    """
    Retrieve all parsed slide data, with fallback to process if not found.

    Steps:
        1. Check Redis cache for slide data.
        2. If cached, return it.
        3. If not cached, fetch from the database.
        4. If no data in database, attempt to process a default file (if configured).
        5. Cache the result in Redis with a 1-hour expiration.
        6. Return the data as JSON.

    Returns:
        JSON response with slide data (200) or error message (404).
    """

    SLIDES_CACHE_KEY = 'slides'

    try:
        cached_data = redis_client.get(SLIDES_CACHE_KEY)
        if cached_data:
            logger.info("Returning cached slide data")
            return jsonify(json.loads(cached_data)), 200
    except Exception as e:
        logger.error(f"Failed to fetch from Redis: {e}")

    slides = VesterAi.query.all()
    if slides:
        slides_data = [{
            'filename': slide.filename,
            'slide_title': slide.slide_title,
            'slide_content': slide.slide_content,
            'slide_metadata': slide.slide_metadata if isinstance(slide.slide_metadata, dict) else {}
        } for slide in slides]

        try:
            redis_client.setex(SLIDES_CACHE_KEY, 3600, json.dumps(slides_data))
            logger.info("Cached slide data in Redis with 1-hour expiration")
        except Exception as e:
            logger.error(f"Failed to cache in Redis: {e}")

        return jsonify(slides_data), 200
    else:
        # Fallback: Attempt to process a default file if configured
        default_file = os.environ.get('DEFAULT_FILE_PATH')  # Set this in Vercel env if needed
        if default_file and os.path.exists(default_file):
            filename = os.path.basename(default_file)
            if allowed_file(filename):
                try:
                    process_file.delay(default_file, filename)
                    logger.info(f"Enqueued default file {filename} for processing")
                    return jsonify({'message': 'No data found, processing default file'}), 202
                except Exception as e:
                    logger.error(f"Error enqueuing default file {filename}: {e}")

        logger.warning("No slide data found in database or default file")
        return jsonify({'error': 'No data found'}), 404
