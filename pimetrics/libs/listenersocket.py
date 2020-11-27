__author__ = 'bensoer'

import os
import socket
import traceback

from pimetrics.libs.tools.pathing import TEMP_DIR


class ListenerSocket:

    __buffer_size = 1024

    __listener_socket = None

    def __init__(self, port: int, buffer_size: int):

        self.__buffer_size = buffer_size
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind(('', port))
        listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        listener_socket.listen(1)
        self.__listener_socket = listener_socket

        print("Listener Socket Initialized")

    def receive_metrics(self)-> str:

        connection, client_address = self.__listener_socket.accept()

        tmp_file_path = TEMP_DIR + os.sep + "metrics.tar.gz"
        # delete any existing temp file if there is one first
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

        fp = open(tmp_file_path, "wb+")

        try:
            while True:
                # received file will be a .tar.gz
                data = connection.recv(self.__buffer_size)
                if data:
                    fp.write(data)
                else:
                    break
        except Exception as e:
            traceback.print_exc()
            print(e)
        finally:
            connection.close()
            fp.flush()
            fp.close()

        return tmp_file_path

