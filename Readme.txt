---

**VesterAI Backend (Flask)**

A Flask-based backend for parsing pitch deck documents (PDF or PowerPoint) and storing the extracted data in a PostgreSQL database. This project is part of the VesterAI Test.

---

**Features**
- File upload: Accepts PDF and PPTX files.
- Data parsing: Extracts slide titles, text content, and metadata from uploaded files.
- Data storage: Stores parsed data in a PostgreSQL database (hosted on Neon).
- REST API: Provides endpoints for file upload and data retrieval.
- CORS support: Allows cross-origin requests for frontend integration.
- Error handling: Handles unsupported file formats, corrupted files, and database errors.

---

**Prerequisites**
- Python 3.9+, Flask, PyPDF2, python-pptx, SQLAlchemy, Flask-CORS.
- PostgreSQL (hosted on Neon).
- Docker (for containerization).

---

**Installation**
1. Clone repository and set up virtual environment:
   - `git clone https://github.com/AfeezTemitope/VesterAi_backendFlask.git && cd VesterAi_backendFlask`.
   - Activate virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # Windows: venv\Scripts\activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add `.env` file with:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://user:password@neon-host/dbname
   ```
---

**Running**
Start Flask development server:
```bash
flask run
```
Access at `http://localhost:5000`.

---

**API Documentation**
1. **Upload File** - POST `/upload`
   - Upload PDF or PPTX for parsing.
   - 200 OK (success), 400 Bad Request (invalid file).
2. **Retrieve Data** - GET `/data`
   - Retrieve parsed data from the database.

---

**Testing**
Run unit tests:
```bash
pytest tests/ --cov=.
```
Use Postman for API testing (upload and retrieve parsed data).

---

**Deployment**
**Vercel**
- Install CLI:
  ```bash
  npm install -g vercel
  vercel
  ```
- Add environment variables via Vercel dashboard.


**Docker**
- Build and run Docker image:
  ```bash
  docker build -t vester .
  docker run -p 5000:5000 vester
  ```

---

**Structure**
```
VesterAi_backendFlask/
├── app.py
├── config.py
├── urls.py
├── views.py
├── models.py
├── parsers/
│   ├── pdf_parser.py
│   └── pptx_parser.py
├── storage/
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.txt
```

---

**Contributing**
1. Fork, create branch, commit changes, push, open pull request.
2. Follow PEP 8 and include unit tests.

---

**License**
MIT License.

---

**Acknowledgments**
Thanks to Flask, PyPDF2, python-pptx, SQLAlchemy, Neon, and Vercel.

---