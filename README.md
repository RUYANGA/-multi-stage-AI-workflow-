# Multi-Stage AI Workflow: Chat → IDE → CLI

## 1. Problem Selected

**Add a validated email-signup rule to a codebase**, broken into three natural
stages: *specify the rules*, *implement the code*, *verify and ship it*.
This splits cleanly across three different AI UX types because each stage
needs a different kind of interaction:

| Stage | Needs | Best UX type |
|---|---|---|
| Define business rules & edge cases | Freeform discussion, brainstorming | **Chat** |
| Write code that fits the existing project | File/context awareness, inline edits | **IDE** |
| Run tests, lint, commit | Deterministic execution, automation | **CLI** |

## 2. Tools Used (kept provider-agnostic)

- **Chat UX** — any general chat assistant (ChatGPT, Claude, Gemini)
- **IDE UX** — any AI-assisted editor (VS Code + Copilot/Cursor, JetBrains AI)
- **CLI UX** — any terminal-based AI agent (Claude Code, Gemini CLI, Aider)

No stage depends on a specific model or vendor — only on the *shape* of the
interface (chat window vs. editor-integrated vs. shell-integrated).

## 3. Workflow Diagram

See `workflow-diagram.mermaid` (rendered alongside this doc). Summary:

```
[Problem] → Chat (spec.json) → IDE (validator.py + test_validator.py) → CLI (pytest, lint, commit) → Merged
                                                    ▲__________________________|
                                                     (loop back on test failure)
```

## 4. Step-by-Step Notes

### Stage 1 — Chat: produce a structured spec
**Prompt used:**
> "Draft a JSON spec for an email validator: business rules, a function
> signature, and a list of test cases with expected results. Output only
> JSON."

**Output → `spec.json`** — a machine-readable contract listing:
- validation rules (character counts, domain shape, disposable-domain block)
- the exact function signature to implement
- concrete input/expected-output test cases

This file is the **hand-off artifact** between Stage 1 and Stage 2. Using a
structured format (JSON) rather than prose is what makes the chain
reliable — the IDE stage doesn't have to re-interpret intent.

### Stage 2 — IDE: implement against the spec
**Prompt used (in-editor):**
> "Implement `validate_email` per `spec.json`, matching this project's
> style, and generate a pytest file that runs every case in
> `spec.json.test_cases`."

**Output →** `validator.py` (implementation) and `test_validator.py` (tests
that load `spec.json` directly, so the tests and the spec never drift
apart).

### Stage 3 — CLI: verify and ship
**Commands run:**
```bash
pytest test_validator.py -v
python -m pyflakes validator.py test_validator.py
```
**Result:** 2/2 tests passed, no lint warnings. The CLI agent then generates
a conventional-commit message (`commit_message.txt`) summarizing what was
added and confirming test status — ready for a real `git commit` /
PR-creation step.

If tests had failed, the CLI stage's output (the failure trace) becomes the
**input to a follow-up IDE-stage prompt** ("fix `validate_email` so this
failing case passes"), closing the loop shown in the diagram.

## 5. Why This Is Adaptable

- The hand-off format at each boundary is a **plain file** (`spec.json`,
  `.py` files, terminal output) — not a vendor-specific API payload. Any
  chat tool can produce the JSON; any IDE assistant can consume it; any CLI
  agent can run the tests.
- Swapping providers only means changing *where you paste the prompt*, not
  the workflow structure itself.

## 6. Efficiency Gained

Manually, this task would require: writing rules from memory, hand-coding
the validator, hand-writing tests, running them, and writing a commit
message — five manual context switches. Here, the human only writes two
prompts and runs one command; the rest is machine-to-machine hand-off via
files.

## 7. Files in This Deliverable

| File | Produced by | Purpose |
|---|---|---|
| `spec.json` | Chat stage | Structured requirements + test cases |
| `validator.py` | IDE stage | Implementation |
| `test_validator.py` | IDE stage | Tests derived from spec |
| `commit_message.txt` | CLI stage | Final shippable artifact |
| `workflow-diagram.mermaid` | — | Visual diagram of the chain |
