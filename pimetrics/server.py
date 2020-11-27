
from libs.listenersocket import ListenerSocket
from libs.tools.pathing import TEMP_DIR
import gzip
import shutil
import os

if __name__ == '__main__':

    # setup listener
    listener = ListenerSocket(4040, 1024)

    while True:

        file_location = listener.receive_metrics()
        # process the incoming file
        print(file_location)
        print("File Size: {} Bytes".format(os.stat(file_location).st_size))

        # - put it somewhere where the syslog daemon is reading from files into MySQL
        with gzip.open(file_location, 'rb') as gz_fp:
            # print into the file that is being read by rsyslog
            with open("/var/log/external/router/router.log", 'ab+') as r_fp:
                shutil.copyfileobj(gz_fp, r_fp, 1024)

        # delete the incoming file
        os.remove(file_location)
