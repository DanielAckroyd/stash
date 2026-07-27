# Usage budget — delegate to cheaper models when logical

I'm on a limited-usage subscription. Top-tier model tokens (Fable/Opus) are the
scarce resource — don't spend them on work a cheaper model handles fine.

- **Delegate to a `haiku` subagent:** broad codebase searches (use the `Explore`
  agent type), log/output summarization, mechanical or repetitive edits with an
  exact recipe.
- **Delegate to a `sonnet` subagent:** self-contained implementation tasks with a
  clear spec, routine test writing, straightforward refactors.
- **Delegate to an `opus` subagent:** meatier-than-Sonnet tasks in well-trodden
  territory — larger features or refactors where the domain and patterns are
  well established and the prompt can spell them out. Don't treat Opus as
  "Fable minus context": it has shipped bugs and dropped the ball on things
  Fable gets right intuitively. If a task needs judgment calls, novel design,
  or subtle correctness reasoning, it isn't an Opus task even if it's
  self-contained.
- **Keep on the top model:** design and architecture reasoning, correctness-critical
  work, gnarly debugging, anything needing the full conversation context, and
  final review of delegated output.
- Delegation only pays when the task fits a self-contained prompt — subagents start
  cold. If writing the handoff prompt costs more than the task, do it inline.
- Forks (`subagent_type: "fork"`) run on the parent model and ignore `model`
  overrides — they never save usage. Use a fresh agent with an explicit `model`.
- Sanity-check delegated results before reporting them as done.
