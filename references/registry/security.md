<!-- translated from upstream/references/registry/security.md @ e233797 — see docs/TRANSLATION.md -->
# Source registry — Security and reliability

Advisory feeds, threat intel, infrastructure state.

**Verified:** 2026-08-05 — every address answered a live request at the time of reconnaissance. Only sources of value 5 out of 5 were selected.
**The addresses are final, after redirects** — the original check ran without `curl -L`, otherwise a dead address is painted green by a response from a redirect.
**Entries:** 19, of them 1 require a key or registration.

The registry answers "where to look for this signal", not "how reliable the source is": the credibility column is a reconnaissance estimate, not a Phase 5 result. The provenance of a number is still checked via `source_scoring.md`. The shelf life of such a list is months; a dead address is not a registry bug but a signal to re-check.

| Source | Address | Signal | Access | Credibility |
|---|---|---|---|---|
| Ookla Speedtest Open Data — Global Fixed & Mobile Network Performance (AWS Open Data / S3 bulk parquet) | <https://ookla-open-data.s3.amazonaws.com/?list-type=2&prefix=parquet/performance/type=mobile/year=2026/quarter=1/> | infra-reliability-signal | free | high |
| RIPE NCC RIPEstat — Routing Status API (BGP/RIS data) | <https://stat.ripe.net/data/routing-status/data.json?resource=AS3333> | infra-reliability-signal | free | high |
| Submarine Cable Map (TeleGeography) — GeoJSON map of submarine cables | <https://www.submarinecablemap.com/api/v3/cable/cable-geo.json> | infra-reliability-signal | free | high |
| npm Status Incident History RSS | <https://status.npmjs.org/history.rss> | infra-reliability-signal | free | high |
| AWS Security Bulletins — RSS | <https://aws.amazon.com/security/security-bulletins/rss/feed/> | security-advisory-signal | free | high |
| CISA — All Cybersecurity Advisories RSS Feed | <https://www.cisa.gov/cybersecurity-advisories/all.xml> | security-advisory-signal | free | high |
| Chrome Releases Blog — RSS | <https://chromereleases.googleblog.com/feeds/posts/default?alt=rss> | security-advisory-signal | free | high |
| Debian Security Advisories — RDF/RSS Feed | <https://www.debian.org/security/dsa-long> | security-advisory-signal | free | high |
| GitHub Security Advisories API | <https://api.github.com/advisories?per_page=5> | security-advisory-signal | free | high |
| Go Vulnerability Database — vulns index JSON | <https://vuln.go.dev/index/vulns.json> | security-advisory-signal | free | high |
| JPCERT/CC — RSS Feed | <https://www.jpcert.or.jp/rss/jpcert.rdf> | security-advisory-signal | free | high |
| Kubernetes Official CVE Feed — JSON Feed | <https://kubernetes.io/docs/reference/issues-security/official-cve-feed/index.json> | security-advisory-signal | free | high |
| Microsoft Security Response Center — Security Update Guide RSS | <https://api.msrc.microsoft.com/update-guide/rss> | security-advisory-signal | free | high |
| RustSec Advisory Database — Atom Feed | <https://rustsec.org/feed.xml> | security-advisory-signal | free | high |
| WPScan — WordPress Vulnerability Database RSS | <https://wpscan.com/feed/> | security-advisory-signal | free | high |
| Abuse.ch ThreatFox — IOC Sharing API | <https://threatfox-api.abuse.ch/api/v1/> | threat-intel-signal | нужен ключ | high |
| AlienVault OTX — Indicator Lookup API | <https://otx.alienvault.com/api/v1/indicators/domain/google.com/general> | threat-intel-signal | free | high |
| GIFCT — WordPress REST API | <https://gifct.org/wp-json/wp/v2/posts> | threat-intel-signal | free | high |
| MITRE ATT&CK Enterprise — STIX 2.0 Bundle | <https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json> | threat-intel-signal | free | high |
