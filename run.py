'''Run the application.'''
import os

from main import create_app
from api.v1.models import User

#create a super user
user = User(username='Administrator',password='pass400&', email='admin@admin.com')
user.roles.append('superuser')
user.save()

configuration = os.getenv('APP_SETTINGS')
app = create_app(configuration)
port=os.getenv('PORT')
app.run(debug=True, host='0.0.0.0', port=port)
