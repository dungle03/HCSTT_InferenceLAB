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
    """Medical Knowledge Base loader for medical/specialized KBs.

    Compatible with both the legacy medical_kb.json and the new sinusitis_kb.json
    structures. Accepts either 'json_path' or 'kb_path' for convenience.
    """

    def __init__(self, json_path: Optional[str] = None, kb_path: Optional[str] = None):
        """Initialize Medical KB.

        Args:
            json_path: Path to KB JSON file (legacy name).
            kb_path: Alias for json_path. If both provided, kb_path takes precedence.
        """
        # Support both parameter names
        chosen_path = kb_path or json_path
        if chosen_path is None:
            # Default path relative to project root (legacy multi-disease KB)
            base_path = Path(__file__).parent.parent
            chosen_path = base_path / "data" / "medical_kb.json"

        self.json_path = Path(chosen_path)
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
        # Map internal numeric rule.id -> original JSON rule metadata (id, notes, module...)
        self._rule_meta_by_internal_id: Dict[int, Dict[str, Any]] = {}

        # Add all rules
        for rule_data in self.data["rules"]:
            # Convert premises to text format: "a ^ b ^ c"
            premises_text = " ^ ".join(rule_data["premises"])
            rule_text = f"{premises_text} -> {rule_data['conclusion']}"

            rule = kb.add_rule_from_text(rule_text)
            # Store mapping for explanations in results page
            self._rule_meta_by_internal_id[rule.id] = {
                "json_id": rule_data.get("id"),
                "module": rule_data.get("module"),
                "premises": list(rule.premises),
                "conclusion": rule.conclusion,
                "notes": rule_data.get("notes"),
                "confidence": rule_data.get("confidence"),
            }

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
        """Get flattened form fields for backward compatibility.

        - Legacy format: form_config.fields (flat list)
        - New format: form_config.steps[*].fields (multi-step)
        """
        fc = self.data.get("form_config", {})
        # Legacy flat layout
        if "fields" in fc and isinstance(fc["fields"], list):
            return fc["fields"]
        # New stepped layout
        fields: List[Dict[str, Any]] = []
        for step in fc.get("steps", []) or []:
            fields.extend(step.get("fields", []))
        return fields

    def get_form_config(self) -> Dict[str, Any]:
        """Return raw form configuration (supports multi-step sinusitis UI)."""
        return self.data.get("form_config", {})

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

    def get_diseases(self) -> List[Dict[str, Any]]:
        """Return disease list (used to build inference goals)."""
        return list(self.data.get("diseases", []))

    def get_rule_info(self, internal_rule_id: int) -> Optional[Dict[str, Any]]:
        """Return rule metadata by internal numeric id used by the engine.

        The returned dict includes keys: json_id, module, premises, conclusion, notes.
        Returns None if not found.
        """
        return self._rule_meta_by_internal_id.get(int(internal_rule_id))

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
