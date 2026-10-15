"""Example usage for Enterprise Customer Empathy & Policy-Constrained Agent."""
from client import EnterpriseCustomerAgentGuard

if __name__ == "__main__":
    # Test 1: Empathy Tone Evaluation
    print("=== Empathy Tone Analysis ===")
    bad_draft = "As per our policy you cannot return this item. Nothing we can do about it."
    eval_bad = EnterpriseCustomerAgentGuard.evaluate_response_empathy(bad_draft)
    print("Bad Draft Status:", eval_bad["status"])
    print("Compliant:", eval_bad["compliant"])
    print("Recommendation:", eval_bad["recommendation"])

    good_draft = "I understand how frustrating this delay is, and I sincerely apologize. I'd be glad to help resolve this right away."
    eval_good = EnterpriseCustomerAgentGuard.evaluate_response_empathy(good_draft)
    print("\nGood Draft Status:", eval_good["status"])
    print("Compliant:", eval_good["compliant"])
    print("Empathy Score:", eval_good["empathy_score"])

    # Test 2: Action Authorization Boundary Checks
    print("\n=== Action Authorization Boundary Verification ===")
    customer = {
        "customer_id": "cust_452",
        "is_authenticated": True,
        "days_since_purchase": 12,
        "order_status": "processing",
    }

    # Action within threshold ($45 <= $100)
    auth1 = EnterpriseCustomerAgentGuard.verify_action_authorization(
        action_name="issue_refund",
        action_params={"amount": 45.0},
        customer_context=customer,
    )
    print(f"Refund $45: Decision={auth1['decision']}, Authorized={auth1['authorized']}")

    # Action exceeding threshold ($250 > $100) -> escalate to supervisor
    auth2 = EnterpriseCustomerAgentGuard.verify_action_authorization(
        action_name="issue_refund",
        action_params={"amount": 250.0},
        customer_context=customer,
    )
    print(f"Refund $250: Decision={auth2['decision']}, Reason={auth2['reason']}")

    # Unauthenticated attempt
    unauth_customer = dict(customer, is_authenticated=False)
    auth3 = EnterpriseCustomerAgentGuard.verify_action_authorization(
        action_name="issue_refund",
        action_params={"amount": 20.0},
        customer_context=unauth_customer,
    )
    print(f"Unauthenticated attempt: Decision={auth3['decision']}")
