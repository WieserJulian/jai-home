"""Skill manager for JAI Home.

Loads ``skills.yaml`` (located next to this file), compiles the regex patterns,
and dispatches matching utterances to the specified Python callables.
Each entry in ``skills.yaml`` must contain:

- ``pattern`` – a regular expression (case‑insensitive) that captures the relevant
  part of the command.
- ``action`` – ``module:function`` reference. The module is imported dynamically
  and the function is called with the captured group (or the full match if no
  group is defined).

If no skill matches, an empty string is returned.
"""

import importlib
import re
from pathlib import Path
import yaml  # type: ignore

SKILLS_PATH = Path(__file__).with_name("skills.yaml")

class SkillManager:
    def __init__(self):
        self._load_skills()

    def _load_skills(self):
        self.skills = []
        if not SKILLS_PATH.is_file():
            return
        with open(SKILLS_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        for entry in data.get("skills", []):
            pattern = re.compile(entry["pattern"], re.IGNORECASE)
            module_name, func_name = entry["action"].split(":")
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            self.skills.append((pattern, func))

    def dispatch(self, text: str) -> str:
        """Return the result of the first matching skill, or ``""``.
        """
        for pattern, func in self.skills:
            m = pattern.search(text)
            if m:
                arg = m.group(1) if m.lastindex else m.group(0)
                return func(arg)
        return ""
