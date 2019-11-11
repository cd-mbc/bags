
import sys
import os
import multiprocessing as mp
import copy

import rosbag

from metax import BagTime
import utils
import db



def check_ndt_pose(bag,fname):

    position_max_x = None
    position_min_x = None
    position_max_y = None
    position_min_y = None 
    initilized = False   


    for topic, msg, t in bag.read_messages(topics='/ndt_pose'):
            
        if not initilized:
            position_max_x = copy.deepcopy(msg.pose.position.x)
            position_max_y = copy.deepcopy(msg.pose.position.y)
            position_min_x = copy.deepcopy(msg.pose.position.x)
            position_min_y = copy.deepcopy(msg.pose.position.y)
            initilized = True

        else:
            if position_max_x < msg.pose.position.x:
                position_max_x = copy.deepcopy(msg.pose.position.x)
            if position_max_y < msg.pose.position.y:
                position_max_y = copy.deepcopy(msg.pose.position.y)
            if position_min_x > msg.pose.position.x:
                position_min_x = copy.deepcopy(msg.pose.position.x)
            if position_min_y > msg.pose.position.y:
                position_min_y = copy.deepcopy(msg.pose.position.y)      

    ops = db.Ops()
    ops.add_ndt_pose(fname, position_max_x, position_max_y, position_min_x, position_min_y)
    
    if utils.is_debag():
        d = ops.get_ndt_pose(fname)
        print d.serialize


def check(fname):
    try:
        bag = rosbag.Bag(fname)
    except:
        # if the file is unrecognizable, ignore it
        return False

    check_ndt_pose(bag,fname)

    bag.close()



if __name__ == '__main__':

    target_directory = TARGET_DIRECTORY
    files = utils.rec_find_files( target_directory )

    for fname in files:
        check(fname)
