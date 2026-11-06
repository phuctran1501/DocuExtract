# Gemini + Antigravity Prompt Playbook

Use one bounded task per prompt. Let the repository instructions and skills carry the repeated rules; prompts should describe the desired outcome and constraints.

## 1. First conversation in a new workspace

```text
Read AGENTS.md and the documentation map in README.md. Inspect the complete repository tree, current Git status, Python project configuration, and existing tests. Do not modify any files yet. Report:
1. What already exists and what is missing.
2. Whether the implementation matches the product and architecture documents.
3. The smallest useful first milestone.
4. Risks or conflicting assumptions.
Do not invent code or claim commands were run unless they were actually run.
```

## 2. Plan a feature

```text
Use the plan-feature skill. I want to implement: [describe one outcome].
Inspect the current implementation first. Read the relevant requirements and API contract. Produce a plan with scope/non-goals, files, API changes, ordered steps, tests, security risks, and documentation updates. Do not change source code yet.
```

## 3. Implement an approved plan

```text
Use the implement-feature skill. Implement the approved plan: [path to plan or pasted plan].
Keep the diff focused, add tests for success and failure cases, update the API contract if behavior changes, and run the relevant checks. Stop and report if the plan conflicts with the repository or requires a material architectural decision.
```

## 4. Debug a failure

```text
Reproduce and diagnose this failure before changing code: [error, command, steps].
Trace the request/data flow, identify the most likely root cause, and distinguish evidence from hypotheses. Propose the smallest safe fix and the regression test. Do not suppress the exception or weaken tests to make the command green.
```

## 5. Review before accepting a change

```text
Use the review-change skill. Review the current Git diff as a senior Python backend reviewer. Prioritize correctness, API compatibility, upload security, async/blocking behavior, error handling, tests, and unintended scope. Report findings by severity with file/line references. Do not edit files unless I ask you to fix the findings.
```

## 6. Prepare ASP.NET Core integration

```text
Use the integrate-aspnet skill. Based on docs/architecture/api-contract.md, design the .NET integration boundary for an ASP.NET Core Clean Architecture application. Keep the Application layer independent of HTTP transport and put the typed HttpClient adapter in Infrastructure. Include timeout, CancellationToken, correlation ID, response mapping, and downstream failure handling. Do not add .NET source files to this repository unless I explicitly request it.
```

## 7. Ask for a learning explanation

```text
Explain the implementation in Vietnamese as if I know C#/.NET but am new to Python. Compare the relevant Python/FastAPI concepts with familiar C#/.NET concepts. Explain the request flow, important trade-offs, and what I should inspect or test myself. Do not rewrite the code just to demonstrate another style.
```

## 8. Useful operating pattern

1. Ask for repository reconnaissance.
2. Ask for a plan for medium/large work.
3. Approve or revise the plan.
4. Implement one vertical slice.
5. Review the diff and test results.
6. Update docs/dev log.
7. Commit only after the owner accepts the result.
