Next task focuses on development of an agent skill. The skill-based approach aims to use a single-agent to mimic multi-agent environment, where there is a controller agent solely responsible for delegating individual tasks to dedicated expert agents. Each expert task agent is configured with instructions tailored to a class of development tasks, such as test running, test writing, refactoring planning, refactoring execution, etc.

In a skill-based design, there is a single agent configured to skills are used to configure a single agent and modulate its context (instead of engineering a separate isolated context for an expert task agent within a multi-agent settings) to assume a specific developer role. This role must be fairly generic. It is not tailored to a project, but to dev strategy. It must also be flexible enough to cover major workflows.

Because skills modulate an existing context, it should be safe to assume that agent already loaded `AGENTS.md` and performed general project discovery. The skill might still reference `AGENTS.md` and, possibly, `PROJECTS.md` as it instructs the agent to perform a limited repo rediscovery focused on the needs of specific role.

Your immediate task is follow my intent and help me forge a well developed description/spec for this role. Then we will use this spec together with skill template for development of an actual skill. Below are preliminary notes on the current role to be used as the starting point for spec development.

The role is the test-runner. It may be used to run a specific test module, a set of test module for a group of related source code modules or the whole project test suite. As usual, the primary objective is to verify that specific component or the full project, whichever is appropriate, is in good shape and pass all tests successfully.

ON_FAIL: If any test fails, the objective is to identify all failing tests, collect and log detailed diagnostic information, reason about potential causes, attempting to group errors based on potential common causes.

The general workflow, as usual, involves running the full test suite at the beginning of a work. If any test fail, then follow ON_FAIL protocol, as test-runner never modifies any code. Its sole responsibility is to assess project health as evidenced by the relevant tests and report back 

