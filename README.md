# AI-eval

My work for the course **Evaluating and Improving AI Agents**. The course uses one
support agent, **Cartwheel**, across every homework, so this repo keeps one copy of
the agent's code and a separate folder for each homework's results.

## Structure

```
AI-eval/
├── README.md        ← this file: structure and every change to the course code
├── TRACKER.md       ← progress across all 9 homeworks
├── cartwheel/       ← the course code with my changes (the agent you run)
├── homework-1/      ← HW1: conversations, findings, trace viewer
└── homework-2/ … homework-9/   ← added as each homework starts
```

- **`cartwheel/`** is the course repository
  ([ai-evals-course/cartwheel-homeworks](https://github.com/ai-evals-course/cartwheel-homeworks))
  plus my edits. The agent only runs with those edits in place, so they live here and
  are listed in the change log below.
- **`homework-N/`** holds what each homework asked for and produced, with its own
  README explaining what was required, what I did, and how.

## Homework status

**1 of 9 homeworks substantially done (HW1, video pending).** Full progress, every
homework and the HW1 checklist: [TRACKER.md](TRACKER.md).

## Running the agent

Run every command from `cartwheel/`:

```bash
cd cartwheel
uv sync
uv run python -m seed.generate
cp .env.example .env   # then add one model key; never commit .env
uv run python -m agent.cli --role shopper --user 1 --debug
```

I used Groq's free tier (`CARTWHEEL_MODEL=groq/openai/gpt-oss-20b`, `GROQ_API_KEY`)
instead of the course default `gpt-4o-mini`.

## Change log: my changes to the course code

**Baseline:** course repo commit `a3aa8d5` (2026-10-09). Everything below is a change
from that baseline. New entries go at the bottom of each homework's section, and a new
section is added per homework.

### Homework 1

| File in `cartwheel/` | Original | Changed to | Why |
|---|---|---|---|
| `agent/tools.py` | 5 functions raised `NotImplementedError` | Implemented `get_policy`, `search_products`, `list_my_orders`, `cancel_order`, `find_order` | HW1 Part A |
| `agent/tools.py` | – | **New tool** `get_store_info` | Agent only knew "Store id: 2", so it gave the 30-day default instead of Juniper's 14-day override (HW1 prompt #6) |
| `agent/tools.py` | – | **New tool** `check_return_eligibility` | Agent did return-window date math wrong (HW1 prompt #8); the tool does it in code with the course's own `seed/eligibility.py` |
| `agent/agent.py` | `list_my_orders` used a strict tool schema | `@function_tool(strict_mode=False)` | Groq rejects a strict schema with no parameters; infrastructure fix, no behavior change |
| `agent/agent.py` | – | Wrappers for the 2 new tools, registered for all roles | So the model can call them |
| `agent/agent.py` (system prompt, Tool guidance) | "Cite the policy id … for every policy claim." | Added: "When a tool result includes a policy_id, include that id in your reply." | Agent had the id and didn't cite it (RESP-1, prompt #4) |
| `agent/agent.py` (system prompt, Tool guidance) | – | Added: don't rely on order details the user states; verify with `find_order`/`get_order`; say when no order matches | Agent answered from user-stated dates (RESP-3, prompt #8). **This is the HW1 Part C fix.** |
| `agent/agent.py` (system prompt, Tool guidance) | – | Added: only describe steps or processes found in a retrieved policy or tool result; cite only policies looked up | Agent invented a 5-step return process (RESP-3, prompt #10) |
| `agent/agent.py` (system prompt, Escalation) | – | Added: account changes of any kind always go to `escalate_to_human`, no self-service steps | Prompt never mentioned account changes (ESC-2, prompt #7) |
| `agent/agent.py` (system prompt, Escalation) | – | Added: don't escalate when the tools give a clear answer | Agent opened a needless ticket for a clear "not eligible" (prompt #4) |
| `SPEC.md` | Tools TOOL-1 to TOOL-9 | Added rows for TOOL-10 and TOOL-11, marked 🆕 "(added in HW1)" | Keep the spec's tool list complete; no requirement rules changed |
| `tests/test_own_tools.py` | – | **New file**, 10 tests for the 2 new tools | Unit tests for my code |
| `pyproject.toml`, `uv.lock` | `rapidfuzz` installed only indirectly | `rapidfuzz` as a direct dependency | Used by `find_order` |
| `.gitignore` | – | Added `.env.example` | My choice; the file was already tracked upstream and holds no keys |

Not changed on purpose: `agent/auth.py`, `agent/db.py`, and the refund logic in
`issue_refund`, which are instructor code. The split-refund finding (HW1 prompt #11) is
recorded, not fixed; see [homework-1](homework-1/README.md).
