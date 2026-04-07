from __future__ import annotations


def parse_form_fields(serialized: str) -> dict[str, str] | str:
    fields: dict[str, str] = {}
    for entry in [chunk.strip() for chunk in serialized.split(",") if chunk.strip()]:
        if "=" not in entry:
            return "Format invalide. Utilisez: selector=valeur,selector=valeur"
        selector, value = entry.split("=", 1)
        selector = selector.strip()
        if not selector:
            return "Format invalide: selecteur vide."
        fields[selector] = value.strip()

    if not fields:
        return "Aucun champ de formulaire fourni."

    return fields
