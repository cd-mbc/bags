
import sys
import os
import multiprocessing as mp

import rosbag

from metax import BagTime
import utils

def check(fname):
    try:
        bag = rosbag.Bag(fname)
    except:
        # if the file is unrecognizable, ignore it
        return False


    # variables available in filter
    start = BagTime( bag.get_start_time() )
    end = BagTime( bag.get_end_time() )
    comp = bag.get_compression_info()
    count = bag.get_message_count()
    size = bag.size
    ver = bag.version
    path = bag.filename
    types = bag.get_type_and_topic_info().msg_types
    topics = bag.get_type_and_topic_info().topics

    b_filter = FILTER
    if type(b_filter) != bool:
        print('Error: only boolean expression is allowed')
        sys.exit()

    bag.close()
    return b_filter
        

def check_files(files, worker_num, conn):

    num_found = 0
    for fname in files:
        
        if not utils.is_bagfile(fname):
            continue

        if check(fname):
            if utils.is_debag():
                print '%s, proc: %d' %(fname, worker_num)
            else:
                print '%s' %(fname)
            num_found += 1

    conn.send(num_found)
    conn.close()


if __name__ == '__main__':

    target_directory = TARGET_DIRECTORY
    files = utils.rec_find_files( target_directory )
    count_find = 0

    num_worker = utils.get_num_workers()
    file_assign = utils.assign_file(list(files), num_worker)

    procs = []
    pipes = []
    for assign in file_assign:
        worker_num = file_assign.index(assign)
        parent_conn, child_conn = mp.Pipe()
        proc = mp.Process(target=check_files, args=(assign,worker_num,child_conn))
        proc.start()
        procs.append(proc)
        pipes.append(parent_conn)

    for proc in procs:
        proc.join()

    for find in [conn.recv() for conn in pipes]:
        count_find += find

    print '%d files found.' %( count_find )