# VesterAI Backend (Flask)

A Flask-based backend for parsing pitch deck documents (PDF or PowerPoint) and storing the extracted data in a PostgreSQL database. This project is part of the VesterAI Test.

---

## Features

- **File Upload**: Accepts PDF and PPTX files.
- **Data Parsing**: Extracts slide titles, text content, and metadata from uploaded files.
- **Data Storage**: Stores parsed data in a PostgreSQL database (hosted on Neon).
- **REST API**: Provides endpoints for file upload and data retrieval.
- **CORS Support**: Allows cross-origin requests for frontend integration.
- **Error Handling**: Handles unsupported file formats, corrupted files, and database errors.

---

## Prerequisites

- Python 3.9+
- Flask
- PyPDF2 (for PDF parsing)
- python-pptx (for PPTX parsing)
- SQLAlchemy (for database operations)
- Flask-CORS (for cross-origin requests)
- PostgreSQL (hosted on Neon)
- Docker (for containerization)

---

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/AfeezTemitope/VesterAi_backendFlask.git
   cd VesterAi_backendFlask
Set Up a Virtual Environment:

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Set Up Environment Variables:
Create a .env file in the root directory and add the following:

env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@neon-host/dbname
Replace user, password, neon-host, and dbname with your Neon PostgreSQL credentials.

Running the Application
Run the Flask Development Server:

flask run
Access the Application:

The API will be available at http://localhost:5000.

Use the /upload endpoint to upload files and the /data endpoint to retrieve parsed data.

API Documentation
Endpoints
1. Upload a File
URL: /upload

Method: POST

Description: Upload a PDF or PPTX file for parsing.

Request Body:

file: The file to upload (PDF or PPTX).

Response:

200 OK: File uploaded and parsed successfully.

400 Bad Request: Unsupported file format or missing file.

2. Retrieve Parsed Data
URL: /data

Method: GET

Description: Retrieve all parsed data from the database.

Response:

200 OK: JSON array of parsed data.

Testing
Unit Tests
Run Unit Tests:

pytest tests/ --cov=.
Test Coverage:

The --cov flag generates a coverage report to show how much of your code is tested.

Postman Tests
Import the Postman Collection:

Import the provided Postman collection to test the API endpoints.

Test Cases:

Upload a PDF File:

Method: POST

URL: http://localhost:5000/upload

Body: form-data with a PDF file.

Upload a PPTX File:

Method: POST

URL: http://localhost:5000/upload

Body: form-data with a PPTX file.

Retrieve Parsed Data:

Method: GET

URL: http://localhost:5000/data

Deployment
Deploying on Vercel
Install Vercel CLI:


npm install -g vercel
Deploy the Backend:

vercel
Set Environment Variables on Vercel:

Go to your Vercel dashboard.

Navigate to the project settings.

Add the following environment variables:

FLASK_APP=app.py

FLASK_ENV=production

DATABASE_URL=postgresql://user:password@neon-host/dbname

Access the Deployed API:

The API will be available at the URL provided by Vercel after deployment.

Docker
Build the Docker Image:

docker build -t vesterai .
Run the Docker Container:

docker run -p 5000:5000 vesterai
Access the Application:

The API will be available at http://localhost:5000.

Project Structure

VesterAi_backendFlask/
│
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── urls.py                 # URL routing
├── views.py                # Flask views/controllers
├── models.py               # Database models
├── parsers/                # Module for parsing PDF and PPTX files
│   ├── pdf_parser.py       # PDF parsing logic
│   └── pptx_parser.py      # PPTX parsing logic
├── storage/                # Folder to store uploaded files
├── tests/                  # Unit tests
│   ├── test_pdf_parser.py  # PDF parser tests
│   └── test_pptx_parser.py # PPTX parser tests
├── requirements.txt        # Python dependencies
├── Dockerfile              # Dockerfile for the Flask app
├── docker-compose.yml      # Docker Compose file for deployment
└── README.txt              # Documentation
Contributing
Fork the repository.

Create a new branch (git checkout -b feature/your-feature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/your-feature).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Flask for the web framework.

PyPDF2 and python-pptx for document parsing.

SQLAlchemy for database operations.

Neon for PostgreSQL hosting.

Vercel for deployment.

This README provides a comprehensive guide to setting up, testing, and deploying the VesterAI Backend. It also includes API documentation and project structure details for easy navigation.

