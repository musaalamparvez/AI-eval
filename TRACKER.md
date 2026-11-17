# Course tracker

Where I stand in **Evaluating and Improving AI Agents**. Update this file whenever a
task finishes. Homework list from the course index:
[cartwheel/homework/README.md](cartwheel/homework/README.md).

## Overall

**1 of 9 homeworks substantially done (HW1, video pending). 8 not started.**

```
HW1 ▓▓▓▓▓▓▓▓▓░  90%   video left
HW2 ░░░░░░░░░░   0%
HW3 ░░░░░░░░░░   0%
HW4 ░░░░░░░░░░   0%
HW5 ░░░░░░░░░░   0%
HW6 ░░░░░░░░░░   0%
HW7 ░░░░░░░░░░   0%
HW8 ░░░░░░░░░░   0%
HW9 ░░░░░░░░░░   0%
```

## All homework

| Module | HW | Topic | Handout | Status | My folder |
|---|---|---|---|---|---|
| 1 | 1 | Build the support agent's tools, test in conversation, fix the prompt | [hw1.md](cartwheel/homework/module-1/hw1.md) | 🟡 Video pending | [homework-1](homework-1/README.md) |
| 1 | 2 | Authenticated sessions and tracing | [hw2.md](cartwheel/homework/module-1/hw2.md) | ⬜ Not started | – |
| 1 | 3 | Support scenario dataset and trace export | [hw3.md](cartwheel/homework/module-1/hw3.md) | ⬜ Not started | – |
| 2 | 4 | Review traces and define failure modes | [hw4.md](cartwheel/homework/module-2/hw4.md) | ⬜ Not started | – |
| 2 | 5 | Develop and test an LLM judge | [hw5.md](cartwheel/homework/module-2/hw5.md) | ⬜ Not started | – |
| 3 | 6 | Continuous integration for the agent | [hw6.md](cartwheel/homework/module-3/hw6.md) | ⬜ Not started | – |
| 3 | 7 | Monitor one failure mode after deployment | [hw7.md](cartwheel/homework/module-3/hw7.md) | ⬜ Not started | – |
| 5 | 8 | Improve accuracy on one failure mode; Pareto comparison | [hw8.md](cartwheel/homework/module-5/hw8.md) | ⬜ Not started | – |
| 5 | 9 | Reduce cost: fewer tokens, caching, model cascade | [hw9.md](cartwheel/homework/module-5/hw9.md) | ⬜ Not started | – |

Module 4 has no homework in the course index. Status key: ✅ done, 🟡 in progress,
⬜ not started.

## HW1 checklist

- [x] Setup: dependencies, seeded data, model key (Groq)
- [x] Part A: 5 required tools, all 8 HW1 tests passing
- [x] Part A: own tools `get_store_info` and `check_return_eligibility`, 10 tests
- [x] Part B: 12 prompts, all 3 roles, 17 records in `hw1-session.jsonl`
- [x] Part C: RESP-3 prompt fix with before/after records
- [x] Extra: fixed prompts #4, #6, #7, #10; trace viewer
- [ ] Video, at most 5 minutes
- [ ] Decide: log the regression reruns of #7 and #8?
- [ ] Ask instructor about #11 (split refund)
