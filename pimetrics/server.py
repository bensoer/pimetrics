
from libs.listenersocket import ListenerSocket
import gzip
import shutil
import os
import configparser

from libs.tools.pathing import PROJECT_ROOT_DIR

if __name__ == '__main__':

    # get config info
    config = configparser.ConfigParser()
    config.read(PROJECT_ROOT_DIR + os.sep + "pimetrics.conf.ini")

    listener_port = config["server"].getint("listenerport")
    rsyslog_file_path = config["server"]["rsyslogfilepath"]

    # setup listener
    listener = ListenerSocket(listener_port, 1024)

    while True:

        file_location = listener.receive_metrics()
        # process the incoming file
        print(file_location)
        print("File Size: {} Bytes".format(os.stat(file_location).st_size))

        # - put it somewhere where the syslog daemon is reading from files into MySQL
        with gzip.open(file_location, 'rb') as gz_fp:
            # print into the file that is being read by rsyslog
            with open(rsyslog_file_path, 'ab+') as r_fp:
                shutil.copyfileobj(gz_fp, r_fp, 1024)

        # delete the incoming file
        os.remove(file_location)
