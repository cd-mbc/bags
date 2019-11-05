

import ndt_pose


class Extension:

    def __init__(self):
        self.info = 'no extension'


def extend(topic,msg):

    if topic=='/ndt_pose':
        return ndt_pose.extend(msg)
    else:
        msg.__class__.x = Extension()
        return msg