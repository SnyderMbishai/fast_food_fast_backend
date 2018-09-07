'''Run the application.'''
import os

from main import create_app

configuration = os.getenv('APP_SETTINGS')
app = create_app(configuration)
app.run(debug=True, host='127.0.0.1', port=5000)