<!-- translated from upstream/references/stat_sources/industries/hr_workforce.md @ e233797 — see docs/TRANSLATION.md -->
# HR / Labor / Workforce

## Tier 1

### LinkedIn Workforce Reports
**URL:** economicgraph.linkedin.com
**Access:** OPEN
**What:** Labor market dynamics derived from LinkedIn data — hiring rates, skills gaps, migration
**When:** labor market trends, white-collar hiring
**Quality:** B (LinkedIn user bias but a huge sample)

### Indeed Hiring Lab
**URL:** hiringlab.org
**Access:** OPEN
**What:** Labor market analysis based on Indeed job postings
**When:** labor demand by occupation/location
**Quality:** B

### Glassdoor Economic Research
**URL:** glassdoor.com/research
**Access:** OPEN
**What:** Salary research, employer reviews economics
**When:** salary benchmarks, employee sentiment

### BLS (US labor)
See core/gov_macro.md.

### Eurostat Labour Market
See core/gov_macro.md (Eurostat).

## Tier 2

### OECD Employment Database
**URL:** oecd.org/employment/database
**Access:** OPEN
**What:** Detailed labor market data OECD members
**When:** cross-country labor comparison

### ILO
**URL:** ilostat.ilo.org
**Access:** OPEN
**What:** International Labour Organization — global labor statistics
**When:** global labor including developing countries

### WEF Future of Jobs Reports
**URL:** weforum.org/reports
**Access:** OPEN
**What:** Future of jobs research, skills, automation impact
**When:** future workforce trends

### Mercer Talent Trends
**URL:** mercer.com/insights/talent-and-transformation
**Access:** OPEN summaries
**What:** Annual talent trends survey
**When:** HR trends survey

### Payscale
**URL:** payscale.com/research
**Access:** OPEN
**What:** Salary data + market reports
**When:** salary benchmarks

### Salary.com
**URL:** salary.com — partial
**Access:** OPEN basic
**What:** US salary benchmarks

### Levels.fyi
**URL:** levels.fyi
**Access:** PARTIAL — the home page (`www.levels.fyi`) returns HTTP 200 (marketing content, without concrete figures), but the company/salary pages (`/companies/<company>/salaries/<role>`, including the `.md` variant) return HTTP 202 with an empty body and the header `x-amzn-waf-action: challenge` — this is an AWS WAF JS challenge on CloudFront, not the 403 that the 05.08 reconnaissance named, but in effect the same result: without passing the challenge there is no data
**What:** Tech compensation data (self-reported)
**When:** tech total compensation analysis
**Quality:** B-C (self-reported but extensive coverage of tech roles)
**Limitations:** The entry's main promise — detailed salary tables by company/role — is closed by an AWS WAF challenge at the request level, programmatic access is impossible. There is no official public API (confirmed by the founder in a Levels.fyi community thread: "No API, but we have some embeds"). A paid enterprise data offering exists (`levels.fyi/offerings/data/`, checked — HTTP 200), but that is not live access, it is a separate commercial product.
**Fallback if blocked:** H1B Salary Database (h1bdata.info, see below in this file) — checked with a live request on 2026-08-17, HTTP 200, real base salary figures from H1B filings. Payscale (payscale.com/research) — also checked with a live request on 2026-08-17, HTTP 200, real content with medians/averages. In that same check Glassdoor and Salary.com turned out to be behind a Cloudflare challenge (403) — do not use them as a fallback without separate verification.
**Verified:** 2026-08-17

### H1B Salary Database
**URL:** h1bdata.info
**Access:** OPEN
**What:** US H1B salary disclosures (legally public)
**When:** US tech salaries by company verifiable

## Specific topics

### Remote work
- **Owl Labs State of Remote Work** — OPEN
- **GitLab Remote Work Report** — OPEN
- **Buffer State of Remote Work** — OPEN annual

### DEI / Diversity
- **McKinsey Diversity Wins** — OPEN
- **Catalyst** — `catalyst.org` — OPEN

### Tech-specific labor
- **Stack Overflow Developer Survey** (see consulting_industry.md)
- **JetBrains State of Developer** (see consulting_industry.md)
- **Hired State of Software Engineers** — OPEN

## Combining patterns

**US labor market:**
BLS (official) + LinkedIn Workforce + Indeed Hiring Lab + ADP National Employment + Conference Board

**Salary research:**
Payscale + Glassdoor + Salary.com + Levels.fyi (tech) + H1B database (verifiable US tech) + company-specific from interviews

**Future of work / skills:**
WEF Future of Jobs + LinkedIn skills data + Mercer trends + McKinsey research + OECD employment outlook
