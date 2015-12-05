#/usr/bin/env python

__doc__ = """

    LLMNR Query ,
                    by Her0in

"""

import socket, struct

class LLMNR_Query:
    def __init__(self,name):
        self.name = name

        self.IsIPv4 = True
        self.populate()
    def populate(self):
        self.HOST = '224.0.0.252' if self.IsIPv4 else 'FF02::1:3'
        self.PORT = 5355
        self.s_family = socket.AF_INET if self.IsIPv4 else socket.AF_INET6

        self.QueryType = "IPv4"
        self.lqs = socket.socket(self.s_family, socket.SOCK_DGRAM)

        self.QueryData = (
        "\xa9\xfb"  # Transaction ID
        "\x00\x00"  # Flags Query(0x0000)? or Response(0x8000) ?
        "\x00\x01"  # Question
        "\x00\x00"  # Answer RRS
        "\x00\x00"  # Authority RRS
        "\x00\x00"  # Additional RRS
        "LENGTH"    # length of Name
        "NAME"      # Name
        "\x00"      # NameNull
        "TYPE"      # Query Type ,IPv4(0x0001)? or IPv6(0x001c)?
        "\x00\x01") # Class
        namelen = len(self.name)
        self.data = self.QueryData.replace('LENGTH', struct.pack('>B', namelen))
        self.data = self.data.replace('NAME', struct.pack(">"+str(namelen)+"s", self.name))
        self.data = self.data.replace("TYPE",  "\x00\x01" if self.QueryType == "IPv4" else "\x00\x1c")

    def Query(self):
        while(True):
            print "LLMNR Querying... -> %s" % self.name
            self.lqs.sendto(self.data, (self.HOST, self.PORT))
        self.lqs.close()

if __name__ == "__main__":
    llmnr = LLMNR_Query("Wooyun")
    llmnr.Query()
