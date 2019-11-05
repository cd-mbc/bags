

import math

class Extension():

    def __init__(self, msg):
        self.msg = msg
        self.info = '  - dist(x,y): (float,float) -> float'

    def dist(self,x,y):
        return math.sqrt( (self.msg.pose.position.x - x)**2 + (self.msg.pose.position.y - y)**2 ) 



def extend(msg):
    msg.__class__.x = Extension(msg)
    return msg
