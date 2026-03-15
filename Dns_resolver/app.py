#!/usr/bin/env python3
"""
DNS Resolver - Built from scratch to understand DNS protocol deeply
Author: For learning and interview preparation
Python Version: 3.12+

This resolver performs iterative DNS queries starting from root nameservers,
following the DNS hierarchy: Root → TLD → Authoritative nameservers

Key concepts implemented:
- DNS message format (RFC 1035)
- Binary protocol parsing
- DNS compression (pointer following)
- Iterative resolution
- Multiple record types (A, AAAA, NS, CNAME)
"""

import socket
import struct
import random
from typing import List, Tuple, Optional

from data_structure import CLASS_IN, ROOT_SERVERS, TYPE_A, TYPE_AAAA, TYPE_CNAME, TYPE_NS, DNSHeader, DNSQuestion, DNSRecord




# =============================================================================
# DNS MESSAGE ENCODING
# =============================================================================

def encode_dns_name(domain: str) -> bytes:
    """
    Encode a domain name into DNS wire format.
    
    Example: "google.com" becomes:
    - 6 (length of "google")
    - "google" (6 bytes)
    - 3 (length of "com")
    - "com" (3 bytes)
    - 0 (null terminator)
    
    Args:
        domain: Domain name like "google.com"
    
    Returns:
        Encoded bytes
    """
    encoded = b""
    for part in domain.split("."):
        if part:  # Skip empty parts
            encoded += bytes([len(part)]) + part.encode("ascii")
    encoded += b"\x00"  # Null terminator
    return encoded


def build_query(domain: str, record_type: int = TYPE_A) -> bytes:
    """
    Build a DNS query packet.
    
    Structure:
    1. Header (12 bytes)
    2. Question section (variable length)
    
    Args:
        domain: Domain to query (e.g., "google.com")
        record_type: Type of record to query (default: A record)
    
    Returns:
        Complete DNS query packet as bytes
    """
    # Generate random 16-bit ID to match response
    query_id = random.randint(0, 65535)
    
    # FLAGS field breakdown:
    # QR (1 bit): 0 for query, 1 for response
    # Opcode (4 bits): 0 for standard query
    # AA (1 bit): Authoritative Answer (only in responses)
    # TC (1 bit): Truncated
    # RD (1 bit): Recursion Desired - we set to 0 (iterative query)
    # RA (1 bit): Recursion Available (only in responses)
    # Z (3 bits): Reserved, must be 0
    # RCODE (4 bits): Response code (only in responses)
    #
    # For our query: 0000 0000 0000 0000 = 0x0000
    # We want iterative resolution, so RD=0
    flags = 0x0000
    
    # Build header: ID, FLAGS, QDCOUNT=1, others=0
    # Format: '>HHHHHH' means:
    # > = big-endian (network byte order)
    # H = unsigned short (2 bytes) x 6 = 12 bytes total
    header = struct.pack(">HHHHHH", query_id, flags, 1, 0, 0, 0)
    
    # Build question section
    question = encode_dns_name(domain)
    question += struct.pack(">HH", record_type, CLASS_IN)
    
    return header + question


# =============================================================================
# DNS MESSAGE DECODING
# =============================================================================

def decode_dns_name(data: bytes, offset: int) -> Tuple[str, int]:
    """
    Decode a domain name from DNS message, handling compression.
    
    DNS Compression: To save space, domain names can use pointers.
    If a length byte has its top 2 bits set (0xC0), it's a pointer.
    The pointer is a 2-byte offset to another location in the message.
    
    Example:
    - 0x06 google 0x03 com 0x00  (normal encoding)
    - 0xC0 0x0C  (pointer to offset 12)
    
    Args:
        data: Full DNS message
        offset: Current position in message
    
    Returns:
        Tuple of (decoded_name, new_offset)
    """
    parts = []
    jumped = False
    original_offset = offset
    jumps = 0
    max_jumps = 10  # Prevent infinite loops
    
    while True:
        # Prevent infinite loops from malformed packets
        if jumps > max_jumps:
            raise Exception("Too many compression jumps")
        
        if offset >= len(data):
            raise Exception("Offset beyond message length")
        
        length = data[offset]
        
        # Check if this is a compression pointer (top 2 bits set)
        if (length & 0xC0) == 0xC0:
            # It's a pointer! Extract 14-bit offset
            if offset + 1 >= len(data):
                raise Exception("Incomplete compression pointer")
            
            pointer = struct.unpack(">H", data[offset:offset + 2])[0]
            pointer &= 0x3FFF  # Mask off top 2 bits to get offset
            
            if not jumped:
                original_offset = offset + 2
            
            offset = pointer
            jumped = True
            jumps += 1
            continue
        
        # End of name
        if length == 0:
            offset += 1
            break
        
        # Regular label
        offset += 1
        if offset + length > len(data):
            raise Exception("Label length exceeds message")
        
        parts.append(data[offset:offset + length].decode("ascii"))
        offset += length
    
    name = ".".join(parts)
    return name, original_offset if jumped else offset


