
import os
from libs.clientsocket import ClientSocket
from libs.tools.pathing import PROJECT_ROOT_DIR


if __name__ == '__main__':

    # spawn connection to server
    client_socket = ClientSocket(4040, "127.0.0.1", 1024)

    # check for new files
    files_for_upload = list()
    for file in os.listdir("/var/log/external"):
        full_path = "/var/log/external" + os.sep + file
        if os.path.isfile(full_path) and file.endswith(".gz"):
            files_for_upload.append(full_path)

    # upload them
    for file_for_upload in files_for_upload:
        print("Uploading: {}".format(file_for_upload))
        print("File Size: {} Bytes".format(os.stat(file_for_upload).st_size))
        client_socket.send_metrics(file_for_upload)
        # then delete them locally
        os.remove(file_for_upload)



