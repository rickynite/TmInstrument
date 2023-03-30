import socket
import threading
import numpy as np

class TmInstrumentServer:
    def __init__(self, host='127.0.0.1', port=5025):
        """
        Initializes an instance of the EmulatedZNB20 class.

        :param host: The IP address of the emulated instrument. Defaults to '127.0.0.1'.
        :param port: The TCP port number to use for the emulated instrument. Defaults to 5025.
        """
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        self.client_socket = None

        # A dictionary of supported commands and their corresponding responses or functions
        self.commands = {
            "*IDN?": "Rohde&Schwarz,ZNB20,123456,1.00",
            "*OPC?": "1",
            "*STB?": "0",
            "CALC:DATA? SDATA": self.generate_s11_data,
        }

    def generate_s11_data(self):
        num_points = 201
        s11_data = np.random.rand(num_points, 2)
        s11_data_str = ','.join([f"{x:.6e},{y:.6e}" for x, y in s11_data])
        return s11_data_str

    def process_command(self, command):
        response = self.commands.get(command)
        if response is not None:
            if callable(response):
                response = response()
            return response
        else:
            return None

    def start(self):
        self.running = True
        self.server = threading.Thread(target=self.run_server)
        self.server.start()

    def stop(self):
        self.running = False
        if self.server:
            self.server.join()

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Emulated VNA connection closed")
            
    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            while self.running:
                conn, addr = s.accept()
                self.client_socket = conn  # set the client socket
                with conn:
                    while self.running:
                        data = conn.recv(1024)
                        if not data:
                            break
                        command = data.decode('utf-8').strip()
                        if command == "DummyServer.stop":
                            self.running = False
                        response = self.process_command(command)
                        if response is not None:
                            conn.sendall((response + '\n').encode('utf-8'))
