'''Run the application.'''
import os

from main import create_app

configuration = os.getenv('APP_SETTINGS')
app = create_app(configuration)
app.run(debug=True, host='0.0.0.0', port=5000)
