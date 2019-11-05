

import os
import heapq as hq


# recursively find all files from designated directory
def rec_find_files(directory):
    for current, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(current, file)

def is_bagfile(path):
    return path[-(len('.bag')):] == '.bag'


def get_num_workers():
    if 'BAGSNUMPROC' in os.environ:
        return int( os.environ['BAGSNUMPROC'] )    
    else:
        return 1


def is_debag():
    if 'BAGSDEBUG' in os.environ:
        return bool(os.environ['BAGSDEBUG'])
    else:
        return False


def show_assign_info(file_assign):
    for worker in file_assign:
        for fname in worker:
            print '%s, proc: %d, size: %d' %(fname, file_assign.index(worker), os.path.getsize(fname))
                        

def assign_file(files, num_worker):
    bags_file_assign = 0
    if 'BAGSFILEASSIGN' in os.environ:
        bags_file_assign = int(os.environ['BAGSFILEASSIGN'])

    if bags_file_assign == 1:
        file_assign = assign_file_by_size(files, num_worker)
    else:
        file_assign = assign_file_naive(files, num_worker)

    if is_debag():
        show_assign_info(file_assign)

    return file_assign


def assign_file_naive(files, num_worker):  

    file_assign = [[] for i in range(len(files))]
    for i in range(len(files)):
        d = files[i]
        file_assign[i % num_worker].append(d)
    

    return file_assign   


def assign_file_by_size(files, num_worker):
    h = []
    for fname in files:
        hq.heappush(h, (os.path.getsize(fname), fname))

    file_assign = [[] for i in range(len(files))]
    for i in range(len(files)):
        d = hq.heappop(h)
        file_assign[i % num_worker].append(d[1])

    return file_assign