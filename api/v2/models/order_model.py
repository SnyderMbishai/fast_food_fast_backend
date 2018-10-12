'''Orders model.'''

class Order(object):
    '''Order model.'''

    def __init__(self, user_id, meals_dict):
        '''
        Create an order.
        '''
        self.id = None
