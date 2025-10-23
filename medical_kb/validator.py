"""Rule Validator for Medical KB.

Validates rules for syntax errors, conflicts, and unreachable facts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .loader import MedicalKnowledgeBase


class RuleValidator:
    """Validator for medical knowledge base rules."""

    def __init__(self, kb: MedicalKnowledgeBase):
        """Initialize validator.

        Args:
            kb: MedicalKnowledgeBase instance to validate
        """
        self.kb = kb
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Dict[str, Any]:
        """Validate entire knowledge base.

        Returns:
            Dictionary with validation results
        """
        self.errors = []
        self.warnings = []

        self.check_syntax()
        self.check_conflicts()
        self.check_duplicates()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "total_rules": len(self.kb.data["rules"]),
            "total_symptoms": len(self.kb.data["symptoms"]),
            "total_diseases": len(self.kb.data["diseases"]),
        }

    def check_syntax(self):
        """Check rule syntax and variable existence."""
        # Build sets of valid variables
        valid_symptoms = {s["variable"] for s in self.kb.data["symptoms"]}
        valid_diseases = {d["variable"] for d in self.kb.data["diseases"]}
        all_valid = valid_symptoms | valid_diseases

        for rule_data in self.kb.data["rules"]:
            rule_id = rule_data["id"]

            # Check premises
            for premise in rule_data["premises"]:
                if premise not in all_valid:
                    self.errors.append(
                        f"Rule {rule_id}: Unknown premise variable '{premise}'"
                    )

            # Check conclusion
            conclusion = rule_data["conclusion"]
            if conclusion not in all_valid:
                self.errors.append(
                    f"Rule {rule_id}: Unknown conclusion variable '{conclusion}'"
                )

    def check_conflicts(self):
        """Check for conflicting rules (same premises, different conclusions)."""
        rule_map: Dict[tuple, List[str]] = {}

        for rule_data in self.kb.data["rules"]:
            rule_id = rule_data["id"]
            premises = tuple(sorted(rule_data["premises"]))
            conclusion = rule_data["conclusion"]

            key = premises
            if key not in rule_map:
                rule_map[key] = []
            rule_map[key].append((rule_id, conclusion))

        # Find conflicts
        for premises, rules in rule_map.items():
            if len(rules) > 1:
                conclusions = {r[1] for r in rules}
                if len(conclusions) > 1:
                    rule_ids = [r[0] for r in rules]
                    self.warnings.append(
                        f"Potential conflict: Rules {', '.join(rule_ids)} have same premises "
                        f"but different conclusions: {', '.join(conclusions)}"
                    )

    def check_duplicates(self):
        """Check for duplicate rules."""
        seen: Set[tuple] = set()

        for rule_data in self.kb.data["rules"]:
            rule_id = rule_data["id"]
            key = (tuple(sorted(rule_data["premises"])), rule_data["conclusion"])

            if key in seen:
                self.warnings.append(f"Duplicate rule detected: {rule_id}")
            seen.add(key)

    def check_unreachable(self):
        """Check for unreachable facts (not implemented yet)."""
        # This would require more complex graph analysis
        pass
