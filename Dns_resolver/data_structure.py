
# =============================================================================
# DATA STRUCTURES
# =============================================================================

from dataclasses import dataclass


@dataclass
class DNSHeader:
    """
    DNS Header Format (12 bytes total):
    
    0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |  2 bytes
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |  2 bytes
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |  2 bytes
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |  2 bytes
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |  2 bytes
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |  2 bytes
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """
    id: int              # 16-bit identifier to match queries with responses
    flags: int           # 16-bit flags field
    qdcount: int         # Number of questions
    ancount: int         # Number of answers
    nscount: int         # Number of authority records
    arcount: int         # Number of additional records


@dataclass
class DNSQuestion:
    """
    DNS Question Section:
    - QNAME: Domain name (variable length)
    - QTYPE: Query type (2 bytes) - A, AAAA, NS, etc.
    - QCLASS: Query class (2 bytes) - usually 1 for Internet
    """
    name: str
    qtype: int
    qclass: int


@dataclass
class DNSRecord:
    """
    DNS Resource Record (Answer/Authority/Additional sections):
    - NAME: Domain name
    - TYPE: Record type
    - CLASS: Record class
    - TTL: Time to live in seconds
    - RDLENGTH: Length of RDATA
    - RDATA: Record data (IP address, nameserver, etc.)
    """
    name: str
    type: int
    class_: int
    ttl: int
    data: str


# =============================================================================
# DNS RECORD TYPES (Most common ones)
# =============================================================================

TYPE_A = 1       # IPv4 address
TYPE_NS = 2      # Nameserver
TYPE_CNAME = 5   # Canonical name (alias)
TYPE_SOA = 6     # Start of authority
TYPE_MX = 15     # Mail exchange
TYPE_TXT = 16    # Text record
TYPE_AAAA = 28   # IPv6 address

CLASS_IN = 1     # Internet class


# =============================================================================
# ROOT NAMESERVERS
# =============================================================================

# The 13 root nameserver IP addresses (A-M)
# These are the starting point of all DNS resolution
ROOT_SERVERS = [
    "198.41.0.4",      # a.root-servers.net
    "199.9.14.201",    # b.root-servers.net
    "192.33.4.12",     # c.root-servers.net
    "199.7.91.13",     # d.root-servers.net
    "192.203.230.10",  # e.root-servers.net
    "192.5.5.241",     # f.root-servers.net
    "192.112.36.4",    # g.root-servers.net
    "198.97.190.53",   # h.root-servers.net
    "192.36.148.17",   # i.root-servers.net
    "192.58.128.30",   # j.root-servers.net
    "193.0.14.129",    # k.root-servers.net
    "199.7.83.42",     # l.root-servers.net
    "202.12.27.33",    # m.root-servers.net
]