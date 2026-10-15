"""MCP server for Enterprise Customer Empathy & Policy-Constrained Agent."""
import sys
import json
from client import EnterpriseCustomerAgentGuard


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "evaluate_response_empathy",
                    "description": "Analyzes agent message drafts for brand empathy markers and detects defensive or dismissive phrases",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "draft_response": {"type": "string"},
                        },
                        "required": ["draft_response"],
                    },
                },
                {
                    "name": "verify_action_authorization",
                    "description": "Validates proposed agent backend operations (refunds, credits, cancellations) against strict business policies",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "action_name": {"type": "string"},
                            "action_params": {"type": "object"},
                            "customer_context": {"type": "object"},
                            "custom_policies": {"type": "object"},
                        },
                        "required": ["action_name", "action_params", "customer_context"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_response_empathy":
            res = EnterpriseCustomerAgentGuard.evaluate_response_empathy(
                args.get("draft_response", "")
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "verify_action_authorization":
            res = EnterpriseCustomerAgentGuard.verify_action_authorization(
                args.get("action_name", ""),
                args.get("action_params", {}),
                args.get("customer_context", {}),
                custom_policies=args.get("custom_policies"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
