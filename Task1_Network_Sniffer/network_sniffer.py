import argparse
from datetime import datetime

from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
def format_payload(raw_bytes, max_len=100):
    """Convert raw payload bytes into a safe, readable preview string."""
    if not raw_bytes:
        return "No payload"
    try:
        text = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        text = str(raw_bytes)
    text = text.replace("\n", "\\n").replace("\r", "\\r")
    if len(text) > max_len:
        text = text[:max_len] + "...(truncated)"
    return text


def process_packet(packet):
    """Callback executed for every captured packet."""
    if not packet.haslayer(IP):
        return  # Skip non-IP packets (ARP, etc.) for this basic sniffer

    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Determine protocol name and ports
    if packet.haslayer(TCP):
        proto = "TCP"
        sport = packet[TCP].sport
        dport = packet[TCP].dport
    elif packet.haslayer(UDP):
        proto = "UDP"
        sport = packet[UDP].sport
        dport = packet[UDP].dport
    elif packet.haslayer(ICMP):
        proto = "ICMP"
        sport = dport = "-"
    else:
        proto = f"Other (proto={ip_layer.proto})"
        sport = dport = "-"

    print("=" * 70)
    print(f"[{timestamp}] {proto} Packet")
    print(f"  Source IP:      {src_ip}:{sport}")
    print(f"  Destination IP: {dst_ip}:{dport}")
    print(f"  TTL:            {ip_layer.ttl}   Length: {len(packet)} bytes")

    if packet.haslayer(Raw):
        payload = packet[Raw].load
        print(f"  Payload:        {format_payload(payload)}")
    else:
        print("  Payload:        None")


def main():
    parser = argparse.ArgumentParser(description="Basic Network Sniffer (CodeAlpha Task 1)")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on (e.g. eth0, Wi-Fi)")
    parser.add_argument("-c", "--count", type=int, default=0,
                         help="Number of packets to capture (0 = infinite, stop with Ctrl+C)")
    parser.add_argument("-f", "--filter", default="",
                         help='BPF filter string, e.g. "tcp", "udp port 53", "icmp"')
    args = parser.parse_args()

    print("Starting Basic Network Sniffer...")
    print(f"Interface : {args.interface or 'default'}")
    print(f"Filter    : {args.filter or 'none (capturing all IP traffic)'}")
    print(f"Count     : {'infinite (Ctrl+C to stop)' if args.count == 0 else args.count}")
    print("-" * 70)

    try:
        sniff(
            iface=args.interface if args.interface else None,
            filter=args.filter if args.filter else None,
            prn=process_packet,
            count=args.count,
            store=False,
        )
    except PermissionError:
        print("\n[!] Permission denied. Try running with sudo/administrator privileges.")
    except KeyboardInterrupt:
        print("\n[!] Sniffing stopped by user.")


if __name__ == "__main__":
    main()