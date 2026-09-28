import json
import sys
from client import DNSProtocol

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "generate_dns_query",
                        "description": "Generate binary DNS query wire hex and header metadata",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string"},
                                "qtype": {"type": "integer", "default": 1}
                            },
                            "required": ["domain"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "generate_dns_query":
            q = DNSProtocol.build_query(args["domain"], qtype=args.get("qtype", 1))
            hdr = DNSProtocol.parse_header(q)
            hdr["hex_bytes"] = q.hex()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(hdr)}]}
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
