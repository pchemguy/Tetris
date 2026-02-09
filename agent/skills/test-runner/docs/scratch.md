Next task focuses on development of an agent skill. The skill-based approach aims to use a single-agent to mimic multi-agent environment, where there is a controller agent solely responsible for delegating individual tasks to dedicated expert agents. Each expert task agent is configured with instructions tailored to a class of development tasks, such as test running, test writing, refactoring planning, refactoring execution, etc. In a skill-based design, skills are used to configure a single agent and modulate its context (instead of engineering a separate isolated context for an expert task agent within a multi-agent settings) to assume a specific developer role. This role must be fairly generic. It is not tailored to a project, but to dev strategy. It must also be flexible enough to cover major workflows.

Because skills modulate an existing context, it should be safe to assume that agent already loaded `AGENTS.md` and performed general project discovery. The skill might still reference `AGENTS.md` and, possibly, `PROJECTS.md` as it instructs the agent to perform a limited repo rediscovery focused on the needs of specific role.

Your immediate task is follow my intent and help me forge a well developed description/spec for this role. Then we will use this spec together with skill template for development of an actual skill. Below are preliminary notes on the current role to be used as the starting point for spec development.

The role is the test-runner. 

