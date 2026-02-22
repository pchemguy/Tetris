### Architectural Domains (Derived from L2 Decomposition)

The following domains are derived directly from the system decomposition
defined in `DECOMPOSITION.md`.

1. `CORE`
   - Corresponds to the Core (Engine) component.
   - Pure deterministic simulation.
   - No I/O, timing, or platform interaction.

2. `SHELL_BASELINE`
   - Corresponds to all baseline shell components:
     - Renderer (pure transformer),
     - Runtime,
     - Input Driver,
     - Input Controller,
     - Presenter,
     - CLI,
     - Baseline persistence.
   - Responsible for orchestration and environment interaction.

3. `CORE_EXTENSIONS`
   - Optional behavioral extensions of the Core component.
   - Remain inside the Core boundary.
   - Preserve deterministic semantics.

4. `VARIANTS`
   - Alternative implementations of shell components
     (e.g., graphical renderer, web UI, alternative runtimes).
   - Must preserve Core contracts.

5. `BENCHMARK`
   - Test & evaluation harness and scoring infrastructure.
   - Does not alter system semantics.