def parse_header(data: bytes) -> DNSHeader:
    """
    Parse DNS header (first 12 bytes).
    
    Args:
        data: DNS message bytes
    
    Returns:
        DNSHeader object
    """
    if len(data) < 12:
        raise Exception("DNS message too short")
    
    # Unpack 6 unsigned shorts (2 bytes each)
    fields = struct.unpack(">HHHHHH", data[:12])
    
    return DNSHeader(
        id=fields[0],
        flags=fields[1],
        qdcount=fields[2],
        ancount=fields[3],
        nscount=fields[4],
        arcount=fields[5]
    )


def parse_question(data: bytes, offset: int) -> Tuple[DNSQuestion, int]:
    """
    Parse a question section.
    
    Args:
        data: Full DNS message
        offset: Starting offset of question
    
    Returns:
        Tuple of (DNSQuestion, new_offset)
    """
    name, offset = decode_dns_name(data, offset)
    qtype, qclass = struct.unpack(">HH", data[offset:offset + 4])
    offset += 4
    
    return DNSQuestion(name, qtype, qclass), offset


def parse_record(data: bytes, offset: int) -> Tuple[DNSRecord, int]:
    """
    Parse a resource record (answer, authority, or additional).
    
    Record format:
    - NAME (variable)
    - TYPE (2 bytes)
    - CLASS (2 bytes)
    - TTL (4 bytes)
    - RDLENGTH (2 bytes)
    - RDATA (RDLENGTH bytes)
    
    Args:
        data: Full DNS message
        offset: Starting offset of record
    
    Returns:
        Tuple of (DNSRecord, new_offset)
    """
    name, offset = decode_dns_name(data, offset)
    
    # Parse TYPE, CLASS, TTL, RDLENGTH
    type_, class_, ttl, rdlength = struct.unpack(
        ">HHIH",  # H=2bytes, I=4bytes, H=2bytes
        data[offset:offset + 10]
    )
    offset += 10
    
    # Parse RDATA based on type
    rdata = data[offset:offset + rdlength]
    offset += rdlength
    
    # Decode based on record type
    if type_ == TYPE_A:
        # IPv4 address (4 bytes)
        if len(rdata) == 4:
            record_data = ".".join(str(b) for b in rdata)
        else:
            record_data = "Invalid A record"
    
    elif type_ == TYPE_AAAA:
        # IPv6 address (16 bytes)
        if len(rdata) == 16:
            # Format as standard IPv6
            parts = struct.unpack(">HHHHHHHH", rdata)
            record_data = ":".join(f"{p:x}" for p in parts)
        else:
            record_data = "Invalid AAAA record"
    
    elif type_ == TYPE_NS or type_ == TYPE_CNAME:
        # Nameserver or CNAME - another domain name
        record_data, _ = decode_dns_name(data, offset - rdlength)
    
    else:
        # Unknown type - store as hex
        record_data = rdata.hex()
    
    return DNSRecord(name, type_, class_, ttl, record_data), offset


def parse_dns_response(data: bytes) -> Tuple[DNSHeader, List[DNSQuestion], List[DNSRecord], List[DNSRecord], List[DNSRecord]]:
    """
    Parse complete DNS response message.
    
    Args:
        data: Complete DNS response bytes
    
    Returns:
        Tuple of (header, questions, answers, authorities, additionals)
    """
    header = parse_header(data)
    offset = 12  # Start after header
    
    # Parse questions
    questions = []
    for _ in range(header.qdcount):
        question, offset = parse_question(data, offset)
        questions.append(question)
    
    # Parse answers
    answers = []
    for _ in range(header.ancount):
        record, offset = parse_record(data, offset)
        answers.append(record)
    
    # Parse authority records
    authorities = []
    for _ in range(header.nscount):
        record, offset = parse_record(data, offset)
        authorities.append(record)
    
    # Parse additional records
    additionals = []
    for _ in range(header.arcount):
        record, offset = parse_record(data, offset)
        additionals.append(record)
    
    return header, questions, answers, authorities, additionals


# =============================================================================
# DNS RESOLUTION
# =============================================================================

