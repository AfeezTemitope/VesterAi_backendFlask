import unittest
from flask import Flask
from werkzeug.datastructures import FileStorage
from models import db, VesterAi
from tests.test_pdf_parser import create_sample_pdf
from views import upload_file, get_data


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up a Flask test client and an in-memory database."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['UPLOAD_FOLDER'] = 'tests/uploads'
        self.app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'pptx'}
        db.init_app(self.app)

        self.app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
        self.app.add_url_rule('/get_data', 'get_data', get_data, methods=['GET'])

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up the in-memory database."""
        with self.app.app_context():
            db.drop_all()

    def test_upload_file_valid_pdf(self):
        """Test uploading a valid PDF file."""
        sample_pdf_path = 'tests/sample.pdf'
        create_sample_pdf(sample_pdf_path)

        with open(sample_pdf_path, 'rb') as pdf:
            data = {'file': (pdf, 'sample.pdf')}
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertIn('File uploaded and parsed successfully', response.get_json()['message'])

    def test_upload_file_invalid_format(self):
        """Test uploading a file with an unsupported format."""
        with open('tests/invalid.txt', 'w') as invalid_file:
            invalid_file.write("Not a valid file format")

        with open('tests/invalid.txt', 'rb') as invalid:
            data = {'file': (invalid, 'invalid.txt')}
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported file format', response.get_json()['error'])

    def test_get_data(self):
        """Test retrieving the most recent parsed slide data."""
        with self.app.app_context():
            # Add mock slide data to the database
            new_slide = VesterAi(
                filename='sample.pdf',
                slide_title='Slide 1',
                slide_content='Sample PDF content for test',
                slide_metadata={'key': 'value'}  # Example metadata
            )
            db.session.add(new_slide)
            db.session.commit()

            # Call the GET endpoint
            response = self.client.get('/get_data')
            self.assertEqual(response.status_code, 200)

            # Verify the response JSON
            slide = response.get_json()
            self.assertEqual(slide['filename'], 'sample.pdf')
            self.assertEqual(slide['slide_title'], 'Slide 1')
            self.assertEqual(slide['slide_content'], 'Sample PDF content for test')
            self.assertEqual(slide['slide_metadata'], {'key': 'value'})

    def test_get_data_empty_db(self):
        """Test retrieving slide data when the database is empty."""
        response = self.client.get('/get_data')
        self.assertEqual(response.status_code, 404)
        self.assertIn('No slide data found', response.get_json()['error'])


if __name__ == '__main__':
    unittest.main()
