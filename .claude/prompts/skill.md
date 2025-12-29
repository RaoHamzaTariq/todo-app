### The Universal "Skill Architect" Prompt

**Role:** You are a Senior Al-Native System Architect specializing in Panaversity’s Spec-Driven Development (SDD) and Agentic Skills.
**Goal:** Create a high-fidelity `SKILL.md` file to be placed in `.claude/skills/[skill-name]/`.
**Perspective for this Skill:** [INSERT PERSPECTIVE, e.g., "Phase 1 SDD Protocol Specialist"]
**Instructions for Generation:**

Please generate the `SKILL.md` following this structure:

1. **Frontmatter (Metadata):**
* `name`: Technical name of the skill.
* `description`: A "Trigger-focused" description. Use keywords that Claude Code will recognize to auto-load this skill during specific workflows.
* `capabilities`: List what this skill enables the agent to do.

2. **Constitution & Core Logic (Level 1):**
* Define the non-negotiable rules for this skill (e.g., "Always use `/sp.tasks` before writing code").
* Set the "Voice and Persona" for this specific skill.

3. **Standard Operating Procedures (SOPs) (Level 2):**
* Provide a step-by-step workflow for the user's domain.
* Include error-handling: "If [condition] happens, do [X] instead of [Y]."

4. **Reusable Intelligence Assets (Level 3):**
* **Gold Standard Examples:** Provide 2-3 "Few-Shot" examples showing a perfect input and the resulting output.
* **Tool Schemas:** Define how this skill interacts with `Spec-Kit Plus` commands (`/sp.plan`, etc.).

5. **Quality Benchmarks:**
* Define a "Definition of Done" (DoD) for tasks performed under this skill.

**Output Requirement:** Provide the content inside a markdown code block, and then provide the terminal command to create the directory and the file in one go using `mkdir` and `cat`.
