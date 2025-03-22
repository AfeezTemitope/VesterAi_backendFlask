from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from config import Config
from models import db, VesterAi
from parsers.pdf_parser import parse_pdf
from parsers.pptx_parser import parse_pptx


def allowed_file(filename):
    """Check if the uploaded file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def upload_file():
    """Handle file uploads, parse the uploaded file, and save the parsed data to the database."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOADER_FOLDER, filename)
        file.save(file_path)

        # Parse the file based on its type
        slides = []
        try:
            if filename.endswith('.pdf'):
                slides = parse_pdf(file_path)
            elif filename.endswith('.pptx'):
                slides = parse_pptx(file_path)
            else:
                return jsonify({'error': 'Unsupported file format'}), 400
        except Exception as e:
            return jsonify({'error': f'There was an error processing your file. Please ensure it is a valid PDF: {str(e)}'}), 400

        for slide in slides:
            new_slide = VesterAi(
                filename=filename,
                slide_title=slide['title'],
                slide_content=slide['content'],
                slide_metadata=slide.get('metadata', {})
            )
            db.session.add(new_slide)
        db.session.commit()

        return jsonify({'message': 'File uploaded and parsed successfully'}), 200
    else:
        return jsonify({'error': 'Unsupported file format'}), 400


def get_data():
    """
    Retrieve all parsed slides from the database and return them as a JSON response.
    Returns:
    - jsonify: A list of parsed slide data including the filename, title, content, and metadata.
      - 200: Successful retrieval of slide data.
    """
    slides = VesterAi.query.order_by(VesterAi.id.desc()).first()
    return jsonify([{
        'filename': slide.filename,
        'slide_title': slide.slide_title,
        'slide_content': slide.slide_content,
        'slide_metadata': slide.metadata
    } for slide in slides]), 200
