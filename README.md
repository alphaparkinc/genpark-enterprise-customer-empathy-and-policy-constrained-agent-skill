# genpark-enterprise-customer-empathy-and-policy-constrained-agent-skill

Deterministic policy boundary enforcement, customer empathy scoring, and authenticated action verifier for enterprise customer service agents.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Deterministic Business Policy Guardrails**: Enforces non-negotiable operational limits (maximum autonomous refund amounts, return window limits, allowed courtesy store credits).
- **Empathy & Tone Compliance Analyzer**: Evaluates conversational drafts to ensure positive, solution-oriented empathy markers while blocking defensive or dismissive wording.
- **Action Authorization Gatekeeper**: Validates customer authentication state and high-impact API calls (e.g., refunds, cancellations, address updates), automatically routing out-of-policy requests to human supervisors.
- **Zero-Dependency Safe Execution**: Operates deterministically without external API overhead or unpredictable prompt drift.

## Architecture

```
[Agent Response Draft / Action Request]
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│         EnterpriseCustomerAgentGuard             │
│  - Empathy Tone Lexicon Analyzer                 │
│  - Authentication State Verifier                 │
│  - Deterministic Policy Window & Limit Checks    │
└──────────────────────────────────────────────────┘
                    │
      ┌─────────────┼──────────────┐
      ▼             ▼              ▼
[AUTHORIZED]   [ESCALATE]     [POLICY_REJECT]
  Autonomous    Supervisor      Immediate
  Execution     Handoff         Safe Rejection
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `evaluate_response_empathy`: Analyzes agent message drafts for brand empathy markers and detects defensive or dismissive phrases.
- `verify_action_authorization`: Validates proposed agent backend operations (refunds, credits, cancellations) against strict business policies.

## Quickstart (Python API)

```python
from client import EnterpriseCustomerAgentGuard

# 1. Analyze Tone
tone = EnterpriseCustomerAgentGuard.evaluate_response_empathy(
    "I understand your frustration and apologize for the shipping delay. Let me help you."
)
print("Tone Compliant:", tone["compliant"], "Empathy Score:", tone["empathy_score"])

# 2. Verify Action Boundary
customer = {"is_authenticated": True, "days_since_purchase": 5}
decision = EnterpriseCustomerAgentGuard.verify_action_authorization(
    action_name="issue_refund",
    action_params={"amount": 40.0},
    customer_context=customer,
)
print("Decision:", decision["decision"], "Authorized:", decision["authorized"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
