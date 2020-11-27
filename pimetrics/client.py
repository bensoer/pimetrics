
import os
from libs.clientsocket import ClientSocket
from libs.tools.pathing import PROJECT_ROOT_DIR
import configparser


if __name__ == '__main__':

    # get config info
    config = configparser.ConfigParser()
    config.read(PROJECT_ROOT_DIR + os.sep + "pimetrics.conf.ini")

    server_ip = config["client"].get("serverip", "127.0.0.1")
    server_port = config["client"].getint("serverport")
    folder_path = config["filepoll"]["folderpath"]

    # spawn connection to server
    client_socket = ClientSocket(server_port, server_ip, 1024)

    # check for new files
    files_for_upload = list()
    for file in os.listdir(folder_path):
        full_path = folder_path + os.sep + file
        if os.path.isfile(full_path) and file.endswith(".gz"):
            files_for_upload.append(full_path)

    # upload them
    for file_for_upload in files_for_upload:
        print("Uploading: {}".format(file_for_upload))
        print("File Size: {} Bytes".format(os.stat(file_for_upload).st_size))
        client_socket.send_metrics(file_for_upload)
        # then delete them locally
        os.remove(file_for_upload)



