
import sys
import os
import multiprocessing as mp
import time
import copy

import rosbag

import datax
import utils


def check(fname, worker_num):
    try:
        bag = rosbag.Bag(fname)
    except:
        # if the file is unrecognizable, ignore it
        return False

    if utils.is_debag():
        print 'start checking: %s, ptoc: %d, at: %f' %(fname, worker_num, time.time())

    found = False
    topic_name = TOPIC

    debug_started = False  
    for topic, msg, t in bag.read_messages(topics=topic_name):

        msg = datax.extend(topic,msg)

        b_filter = FILTER
        if type(b_filter) != bool:
            print('Error: only boolean expression is allowed')
            sys.exit()        

        if b_filter:
            found = True
            break

    bag.close()   

    return found


def check_files(files, worker_num, conn):

    num_found = 0
    for fname in files:
        
        if not utils.is_bagfile(fname):
            continue

        if check(fname, worker_num):
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