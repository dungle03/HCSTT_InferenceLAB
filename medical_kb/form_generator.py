"""Form Generator for Medical KB.

Generates dynamic HTML forms and extracts facts from form data.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set


def generate_form_html(fields: List[Dict[str, Any]]) -> str:
    """Generate HTML form from field configuration.

    Args:
        fields: List of field configurations

    Returns:
        HTML string for the form
    """
    html_parts = []

    for field in fields:
        field_type = field["type"]
        field_id = field["id"]
        variable = field["variable"]
        label = field["label"]
        required = field.get("required", False)
        options = field.get("options", {})

        # Wrapper div
        html_parts.append(f'<div class="form-group" data-field-id="{field_id}">')

        if field_type == "boolean":
            # Checkbox
            html_parts.append(
                f"""
                <label class="checkbox-label">
                    <input type="checkbox" 
                           name="{variable}" 
                           id="{variable}"
                           {'required' if required else ''}>
                    <span>{label}</span>
                </label>
            """
            )

        elif field_type == "number":
            # Number input
            min_val = options.get("min", 0)
            max_val = options.get("max", 100)
            step = options.get("step", 1)

            html_parts.append(
                f"""
                <label for="{variable}">{label}</label>
                <input type="number" 
                       name="{variable}" 
                       id="{variable}"
                       min="{min_val}" 
                       max="{max_val}" 
                       step="{step}"
                       placeholder="Nhập {label.lower()}"
                       {'required' if required else ''}>
            """
            )

        elif field_type == "range":
            # Range slider
            min_val = options.get("min", 0)
            max_val = options.get("max", 10)
            default = options.get("default", (min_val + max_val) // 2)

            html_parts.append(
                f"""
                <label for="{variable}">
                    {label}: <span id="{variable}_value">{default}</span>
                </label>
                <input type="range" 
                       name="{variable}" 
                       id="{variable}"
                       min="{min_val}" 
                       max="{max_val}" 
                       value="{default}"
                       oninput="document.getElementById('{variable}_value').textContent=this.value">
            """
            )

        elif field_type == "radio":
            # Radio buttons
            opts = options.get("options", "").split(",")
            html_parts.append(f"<label>{label}</label>")
            html_parts.append('<div class="radio-group">')

            for i, opt in enumerate(opts):
                opt = opt.strip()
                checked = "checked" if i == 0 else ""
                html_parts.append(
                    f"""
                    <label class="radio-label">
                        <input type="radio" 
                               name="{variable}" 
                               value="{opt}" 
                               {checked}
                               {'required' if required else ''}>
                        <span>{opt.replace("_", " ").title()}</span>
                    </label>
                """
                )

            html_parts.append("</div>")

        elif field_type == "select":
            # Dropdown select
            opts = options.get("options", "").split(",")
            html_parts.append(f'<label for="{variable}">{label}</label>')
            html_parts.append(
                f'<select name="{variable}" id="{variable}" {"required" if required else ""}>'
            )

            for opt in opts:
                opt = opt.strip()
                html_parts.append(
                    f'<option value="{opt}">{opt.replace("_", " ").title()}</option>'
                )

            html_parts.append("</select>")

        # Add hint if available
        hint = field.get("hint")
        if hint:
            html_parts.append(f'<small class="hint">💡 {hint}</small>')

        html_parts.append("</div>")

    return "\n".join(html_parts)


def extract_facts_from_form(form_data: Dict[str, Any], kb: Any) -> Set[str]:
    """Extract facts from form data based on logic rules.

    Args:
        form_data: Dictionary of form field values
        kb: MedicalKnowledgeBase instance

    Returns:
        Set of fact strings
    """
    facts = set()

    # Get fact mapping rules from KB
    fact_rules = kb.data.get("fact_rules", [])

    for rule in fact_rules:
        fact = rule["fact"]
        condition = rule["condition"]

        # Safely evaluate condition
        try:
            # Create a safe evaluation context with only form_data variables
            context = {key: form_data.get(key) for key in form_data}

            # Evaluate condition (simple conditions only for safety)
            if evaluate_condition(condition, context):
                facts.add(fact)
        except Exception:
            # Skip invalid conditions
            continue

    # Also add direct boolean fields
    for key, value in form_data.items():
        if isinstance(value, bool) and value:
            facts.add(key)
        elif value == "true" or value == True:
            facts.add(key)

    return facts


def evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    """Safely evaluate a condition string.

    Args:
        condition: Condition string like "nhiet_do > 38"
        context: Dictionary of variable values

    Returns:
        Boolean result
    """
    # Replace variable names with context values
    # This is a simple implementation - for production, use a proper expression parser

    try:
        # Simple comparisons
        if ">=" in condition:
            var, val = condition.split(">=")
            var = var.strip()
            val = float(val.strip())
            return float(context.get(var, 0)) >= val

        elif ">" in condition:
            var, val = condition.split(">")
            var = var.strip()
            val = float(val.strip())
            return float(context.get(var, 0)) > val

        elif "<=" in condition:
            var, val = condition.split("<=")
            var = var.strip()
            val = float(val.strip())
            return float(context.get(var, 0)) <= val

        elif "<" in condition:
            var, val = condition.split("<")
            var = var.strip()
            val = float(val.strip())
            return float(context.get(var, 0)) < val

        elif "===" in condition:
            var, val = condition.split("===")
            var = var.strip()
            val = val.strip().strip("'").strip('"')
            if val == "true":
                return context.get(var) == True or context.get(var) == "true"
            elif val == "false":
                return context.get(var) == False or context.get(var) == "false"
            return str(context.get(var, "")) == val

        elif "!==" in condition:
            var, val = condition.split("!==")
            var = var.strip()
            val = val.strip().strip("'").strip('"')
            return str(context.get(var, "")) != val

        elif " && " in condition or " ^ " in condition:
            # AND condition
            parts = condition.replace(" ^ ", " && ").split(" && ")
            return all(evaluate_condition(part.strip(), context) for part in parts)

        elif " || " in condition or " v " in condition:
            # OR condition
            parts = condition.replace(" v ", " || ").split(" || ")
            return any(evaluate_condition(part.strip(), context) for part in parts)

        else:
            # Simple boolean variable
            var = condition.strip()
            return bool(context.get(var, False))

    except Exception:
        return False
