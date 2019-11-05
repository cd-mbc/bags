
import rosbag

import datax
import utils


def check(fname):
    try:
        bag = rosbag.Bag(fname)
    except:
        # if the file is unrecognizable, ignore it
        return False

    found = False
    topic_name = TOPIC
    for topic, msg, t in bag.read_messages(topics=topic_name):

        msg = datax.extend(topic,msg)
        print '[File name]\n%s\n' %(fname)
        print '[Message format]\n%s\n' %(msg)
        print '[Extension info]\n%s' %(msg.x.info)
        found = True
        break

    bag.close() 
    return found
        

if __name__ == '__main__':

    target_directory = TARGET_DIRECTORY
    files = utils.rec_find_files( target_directory )
    found = False
    for fname in files:
        if not utils.is_bagfile(fname):
            continue

        if check(fname):
            found = True
            break

    if not found:
        print 'topic not found.'