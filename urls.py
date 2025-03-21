from views import upload_file, get_data


def setup_routes(app):
    app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
    app.add_url_rule('/data', 'get_data', get_data, methods=['GET'])
