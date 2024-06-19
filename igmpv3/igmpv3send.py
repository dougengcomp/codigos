from scapy.all import Ether, IP, UDP, Raw, sendp, conf

def send_igmpv3_query():
    # Craft IGMPv3 Query Packet
    igmp_query = (
        Ether(dst="01:00:5e:00:00:01") /
        IP(dst="224.0.0.1", options="\x00\x00\x00\x00", ttl=1, proto=2) /
        Raw(load=b'\x11\x64\xe4\x5f\x00\x00\x00\x00\x00\x0a\x3c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    )

    # Send packet on the default interface
    sendp(igmp_query, iface=conf.iface)

if __name__ == "__main__":
    send_igmpv3_query()
