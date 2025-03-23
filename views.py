from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from extension import cache
from config import Config
from models import db, VesterAi
from parsers.pdf_parser import parse_pdf
from parsers.pptx_parser import parse_pptx
from task import process_file

logging.basicConfig(level=logging.DEBUG)


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
    Handle file uploads, process the file, and save the extracted data to the database.

    Steps:
        1. Check if a file is included in the request.
        2. Validate the file name and extension.
        3. Save the file to the upload folder.
        4. Parse the file to extract slide titles, content, and metadata.
        5. Save the extracted data to the database.
        6. Clear the Redis cache to ensure fresh data is fetched next time.
        7. Return a success or error message.

    Error Messages:
        - "No file selected": No file was chosen for upload.
        - "Unsupported file format": The file is not a PDF or PowerPoint.
        - "File processing failed": Something went wrong while processing the file.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOADER_FOLDER, filename)
            file.save(file_path)

            # Enqueue the file processing task
            process_file.delay(file_path, filename)

            return jsonify({'message': 'Your file is being processed'}), 202

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error processing file: {str(e)}")
            return jsonify({'error': 'File processing failed'}), 500

    return jsonify({'error': 'Unsupported file format'}), 400


def get_data():
    """
    Retrieve all parsed slide data from the database and return it as a JSON response.

    Steps:
        1. Check if the data is available in the Redis cache.
        2. If cached data is found, return it.
        3. If no cached data is found, fetch data from the database.
        4. Store the fetched data in the Redis cache for future requests.
        5. Return the data as a JSON response.

    Error Messages:
        - "No data found": No files have been uploaded yet.
    """

    cached_data = cache.get('slides')
    if cached_data:
        return jsonify(cached_data), 200

    slides = VesterAi.query.all()
    if slides:
        slides_data = [{
            'filename': slide.filename,
            'slide_title': slide.slide_title,
            'slide_content': slide.slide_content,
            'slide_metadata': slide.slide_metadata if isinstance(slide.slide_metadata, dict) else {}
        } for slide in slides]

        cache.set('slides', jsonify(slides_data).get_data(as_text=True), ex=3600)
        return jsonify(slides_data), 200

    return jsonify({'error': 'No data found'}), 404
