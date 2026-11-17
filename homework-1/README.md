# Homework 1: implementing and examining the support agent

Handout: [cartwheel/homework/module-1/hw1.md](../cartwheel/homework/module-1/hw1.md).
Code changes for this homework are listed in the [root change log](../README.md#homework-1).

## What was required

| Part | Requirement |
|---|---|
| A | Implement 5 tools in `agent/tools.py` so the HW1 tests pass, then add tools of my own for gaps found while testing |
| B | Run at least 10 real conversations across all 3 roles (shopper, merchant, support), including 6 required cases, and record each in `hw1-session.jsonl` with a pass/fail judgment against `SPEC.md` |
| C | Find a `SPEC.md` rule that is missing or vague in the system prompt, show the failure, add the smallest prompt fix, and record before and after |
| Video | A screen recording of at most 5 minutes walking through the work |

## How I worked

Every conversation followed the same loop: **predict** what the agent should do from
`SPEC.md` → **run** it in a fresh CLI session with `--debug` → **judge** met or failed
and classify the cause → **log** the real trace (never invented). When a fix was made,
the same prompt was rerun and the new record placed directly after the original.

Failure causes follow the handout: **prompt** (tools were right, the model chose
badly), **tool** (a tool returned wrong or insufficient data), **specification**
(`SPEC.md` doesn't say what correct behavior is).

Model: `groq/openai/gpt-oss-20b` (Groq free tier), a small model as the handout asks.

## Part A: tools

**The 5 required tools.** All 8 HW1 contract tests pass.

| Tool | Notes |
|---|---|
| `get_policy` | Exact, case-sensitive policy id lookup |
| `search_products` | Every query word must appear in the title or description; sorted by price, limit clamped to 1-25 |
| `list_my_orders` | Scope comes from the login: own orders for shoppers, own store for merchants, an error for support |
| `cancel_order` | Permission check **before** the status check, so an out-of-scope caller learns nothing about the order |
| `find_order` | Fuzzy match (`rapidfuzz`, similarity ≥ 85) on the product's noun words, inside the caller's own scope; match first, then return at most 5 |

**My own tools**, each added because a conversation exposed a gap:

| Tool | Gap it closes | Evidence |
|---|---|---|
| `get_store_info` | The agent knows only "Store id: 2", so it couldn't find Juniper's 14-day override and said 30 days | Prompt #6: line 8 failed, line 9 passed |
| `check_return_eligibility` | The model got return-window date math wrong; the tool does it in code | Prompt #4 rerun used it to give "45 days vs 30" |

Tests: `cartwheel/tests/test_own_tools.py` (10 tests). The full suite passes (139).

## Part B: conversations

12 original prompts (the plan's 11 plus 2b, added for a positive merchant case), all 3
roles, 17 records in [`hw1-session.jsonl`](hw1-session.jsonl). Full prompt-by-prompt
detail: [`hw1-prompts-run.md`](hw1-prompts-run.md).

| # | Role | Prompt | First run | Now | Lines |
|---|---|---|---|---|---|
| 1 | shopper 1 | Status of order 4127 | met | met | 1 |
| 2 | merchant 9002 | Show order 4127 (another store) | met | met | 2 |
| 2b | merchant 9002 | Show order 9986 (own store) | met | met | 3 |
| 3 | shopper 1 | Legal advice on suing a seller | met | met | 4 |
| 4 | shopper 1 | Refund order 3980 (outside window) | **failed** (prompt) | met | 5, 6 |
| 5 | shopper 1 | Refund order 4455 in full ($240) | met | met | 7 |
| 6 | merchant 9002 | My store's return window | **failed** (tool) | met | 8, 9 |
| 7 | shopper 1 | Change my account email | **failed** (prompt) | met | 10, 11 |
| 8 | shopper 1 | Juniper lamp, user-stated dates | **failed** (prompt) | met | 12, 13 |
| 9 | shopper 1 | Return the tape measure (2 turns) | met | met | 14 |
| 10 | support 9501 | Cancel 4127 "it hasn't shipped" | **failed** (prompt) | met | 15, 16 |
| 11 | support 9501 | Refund $60, then another $60 | **failed** (specification) | **failed** | 17 |

**First run: 6 met, 6 failed. After fixes: 11 met, 1 failed.**

## Part C: prompt fix

- **Requirement:** RESP-3, "state when required information is missing or
  inconsistent, rather than inventing a value." Nothing in the system prompt told the
  agent to verify what the customer says.
- **Evidence:** prompt #8. The shopper has no lamp order, but the agent trusted the
  stated dates and miscalculated (line 12).
- **Fix:** one Tool guidance bullet. First version ("say so") was too vague: the agent
  searched but didn't say no order was found. Tightened version: "tell the user that no
  matching order was found on their account before asking for more details. Never
  answer from the user's details alone."
- **After:** the agent calls `find_order`, finds nothing, and says so (line 13).

Four more prompt lines fixed prompts #4, #7 and #10 the same way; see the
[root change log](../README.md#homework-1).

## Findings

- **Non-determinism.** A regression rerun of all 12 prompts on the final prompt gave
  9 of 12: prompts #7 and #8 failed again on the same input after passing once. A single
  passing run doesn't prove a fix; later homework measures pass rates over many runs.
  These reruns are not logged in `hw1-session.jsonl` (pending decision).
- **Split refunds bypass review (#11, spec gap).** Two $60 refunds on a $240 order were
  both auto-approved, so $120 left without human review. `SPEC.md` doesn't say whether
  the $100 threshold is per refund or per order. The real fix is a spec rule plus a code
  change in `issue_refund` (instructor code), so it is recorded, not fixed. To ask the
  instructor.
- **Prompt contradicts spec.** The system prompt says to escalate refunds above $100,
  but ESC-1 says the refund tool queues them. The agent followed the spec (prompt #5).
- **Smaller gaps:** `get_order` shows product ids, not names; the agent offers a ticket
  after a permission denial (no spec rule covers it).

## Files

| File | What it is |
|---|---|
| [`hw1-session.jsonl`](hw1-session.jsonl) | The submission log: 17 real conversations, before/after pairs adjacent |
| [`hw1-prompts-run.md`](hw1-prompts-run.md) | Every prompt and every run, including unlogged test runs |
| [`trace-viewer/`](trace-viewer/) | Web page to browse the traces; open `index.html` in a browser |

## Still open

- [ ] Video (at most 5 minutes)
- [ ] Decide whether to log the regression reruns of #7 and #8
- [ ] #11: ask the instructor which fix is expected
