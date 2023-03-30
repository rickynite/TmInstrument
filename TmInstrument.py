import time
from RsInstrument import *

class TmInstrument(RsInstrument):
    def send_command_sequence(self, commands, sequence_title = "Command Sequence", max_lines=5, max_row_length=[]):
        #if not self._isOpen:
        #self.open_connection()
        # Get instrument identification string
        idn = self.query("*IDN?")
        if not max_row_length:
            max_row_length = len("Connected to:      %s" % idn)
        print(sequence_title.center(max_row_length, "-"))
        print("Connected to:      %s" % idn)
        responses = []
        for cmd in commands:
            # Print the command prompt
            print("> %s" % cmd)
            if "?" in cmd:
                response = self.query(cmd)
                responses.append(response)
            else:
                self.write(cmd)
                response = ""
            # Print the command output
            lines = response.strip().split("\n")
            total_lines = 0
            new_lines = []
            for line in lines:
                while len(line) > max_row_length:
                    new_lines.append(line[:max_row_length])
                    line = line[max_row_length:]
                    total_lines += 1
                    if total_lines >= max_lines:
                        new_lines[-1] = new_lines[-1][:max_row_length-4] + " ..."
                        break
                if total_lines >= max_lines:
                    break
                new_lines.append(line)
                total_lines += 1
                if total_lines >= max_lines:
                    new_lines[-1] = new_lines[-1][:max_row_length-4] + " ..."
                    break
            for line in new_lines:
                print(line)
            #self.wait_for_srq()
            time.sleep(1)
        # Print disconnect message with timestamp
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Disconnected from: %s" % idn)
        timestamp_str = "%s" % now
        print(timestamp_str.center(max_row_length, "-"))
        self.close()
        return responses
