
import sys
import os
import multiprocessing as mp

import rosbag

from metax import BagTime
import utils
import db


def check(fname):
    ops = db.Ops()
    ndt_pose = ops.get_ndt_pose(fname).serialize

    b_filter = FILTER
    if type(b_filter) != bool:
        print('Error: only boolean expression is allowed')
        sys.exit()

    return b_filter



if __name__ == '__main__':

    ops = db.Ops()
    files = [f.name for f in ops.get_file_all()]
    for fname in files:
        if check(fname):
            print fname