import socket
import sys
import argparse
import concurrent.futures
from datetime import datetime


# Default port range if none is specified
DEFAULT_PORT_RANGE = "1-65535"
DEFAULT_TIMEOUT = 1.0
DEFAULT_WORKERS = 50


def resolve_target(target):
    """
    Resolve a hostname or IP string to an IP address.

    Prints an error and exits cleanly if the host cannot be resolved,
    handling socket.gaierror for invalid or unknown hostnames.
    """
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Could not resolve host: {target}")
        sys.exit(1)


def get_service_name(port):
    """
    Return the known service name for a port, or 'unknown'.
    """
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def scan_port(target_ip, port, timeout):
    """
    Attempt a TCP connection to a single port.

    Returns True if the port is open, False if closed, filtered,
    or if a socket error occurs. Handles socket.error gracefully
    without crashing.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((target_ip, port))
        sock.close()
        return result == 0
    except socket.error:
        sock.close()
        return False


def scan_ports_concurrent(target_ip, start_port, end_port, timeout, workers):
    """
    Scan a port range concurrently using a thread pool.

    Returns a sorted list of open (port, service_name) tuples.
    Concurrent scanning significantly reduces total scan time on
    large ranges where most ports are filtered or closed.
    """
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_port = {
            executor.submit(scan_port, target_ip, port, timeout): port
            for port in range(start_port, end_port + 1)
        }
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            if future.result():
                service = get_service_name(port)
                open_ports.append((port, service))
                print(f"[OPEN] Port {port}/tcp  ({service})")

    open_ports.sort(key=lambda item: item[0])
    return open_ports


def print_summary(open_ports, start_port, end_port, elapsed):
    """Print a final summary of scan results."""
    total = end_port - start_port + 1
    print("-" * 50)
    print(f"[+] Scan complete in {elapsed:.2f}s")
    print(f"[+] Scanned {total} port(s) | Open: {len(open_ports)}")

    if open_ports:
        print("\n[+] Open ports summary:")
        for port, service in open_ports:
            print(f"    {port}/tcp  ({service})")
    else:
        print("[+] No open ports found in the specified range.")


def parse_port_range(port_range_str):
    """
    Parse a port range string in START-END format.

    Returns (start, end) as integers, or exits on invalid input.
    """
    try:
        parts = port_range_str.split("-")
        start = int(parts[0])
        end = int(parts[1])
        if not (1 <= start <= end <= 65535):
            raise ValueError
        return start, end
    except (ValueError, IndexError):
        print(f"[!] Invalid port range '{port_range_str}'. Use format: START-END (e.g. 1-1024)")
        sys.exit(1)


def main():
    """Main entry point: parse arguments and run the port scan."""
    parser = argparse.ArgumentParser(
        description="TCP port scanner using the Python standard library."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Target IP address or hostname to scan."
    )
    parser.add_argument(
        "-p", "--ports",
        default=DEFAULT_PORT_RANGE,
        help=f"Port range to scan (default: {DEFAULT_PORT_RANGE})"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout per port in seconds (default: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Number of concurrent threads (default: {DEFAULT_WORKERS})"
    )

    args = parser.parse_args()

    # Get target from argument or prompt
    target = args.target
    if target is None:
        try:
            target = input("Enter target IP address or hostname: ").strip()
        except EOFError:
            print("[!] No target provided. Exiting.")
            sys.exit(1)

    if not target:
        print("[!] No target provided. Exiting.")
        sys.exit(1)

    target_ip = resolve_target(target)

    if target_ip != target:
        print(f"[+] Resolved {target} -> {target_ip}")

    start_port, end_port = parse_port_range(args.ports)

    print("=" * 50)
    print(f"  TCP Port Scanner  |  Target: {target_ip}")
    print("=" * 50)
    print(f"[+] Range: {start_port}-{end_port}")
    print(f"[+] Timeout: {args.timeout}s  |  Threads: {args.workers}")
    print(f"[+] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    start_time = datetime.now()

    try:
        open_ports = scan_ports_concurrent(
            target_ip, start_port, end_port, args.timeout, args.workers
        )
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit(1)

    elapsed = (datetime.now() - start_time).total_seconds()
    print_summary(open_ports, start_port, end_port, elapsed)


if __name__ == "__main__":
    main()
