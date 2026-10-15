"""Enterprise Customer Empathy & Policy-Constrained Agent Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import re


class EnterpriseCustomerAgentGuard:
    """Enforces deterministic business policy constraints, empathy tone compliance,
    and action authorization boundaries for enterprise customer service agents."""

    # Default business policies for customer service
    DEFAULT_POLICIES = {
        "max_instant_refund_amount": 100.0,
        "max_return_days_window": 30,
        "requires_supervisor_for_cashback": True,
        "allow_courtesy_store_credit_limit": 25.0,
    }

    EMPATHY_MARKERS = [
        "understand", "apologize", "sorry", "appreciate", "help you",
        "glad to", "resolve this", "right away", "patience", "frustrating"
    ]

    DEFENSIVE_OR_DISMISSIVE_MARKERS = [
        "not our fault", "as per our policy you cannot", "you should have known",
        "impossible", "nothing we can do", "too late", "don't blame us"
    ]

    @classmethod
    def evaluate_response_empathy(cls, draft_response: str) -> Dict[str, Any]:
        """Analyzes an agent's response for empathy markers and checks for dismissive/defensive language."""
        text = draft_response.lower()
        matched_empathy = [m for m in cls.EMPATHY_MARKERS if m in text]
        matched_defensive = [d for d in cls.DEFENSIVE_OR_DISMISSIVE_MARKERS if d in text]

        empathy_score = min(1.0, len(matched_empathy) * 0.3)
        if matched_defensive:
            compliant = False
            status = "POLICY_REJECT_DEFENSIVE_TONE"
            recommendation = f"Remove dismissive phrasing: {', '.join(matched_defensive)}. Rephrase with empathetic problem-solving tone."
        elif empathy_score >= 0.3:
            compliant = True
            status = "COMPLIANT_EMPATHETIC"
            recommendation = "Response adheres to enterprise brand empathy standards."
        else:
            compliant = True  # Neutral
            status = "NEUTRAL_TONE"
            recommendation = "Consider adding an empathetic acknowledgement (e.g., 'I understand your frustration and am glad to help')."

        return {
            "status": status,
            "compliant": compliant,
            "empathy_score": round(empathy_score, 2),
            "matched_empathy_markers": matched_empathy,
            "defensive_phrases_found": matched_defensive,
            "recommendation": recommendation,
        }

    @classmethod
    def verify_action_authorization(
        cls,
        action_name: str,
        action_params: Dict[str, Any],
        customer_context: Dict[str, Any],
        custom_policies: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Validates a proposed agent backend action against strict business rules and limits."""
        policies = dict(cls.DEFAULT_POLICIES)
        if custom_policies:
            policies.update(custom_policies)

        authenticated = bool(customer_context.get("is_authenticated", False))
        if not authenticated:
            return {
                "decision": "REJECTED_UNAUTHENTICATED",
                "action": action_name,
                "authorized": False,
                "reason": "Customer identity is not authenticated. Re-direct to secure authentication portal.",
            }

        # Rule check: issue_refund
        if action_name == "issue_refund":
            amount = float(action_params.get("amount", 0.0))
            max_limit = float(policies.get("max_instant_refund_amount", 100.0))
            days_since_purchase = int(customer_context.get("days_since_purchase", 0))
            max_days = int(policies.get("max_return_days_window", 30))

            if days_since_purchase > max_days:
                return {
                    "decision": "REQUIRES_SUPERVISOR_ESCALATION",
                    "action": action_name,
                    "authorized": False,
                    "reason": f"Purchase was {days_since_purchase} days ago, exceeding standard {max_days}-day return window.",
                }

            if amount > max_limit:
                return {
                    "decision": "REQUIRES_SUPERVISOR_ESCALATION",
                    "action": action_name,
                    "authorized": False,
                    "reason": f"Refund amount ${amount:.2f} exceeds agent autonomous threshold of ${max_limit:.2f}.",
                }

            return {
                "decision": "AUTHORIZED",
                "action": action_name,
                "authorized": True,
                "reason": f"Refund of ${amount:.2f} is within authorized threshold and policy window.",
            }

        # Rule check: issue_store_credit
        elif action_name == "issue_store_credit":
            amount = float(action_params.get("amount", 0.0))
            limit = float(policies.get("allow_courtesy_store_credit_limit", 25.0))
            if amount <= limit:
                return {
                    "decision": "AUTHORIZED",
                    "action": action_name,
                    "authorized": True,
                    "reason": f"Courtesy credit of ${amount:.2f} is within autonomous approval limit.",
                }
            else:
                return {
                    "decision": "REQUIRES_SUPERVISOR_ESCALATION",
                    "action": action_name,
                    "authorized": False,
                    "reason": f"Requested credit ${amount:.2f} exceeds standard courtesy limit of ${limit:.2f}.",
                }

        # Rule check: modify_order_address
        elif action_name == "modify_order_address":
            order_status = str(customer_context.get("order_status", "")).lower()
            if order_status in ["shipped", "delivered"]:
                return {
                    "decision": "REJECTED_TERMINAL_STATE",
                    "action": action_name,
                    "authorized": False,
                    "reason": f"Order has already reached state '{order_status}' and address cannot be modified.",
                }
            return {
                "decision": "AUTHORIZED",
                "action": action_name,
                "authorized": True,
                "reason": "Order is pending fulfillment; address update approved.",
            }

        # Fallback for unrecognized action
        return {
            "decision": "REQUIRES_SUPERVISOR_ESCALATION",
            "action": action_name,
            "authorized": False,
            "reason": f"Unrecognized action '{action_name}' requires human operator confirmation.",
        }
