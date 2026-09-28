"""DNS Wire Protocol Packet Builder & Parser.
100% Python Standard Library.
"""

import struct

class DNSProtocol:
    """DNS wire-format packet generator and inspector."""

    @staticmethod
    def encode_qname(domain: str) -> bytes:
        parts = domain.strip(".").split(".")
        out = bytearray()
        for p in parts:
            out.append(len(p))
            out.extend(p.encode("ascii"))
        out.append(0)
        return bytes(out)

    @staticmethod
    def build_query(domain: str, tx_id: int = 0x1234, qtype: int = 1) -> bytes:
        flags = 0x0100  # Standard query with recursion desired
        qdcount = 1
        ancount = 0
        nscount = 0
        arcount = 0
        header = struct.pack("!HHHHHH", tx_id, flags, qdcount, ancount, nscount, arcount)
        question = DNSProtocol.encode_qname(domain) + struct.pack("!HH", qtype, 1)  # IN class
        return header + question

    @staticmethod
    def parse_header(wire: bytes) -> dict:
        if len(wire) < 12:
            raise ValueError("DNS wire format requires at least 12-byte header")
        tx_id, flags, qd, an, ns, ar = struct.unpack("!HHHHHH", wire[:12])
        is_response = bool(flags & 0x8000)
        opcode = (flags >> 11) & 0x0F
        authoritative = bool(flags & 0x0400)
        truncated = bool(flags & 0x0200)
        recursion_desired = bool(flags & 0x0100)
        recursion_available = bool(flags & 0x0080)
        rcode = flags & 0x000F
        return {
            "tx_id": hex(tx_id),
            "is_response": is_response,
            "opcode": opcode,
            "authoritative": authoritative,
            "truncated": truncated,
            "recursion_desired": recursion_desired,
            "recursion_available": recursion_available,
            "rcode": rcode,
            "questions": qd,
            "answers": an,
            "authorities": ns,
            "additionals": ar
        }
