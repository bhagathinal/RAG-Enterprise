import yaml
from pathlib import Path

PROMPT_CONFIG_PATH = Path("configs/system_prompts_4.yaml")

def load_system_prompt(domain: str) -> str:
    """
    Load system instruction based on document domain.

    Args:
        domain (str): Domain such as hr, technical, finance

    Returns:
        str: System prompt text
    """

    with open(PROMPT_CONFIG_PATH, "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f)

    # Fallback to general if domain not found
    return prompts.get(domain.lower(), prompts["general"])
