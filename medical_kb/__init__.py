"""Medical Knowledge Base module for inference_lab.

This module provides a comprehensive medical knowledge base with 100+ rules
for common medical diagnoses including respiratory, digestive, cardiovascular,
endocrine, and emergency conditions.
"""

from .loader import MedicalKnowledgeBase
from .form_generator import generate_form_html, extract_facts_from_form
from .validator import RuleValidator

__all__ = [
    "MedicalKnowledgeBase",
    "generate_form_html",
    "extract_facts_from_form",
    "RuleValidator",
]

__version__ = "1.0.0"
