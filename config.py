import os


class Config:
    # file upload settings
    UPLOADER_FOLDER = os.getenv('UPLOAD_FOLDER', 'storage/uploads')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,pptx').split(','))
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 16 * 1024 * 1024))

    # database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_DB_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ensuring upload folder exists
    if not os.path.exists(UPLOADER_FOLDER):
        os.makedirs(UPLOADER_FOLDER)
