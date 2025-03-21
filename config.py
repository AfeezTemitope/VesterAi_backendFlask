import os


class Config:
    # file upload settings
    UPLOADER_FOLDER = 'storage/uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16mb

    # database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ensuring upload folder exists
    if not os.path.exists(UPLOADER_FOLDER):
        os.makedirs(UPLOADER_FOLDER)
