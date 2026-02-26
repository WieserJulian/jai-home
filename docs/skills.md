# Skills Framework

The skill system is defined in `src/skill_manager.py` and `src/skills.yaml`.

- Each skill entry contains a **regex pattern** and an **action** (`module:function`).
- The manager loads all skills at startup and dispatches the first matching skill.

```yaml
skills:
  - pattern: "(?i)turn on the (.+) light"
    action: "skills.lighting:turn_on"
```

Add new skills by editing `skills.yaml` and providing the corresponding Python function.
