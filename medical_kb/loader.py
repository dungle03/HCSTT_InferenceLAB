"""Medical Knowledge Base Loader.

Loads and manages medical KB from JSON file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from inference_lab.knowledge_base import KnowledgeBase
from inference_lab.models import Rule


class MedicalKnowledgeBase:
    """Medical Knowledge Base with 100+ rules for diagnosis."""

    def __init__(self, json_path: Optional[str] = None):
        """Initialize Medical KB.

        Args:
            json_path: Path to medical_kb.json. If None, uses default path.
        """
        if json_path is None:
            # Default path relative to project root
            base_path = Path(__file__).parent.parent
            json_path = base_path / "data" / "medical_kb.json"

        self.json_path = Path(json_path)
        self.data = self._load_json()
        self.kb = self._create_knowledge_base()

    def _load_json(self) -> Dict[str, Any]:
        """Load JSON data from file."""
        if not self.json_path.exists():
            raise FileNotFoundError(
                f"Medical KB file not found: {self.json_path}\n"
                f"Please run: python data/generate_medical_kb.py"
            )

        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _create_knowledge_base(self) -> KnowledgeBase:
        """Create KnowledgeBase instance from JSON data."""
        kb = KnowledgeBase(name="Medical KB")

        # Add all rules
        for rule_data in self.data["rules"]:
            # Convert premises to text format: "a ^ b ^ c"
            premises_text = " ^ ".join(rule_data["premises"])
            rule_text = f"{premises_text} -> {rule_data['conclusion']}"

            kb.add_rule_from_text(rule_text)

        return kb

    def get_rules(self) -> List[Rule]:
        """Get all rules."""
        return list(self.kb.rules)

    def get_rules_by_module(self, module: str) -> List[Rule]:
        """Get rules by module code (SYMP, RESP, DIGE, etc.)."""
        matching_rules = []

        for rule_data in self.data["rules"]:
            if rule_data["module"] == module:
                # Find corresponding Rule object
                conclusion = rule_data["conclusion"]
                for rule in self.kb.rules:
                    if rule.conclusion == conclusion:
                        matching_rules.append(rule)
                        break

        return matching_rules

    def get_form_fields(self) -> List[Dict[str, Any]]:
        """Get form configuration for dynamic form generation."""
        return self.data["form_config"]["fields"]

    def get_recommendation(self, disease: str) -> str:
        """Get treatment recommendation for a disease.

        Args:
            disease: Disease identifier (e.g., 'cam_thuong', 'covid_19')

        Returns:
            Recommendation text or default message
        """
        for rec in self.data["recommendations"]:
            if rec["condition"] == disease:
                return rec["recommendation"]

        return "Cần khám bác sĩ để được tư vấn chi tiết."

    def get_disease_info(self, disease: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a disease."""
        for disease_data in self.data["diseases"]:
            if disease_data["variable"] == disease:
                return disease_data
        return None

    def get_symptom_label(self, symptom: str) -> str:
        """Get human-readable label for a symptom variable."""
        for symp in self.data["symptoms"]:
            if symp["variable"] == symptom:
                return symp["label"]
        return symptom.replace("_", " ").title()

    def get_metadata(self) -> Dict[str, Any]:
        """Get KB metadata (version, counts, etc.)."""
        return self.data["metadata"]

    def validate(self) -> Dict[str, Any]:
        """Validate the knowledge base.

        Returns:
            Validation result with errors and warnings
        """
        from .validator import RuleValidator

        validator = RuleValidator(self)
        return validator.validate_all()
