# Repository-maintenance demo scenarios

This repository contains controlled scenarios for a custodian demonstration.
The input defect is deliberate and has an expected-failure regression test.
Seeded GitHub issues should identify themselves as demo scenarios, not real user
reports. Do not put personal information, credentials or tokens in them.

## Blank task from spaces

Use a separate local file:

```bash
python3 todo.py --file data/blank-demo.json add "   "
python3 todo.py --file data/blank-demo.json list
```

The actual result is an entry such as `1. [ ] ` without a title. The expected
behavior is an error with no new task. `add_task` checks for an empty string
before trimming; three spaces are not yet an empty string at that point.
This is a small bug an agent can investigate without executing arbitrary code.

For the cloud demo, the custodian should read the labeled issue, retrieve relevant
context, inspect the permitted function and post a concise evidence-based comment.
It should not change application source automatically.

## README drift after a limit change

Compare the README's Limits section with `MAX_TASK_LENGTH` and the title boundary
tests. A change to that constant can leave the README describing an old limit.
This makes a factual, narrowly scoped documentation-maintenance task.

The custodian should confirm the mismatch and open a README-only pull request.
A human reviews and merges it. Refresh the retrieval index after the merge so
future answers use the corrected document, not a stale copy. A suggestion in chat
alone is not a completed documentation update.

## Due dates as a future request

A separate unlabeled issue can request optional due dates. The app currently has
no deadline field or notification feature. The scheduled custodian can summarize
and classify this request as an enhancement rather than pretending it is a bug.
Adding due dates is outside this demo's application scope.

## Tool boundaries

Allow the custodian to read these docs, approved source snippets and this
repository's issues. Permit comments on selected issues and a controlled
README-only pull request. Do not permit arbitrary file edits, shell execution,
automatic merges or changes to other repositories. The cloud agent's job/run
state is separate from the todo application's local JSON file.
