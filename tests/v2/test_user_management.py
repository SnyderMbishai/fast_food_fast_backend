"""Test the user management funciton."""
from json import loads, dumps

from tests.v2.base import BaseCase

MNG_URL = '/api/v2/users/manage/1'
class TestUserManagement(BaseCase):
    '''Test promoting a user.'''
    def test_user_can_be_promoted(self):
        #create user
        response = self.client.post(
            '/api/v2/users/signup', data=self.user_data_1)
        #confirm creation
        self.assertEqual(201, response.status_code)
        #get super user token
        token = self.get_super_user_token()
        headers = {'Authorization':'Bearer {}'.format(token)}
        #test user promoted
        response = self.client.put(MNG_URL, headers=headers)
        self.assertEqual(response.status_code,200)
        #test promoting non user
        response = self.client.put('/api/v2/users/manage/10', headers=headers)
        expected = {'message':"User was not found!"}
        self.assertEqual(expected, loads(response.data))
        self.assertEqual(404,response.status_code)
