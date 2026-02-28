# Skills Framework

The skill system is defined in `src/skill_manager.py` and `src/skills.yaml`.

## Skill Definition

- Each skill entry contains a **regex pattern** and an **action** (`module:function`).
- The manager loads all skills at startup and dispatches the first matching skill.

```yaml
skills:
  - pattern: "(?i)turn on the (.+) light"
    action: "skills.lighting:turn_on"
```

## Adding New Skills

1. **Edit `skills.yaml`** – Add a new entry with the desired pattern and action.
2. **Implement the handler** – Create a Python function matching the `module:function` reference.
3. **Test** – Run the unit test suite (`pytest -q tests/test_skills.py`) to verify the new skill is recognized.
4. **Document** – Add a short description to this guide and, if needed, a usage example in the user‑facing docs.

---
*Formatted to the project’s documentation standards.
*Note: Keep entries concise; the assistant parses only the first matching pattern.*


The skill system is defined in `src/skill_manager.py` and `src/skills.yaml`.

- Each skill entry contains a **regex pattern** and an **action** (`module:function`).
- The manager loads all skills at startup and dispatches the first matching skill.

```yaml
skills:
  - pattern: "(?i)turn on the (.+) light"
    action: "skills.lighting:turn_on"
```

Add new skills by editing `skills.yaml` and providing the corresponding Python function.