def send_dns_query(domain: str, nameserver: str, record_type: int = TYPE_A) -> bytes:
    """
    Send a DNS query to a specific nameserver and get response.
    
    Uses UDP on port 53 (standard DNS port).
    
    Args:
        domain: Domain to query
        nameserver: IP address of nameserver
        record_type: Type of record to query
    
    Returns:
        Raw DNS response bytes
    """
    query = build_query(domain, record_type)
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # 5 second timeout
    
    try:
        # Send query to nameserver on port 53
        sock.sendto(query, (nameserver, 53))
        
        # Receive response (max 512 bytes for UDP, per RFC 1035)
        data, _ = sock.recvfrom(512)
        return data
    
    finally:
        sock.close()


def resolve(domain: str, record_type: int = TYPE_A) -> Optional[str]:
    """
    Resolve a domain name using iterative queries.
    
    Resolution process:
    1. Start with root nameservers
    2. Query root for TLD nameservers (.com, .org, etc.)
    3. Query TLD for authoritative nameservers
    4. Query authoritative for final answer
    
    Args:
        domain: Domain to resolve (e.g., "google.com")
        record_type: Type of record to query
    
    Returns:
        IP address or None if resolution fails
    """
    print(f"\n{'='*60}")
    print(f"Resolving: {domain}")
    print(f"{'='*60}\n")
    
    # Start with a random root server
    nameserver = random.choice(ROOT_SERVERS)
    
    # Track our path through DNS hierarchy
    depth = 0
    max_depth = 10  # Prevent infinite loops
    
    while depth < max_depth:
        depth += 1
        print(f"Step {depth}: Querying {nameserver} for {domain}")
        
        try:
            # Send query
            response = send_dns_query(domain, nameserver, record_type)
            header, questions, answers, authorities, additionals = parse_dns_response(response)
            
            # Check for errors in response
            rcode = header.flags & 0x000F  # Last 4 bits
            if rcode != 0:
                print(f"  Error: RCODE = {rcode}")
                return None
            
            # Do we have an answer?
            if answers:
                for answer in answers:
                    if answer.type == record_type:
                        print(f"  ✓ Found answer: {answer.data}")
                        return answer.data
                    elif answer.type == TYPE_CNAME:
                        # Follow CNAME
                        print(f"  → CNAME: {answer.data}")
                        return resolve(answer.data, record_type)
            
            # No answer, check authority section for next nameserver
            if authorities:
                # Find NS records
                ns_records = [auth for auth in authorities if auth.type == TYPE_NS]
                
                if ns_records:
                    # Pick first nameserver
                    next_ns_name = ns_records[0].data
                    print(f"  → Referred to nameserver: {next_ns_name}")
                    
                    # Look for IP in additional section (glue records)
                    next_ns_ip = None
                    for additional in additionals:
                        if additional.name == next_ns_name and additional.type == TYPE_A:
                            next_ns_ip = additional.data
                            break
                    
                    if next_ns_ip:
                        nameserver = next_ns_ip
                        print(f"    Using IP from glue record: {next_ns_ip}")
                    else:
                        # Need to resolve the nameserver itself
                        print(f"    Resolving nameserver: {next_ns_name}")
                        next_ns_ip = resolve(next_ns_name, TYPE_A)
                        if next_ns_ip:
                            nameserver = next_ns_ip
                        else:
                            print(f"  Failed to resolve nameserver")
                            return None
                    
                    continue
            
            print(f"  No answer or referral found")
            return None
        
        except socket.timeout:
            print(f"  Timeout querying {nameserver}")
            return None
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    print(f"Max depth reached")
    return None


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    """
    Main program - demonstrates DNS resolution.
    """
    print("DNS Resolver - Iterative Resolution from Root Servers")
    print("=" * 60)
    
    # Test domains
    test_domains = [
        "google.com",
        "github.com",
        "cloudflare.com",
    ]
    
    for domain in test_domains:
        result = resolve(domain)
        if result:
            print(f"\n✓ SUCCESS: {domain} → {result}")
        else:
            print(f"\n✗ FAILED: Could not resolve {domain}")
        print()
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Mode - Enter domain names to resolve")
    print("Type 'quit' to exit")
    print("=" * 60)
    
    while True:
        try:
            domain = input("\nEnter domain: ").strip()
            if domain.lower() in ['quit', 'exit', 'q']:
                break
            
            if domain:
                result = resolve(domain)
                if result:
                    print(f"\n✓ {domain} → {result}")
                else:
                    print(f"\n✗ Failed to resolve {domain}")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()