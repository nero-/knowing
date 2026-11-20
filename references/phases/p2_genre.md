<!-- translated from upstream/references/phases/p2_genre.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 2. Genre & block selection

**Model:** `mid` / `medium`.

After reframing, before the plan — we determine what type of report we are assembling.

**Steps:**

1. Read `genres.md` — it holds the heuristic for choosing a genre by the signals in the question.
2. Apply the heuristic:
   - «how does it work» → explainer
   - «what to choose, X or Y» → decision
   - «map», «who does it» → landscape
   - «is it true», «does it work» → validation
   - open, a series of questions → qa
   - «by metrics», a mix, something non-standard → custom

3. For a standard genre — take the block preset from `genres.md`.

4. For custom — assemble the block list:
   - Base scaffolding: `tldr`, `scope` (if the boundaries matter), `counter-arguments`, `open-questions`, `next-research`, `map-of-sources`, `metadata`.
   - Heuristic by the signals in the question (see `genres.md`, the `## Genre selection heuristics` table).
   - If the question is hybrid (e.g. «how it works + what to choose») — combine blocks from both genres.

5. Announce to the user in ONE line:
   ```
   "Genre: <genre>. Blocks: <list>. Ok?"
   ```
   For example:
   ```
   "Genre: custom (competitors by metrics). Blocks: tldr, scope, data-table,
    profile-card×N, trends, counter-args, open-q, next-research, sources, metadata. Ok?"
   ```

6. If the user edits it — update the set.

7. Record the final set in `plan.md` (see Phase 3).

**Do not load all the category files `blocks/*.md` at once.** Only those that are needed for the chosen blocks — after the plan phase.
