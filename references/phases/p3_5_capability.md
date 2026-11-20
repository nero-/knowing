<!-- translated from upstream/references/phases/p3_5_capability.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 3.5. Capability Discovery

**Model:** `mid` / `low`. A mechanical pass over env vars and tables.

**Optional** for shallow. **Recommended** for medium. **Mandatory** for deep.

Between planning and launching the search — a sanity check: what do we actually have available?

See `capability_discovery.md` for the detailed workflow. The short version:

### Step 1: Audit env vars

Check for the existence of env vars for the API keys planned in the plan.md section 12:

```
$FRED_API_KEY, $GITHUB_TOKEN, $NEWSAPI_KEY, ...
```

The full list — `capability_discovery.md` section "Step 1".

### Step 2: Map subtopics to capabilities

For each subtopic → a table: planned source × status (`authenticated` / `open-no-auth` / `fallback` / `unavailable`).

### Step 3: Discover unknown gaps

If the plans do not cover the whole topic — fall back to `awesome_lists_registry.md` for discovery:

```
for subtopic X:
  if not found in my catalog → find an upstream awesome-list
  → WebFetch its README
  → identify 1-3 candidates → add as ad-hoc to plan.md
```

### Step 4: Report to user

A summary report:
- ✅ Available: [list]
- ⚠ Fallback: [list]
- ❌ Unavailable: [list]
- ❓ Ad-hoc from upstream: [list]
- Suggest env vars: [list]

User confirms continue.

### Step 5: Update plan.md

Extend `plan.md` section 12 (Information sourcing strategy) per subtopic with a "Capabilities check" block:

```markdown
**Capabilities check (Phase 3.5):**
- ✅ FRED API: authenticated, will use directly
- ⚠ Brave Search: no key → fallback to standard WebSearch
- ❓ Niche topic — using ad-hoc API from public-apis registry
```
