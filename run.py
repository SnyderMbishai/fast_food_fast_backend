'''Run the application.'''
import os

from main import create_app

configuration = os.getenv('APP_SETTINGS')
app = create_app(configuration)
port=os.getenv('PORT')
app.run(debug=True, host='0.0.0.0', port=port)
