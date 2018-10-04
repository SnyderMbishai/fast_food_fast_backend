'''Run the application.'''
import os

from main import create_app
from api.v1.models import User
from api.v2.models.user_model import User as User2

# create super user without db
user = User(username='Administrator',
            password='pass400&', email='admin@admin.com')
user.roles.append('superuser')
user.save()

# create super user with db
user2 = User2(username='Administrator',
              password='pass400&', email='admin@admin.com')
if not User2.get(username='Administrator'):
    user2.add_user()
    super_id = User2.get(username='Administrator')[0]
    user2.assign_user_a_role('superuser', super_id)
else:
    pass

# run application
CONFIGURATION = os.getenv('APP_SETTINGS')
app = create_app(CONFIGURATION)
PORT = os.getenv('PORT')
app.run(debug=True)
