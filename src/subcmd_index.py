
import sys
import os
import multiprocessing as mp

import rosbag

from metax import BagTime
import utils
import db







if __name__ == '__main__':


    ndt_pose = db.FNdtPose()

    b_filter = FILTER
    if type(b_filter) != set:
        print('Error: invalid filter')
        sys.exit()

    for fname in list(b_filter):
        print fname