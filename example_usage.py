from client import DNSProtocol

def main():
    query = DNSProtocol.build_query("agent.genpark.ai", tx_id=0x9999)
    print("Built raw query bytes (length):", len(query))
    parsed = DNSProtocol.parse_header(query)
    print("Parsed DNS header:", parsed)
    assert parsed["tx_id"] == "0x9999" and parsed["questions"] == 1

if __name__ == "__main__":
    main()
