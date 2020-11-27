__author__ = 'bensoer'

import socket


class ClientSocket:

    __buffer_size = 1024
    __port = 4040
    __ip = 'localhost'

    def __init__(self, port: int, ip: str, buffer_size: int):

        self.__buffer_size = buffer_size
        self.__port = port
        self.__ip = ip


        print("Client Socket Initialized")

    def send_metrics(self, absolute_file_path: str):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client_socket.connect((self.__ip, self.__port))

        fp = open(absolute_file_path, 'rb')

        buffer = fp.read(self.__buffer_size)
        while buffer:

            client_socket.sendall(buffer)
            buffer = fp.read(self.__buffer_size)

        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()



