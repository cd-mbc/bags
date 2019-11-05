
from datetime import datetime

class BagTime(float):

    def __new__(cls, value):
        return super(BagTime, cls).__new__(cls, value)

    def __init__(self,value):
        super(BagTime, self).__init__()

        # additionally defined attributes
        self.datetime = datetime.fromtimestamp(value)
