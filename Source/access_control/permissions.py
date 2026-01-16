ROLE_PERMISSIONS = {
    "Employee": ["General", "Technical"],
    "HR": ["HR", "General"],
    "Management": ["HR", "Finance", "Technical", "General"]
}

DOMAIN_ROLE_MAPPING = {
    "HR": ["HR", "Management"],
    "Finance": ["Management"],
    "Technical": ["Employee", "Management"],
    "General": ["Employee", "HR", "Management"]
}
