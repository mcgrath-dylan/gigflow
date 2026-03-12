# Project North Star: AI-Assisted Freelance Pipeline

## Last Updated: March 12, 2026

---

## ⚡ SESSION STATE — READ THIS FIRST

> **Claude: When Dylan says "pick up where we left off," read this block and resume accordingly.**

**Current Phase:** 3 — Expand Sources + Refine
**Current Micro-Task:** 3.3 — Phase 4 outbound strategy
**Session Count:** 5
**Progression Level:** Supervised
**Last Session Date:** 2026-03-12
**Last Session Summary:** Added HN scraper (monthly, Algolia search, require_terms filter). Expanded Reddit to 5 subreddits (added r/freelance_forhire, r/WorkOnline, r/HireaWriter) with tag_exempt_subreddits config for subreddits that don't use [Hiring] tags. Investigated + eliminated Craigslist (403 on all endpoints) and RemoteOK (90% full-time engineering). Tightened keywords — replaced broad "report"/"analysis" with "data report"/"data analysis", added "sop", "standard operating procedure", "data quality", "process documentation".
**Blockers / Open Issues:** Source quality ceiling identified: high AI-deliverability gigs (data cleanup, SOPs, spreadsheet work) are posted by non-technical people who don't use developer platforms. Inbound monitoring alone is unlikely to fund the tools.
**Next Action:** Phase 4 — Outbound strategy. Options: (a) post Dylan's services to the same subreddits as [For Hire], (b) simple portfolio page on GitHub Pages, (c) both. Decide and build.

### How to resume

1. Greet Dylan briefly. State the current micro-task and what it involves.
2. If there were blockers from last session, address those first.
3. Follow the Learning Protocol (Section 6) at the current Progression Level.
4. At session end, run the Handoff Protocol (Section 6) and tell Dylan what to update in this block.

---

## 1. Project Identity

**Codename:** GigFlow
**Owner:** Dylan
**AI Partner:** Claude (Anthropic)
**Status:** Phases 1–3 complete — Phase 4 starting

### What This Is

An automated pipeline that finds freelance gigs, scores them for fit, drafts proposals, and streamlines delivery — with AI handling ~80% of production work and Dylan providing ~20% (judgment, QA, client communication).

### What This Is NOT

- A startup or product to sell
- A full-time freelancing career
- A replacement for Dylan's day job or AE career pivot goals

---

## 2. Strategic Context

### Two-Bucket Framework

This project exists within a broader personal strategy:

| | Bucket 1: Fund the Tools | Bucket 2: Build Toward AE |
|---|---|---|
| **Goal** | Self-sustaining AI subscription income ($100-200/mo) | Portfolio, skills, visibility for Analytics Engineering pivot |
| **Timeline** | Immediate | 6-18 months |
| **Overlap** | Building this pipeline IS an AE-relevant portfolio piece (data pipelines, APIs, Python, automation) |

**Critical rule:** Bucket 1 decisions should never compromise Bucket 2 goals. If a shortcut makes money but teaches nothing, skip it.

### Constraints

- **Time budget:** 2-3 hours/week until proven, then scale up
- **Financial budget:** Minimal. Claude API costs (~$5/mo), free-tier tooling preferred
- **Dylan's current role:** Business Analyst, Data Governance team at LFG
- **Core skills to leverage:** Data standards/policy documentation, light analysis/reporting, stakeholder translation (technical ↔ business), spreadsheet/data cleanup
- **No existing freelance network** — cold-start problem is real and acknowledged

---

## 3. Architecture Overview

```
[Sources] → [Scraper/Monitor] → [Scoring Engine] → [Daily Digest] → [Dylan Reviews]
                                                                          ↓
                                                              [Proposal Drafting] → [Dylan QA + Submit]
                                                                                          ↓
                                                                                 [Deliverable Production]
                                                                                    (Claude does work)
                                                                                          ↓
                                                                                 [Dylan QA + Deliver]
                                                                                          ↓
                                                                                 [Tracking / Feedback Loop]
```

### Layer Breakdown

#### Layer 1: Gig Radar (Monitoring)
**Purpose:** Automatically discover relevant gig postings from multiple sources.

**Sources (active):**
1. Reddit (r/forhire, r/slavelabour, r/freelance_forhire, r/WorkOnline, r/HireaWriter) — public JSON endpoint, no auth required; daily cadence
2. Hacker News "Who is hiring?" — monthly thread, Algolia search API, no auth required; runs once per month via state file
3. LinkedIn job alerts — passive input, no automation

**Sources evaluated and eliminated:** Contra (design/product skew), Discord (auth required), Craigslist (RSS 403 from all endpoints), RemoteOK (90% full-time engineering roles).

**Structural note:** Inbound monitoring has a ceiling for Dylan's gig types. Data cleanup, SOPs, and spreadsheet work are posted by non-technical people who don't use developer platforms. Phase 4 outbound is needed to complement passive monitoring.

**Output:** Raw list of candidate gigs with metadata (source, title, description, budget if stated, post date, poster history).

**Tech:** Python script, scheduled via Windows Task Scheduler (local). Cloud scheduling deferred — Reddit blocks datacenter IPs.

#### Layer 2: Gig Scoring (Filtering)
**Purpose:** Use Claude API to evaluate each gig against Dylan's profile and constraints.

**Scoring prompt should evaluate:**
- Clarity of scope (1-10): Is the deliverable well-defined?
- AI-deliverability (1-10): Can Claude do 80%+ of this?
- Estimated time for Dylan (hours): Including QA and client comms
- Budget-to-effort ratio: Is this worth the time?
- Red flags: Vague scope, "test project" language, no budget mentioned, brand-new poster with no history
- Recommendation: BID / MAYBE / SKIP

**Output:** Scored and ranked shortlist pushed to Dylan via Discord.

**Critical design decision:** Over-filter aggressively early. Better to surface 2 strong matches than 10 mediocre ones. Dylan's time is the bottleneck.

#### Layer 3: Proposal Drafting
**Purpose:** Generate ready-to-send (or near-ready) proposals tailored to each gig.

**Template library (build iteratively):**
- `data-cleanup`: "I'll clean and structure your data..."
- `doc-writing`: "I'll turn your notes/requirements into a polished document..."
- `analysis`: "I'll analyze your data and deliver a clear report..."
- `policy-template`: "I'll draft a [policy/standard/procedure] document..."
- `general-short`: Catch-all for small tasks

**Each proposal must:**
- Reference specific details from the gig posting (no generic spam)
- Be concise (under 150 words for Reddit/Discord, longer for platforms)
- Include a realistic timeline
- State a clear price or ask for budget

**Output:** Draft proposal for Dylan to review/edit/send. Target: <5 min review time.

#### Layer 4: Deliverable Production
**Purpose:** Claude produces the actual work product.

**This is the existing workflow — no special tooling needed.** Dylan takes client input, passes to Claude with context, QAs the output, delivers.

**Quality gates:**
- Dylan reviews every deliverable before delivery (non-negotiable)
- For data work: spot-check formulas, row counts, edge cases
- For documents: read fully, check tone/formatting, verify requirements met
- For analysis: validate conclusions against the data

#### Layer 5: Tracking & Feedback Loop
**Purpose:** Track what's working, what's not, and feed learnings back into the system.

**Track in Airtable:**
- Gig source, type, budget, status (applied / won / lost / completed)
- Time spent (Dylan's hours only)
- Revenue
- Scoring accuracy (did the score predict win/quality?)
- Client satisfaction / repeat potential

**Monthly review:** Calculate effective hourly rate, identify best-performing gig types and sources, refine scoring prompts accordingly.

---

## 4. Tech Stack

| Component | Tool | Cost | Why |
|---|---|---|---|
| Scripting | Python 3.13 | Free | AE-relevant, good API support |
| Reddit data | `requests` + public JSON API | Free | Reddit locked down script app registration; public endpoint requires no auth |
| HN data | Algolia search API + HN Firebase API | Free | No auth required; monthly cadence; searches within HN thread by keyword |
| AI Engine | Claude API (Sonnet for scoring + proposals) | ~$5/mo | Already in ecosystem |
| Scheduling | Windows Task Scheduler (local) | Free | Reddit blocks GitHub Actions/datacenter IPs; local runner on residential IP works fine |
| CRM/Tracker | Airtable | Free tier | Visual, no-code, fast to set up; auto-logged via airtable_logger.py |
| Notifications | Discord webhook | Free | Zero-friction setup; Gmail app passwords require 2FA |
| Version Control | GitHub (private repo) | Free | Portfolio-ready, good practice |

**Explicitly not using:** Upwork (connect costs, bot competition), Fiverr (20% fee), praw (Reddit locked down API registration), GitHub Actions for scheduling (Reddit 403 block), Craigslist (RSS 403 from all IPs), RemoteOK (wrong market — full-time eng roles).

---

## 5. Tooling Context: Claude Code vs Cowork

| Activity | Tool | Why |
|---|---|---|
| Building the pipeline (Python, APIs, git) | Claude Code | Terminal-native, full dev environment, teaches AE-relevant skills |
| Iterating on scoring/proposal prompts | Claude Code or Chat | Conversational prompt engineering |
| Producing client deliverables (file-in → file-out) | Cowork | Non-technical, folder-based, fast for repetitive production tasks |
| Ad hoc analysis or tracking | Either | Depends on complexity |

**Build phase (Phases 1–3):** Complete. Claude Code remains available for Phase 4 portfolio work and pipeline maintenance.

**Operational phase (Phase 4+):** Cowork takes over deliverable production. Claude Code stays for new features and the portfolio page build.

**Key principle:** Claude Code is where the learning happens. Cowork is where the earning happens.

---

## 6. Learning Protocol

This section exists to prevent the most likely failure mode: Claude Code builds everything, Dylan learns nothing, and Bucket 2 gets zero value.

### Rules for Claude Code Sessions

> **LEARNING MODE — ACTIVE**
>
> Dylan prefers fast-forward mode: Claude builds, explains key concepts at a high level, Dylan does not need to execute every individual step unless it's genuinely non-trivial. Teaching happens through explanation and AE parallels, not hand-holding.
>
> 1. **Explain before writing.** Before producing any code, explain in plain English what you're about to build and why.
>
> 2. **Name the transferable concept.** After each micro-task, explicitly state what AE-relevant skill was just practiced.
>
> 3. **Never auto-fix silently.** If Dylan's code has an error, show the error message first and ask what he thinks it means before fixing it.
>
> 4. **Vocabulary building.** When introducing a new term, define it once in plain language and use it naturally going forward.

### TIL (Today I Learned) Log

After every Claude Code session, Dylan writes 2-3 sentences in a running log. Format:

```
## 2026-03-XX — Session N
**What I built:** [one sentence]
**What I learned:** [one concept or skill]
**What confused me:** [one thing, or "nothing" if clear]
```

This log lives in the repo at `/docs/TIL.md`.

### Progression Model

Tied to phases, not calendar weeks. Dylan moves fast — don't artificially slow down.

**Phase 1 (complete) — Collaborative:** Claude builds, explains at a high level. Dylan follows along, asks questions, understands what was built even if he didn't type it.

**Phase 2 — Supervised:** Dylan drives more decisions. Claude handles unfamiliar syntax and complex integrations. Dylan should be able to read any file in the repo and explain it.

**Phase 3+ — Independent with support:** Dylan can make small changes solo. Claude handles new features and debugging. Dylan can explain the full architecture to someone else.

### Session Handoff Protocol

**Run this at the end of every Claude Code session.**

1. **State what was completed.**
2. **State what's next** — next micro-task, one-sentence preview.
3. **Log any blockers.**
4. **Prompt the TIL entry.**
5. **Generate the Session State update** — ready-to-paste replacement for the `⚡ SESSION STATE` block.

**Dylan's job after each session:**
1. Write the TIL entry in `/docs/TIL.md`
2. Copy the generated Session State block into the top of this document
3. Save the file

---

## 7. Build Phases

### Phase 1: Reddit Scraper + Scoring Pipeline ✅ COMPLETE

**Goal:** Automatically surface scored gig recommendations from Reddit.

**Deliverables:**
- [x] Python script that polls target subreddits for new posts matching keywords
- [x] Keyword/filter config (editable without code changes)
- [x] Claude API integration for scoring each post
- [x] Output: scored digest sent via Discord webhook
- [x] Scheduled via Windows Task Scheduler (5pm daily)

**Success criteria:** Pipeline runs reliably. At least 1 gig surfaces that Dylan would actually bid on. ✅

#### Phase 1 Micro-Tasks

- [x] **1.1** — Project setup and environment
- [x] **1.2** — Reddit data access *(Note: Reddit locked down script app registration. Used public JSON endpoint `reddit.com/r/sub/new.json` via `requests` — no auth required. praw not used.)*
- [x] **1.3** — Fetch posts from one subreddit
- [x] **1.4** — Parse and filter posts
- [x] **1.5** — Multi-subreddit support + config file *(Note: r/dataengineering and r/analytics removed — discussion communities, not job boards; [Hiring] tag filter screens out almost everything)*
- [x] **1.6** — Deduplication and state
- [x] **1.7** — Claude API integration for scoring
- [x] **1.8** — Scoring prompt development
- [x] **1.9** — Output formatting + Discord notification *(Note: Email dropped due to Gmail 2FA friction. Discord webhook used instead.)*
- [x] **1.10** — Scheduling *(Note: GitHub Actions blocked by Reddit 403 on datacenter IPs. Replaced with Windows Task Scheduler at 5pm daily.)*
- [x] **1.11** — README and documentation

---

### Phase 2: Proposal System + Airtable ✅ COMPLETE

**Goal:** End-to-end flow from scored gig → draft proposal → tracking.

**Deliverables:**
- [x] Proposal template library (3-4 templates)
- [x] Claude API integration for proposal customization
- [x] Airtable base with gig tracking schema
- [x] Discord notification includes draft proposal alongside scored gig
- [x] Simple "log this gig" workflow (airtable_logger.py auto-logs BID+MAYBE posts)

**Success criteria:** Pipeline built and functional — per-gig time target achievable. First proposal submission is now the Phase 4 operational target.

---

### Phase 3: Expand Sources + Refine ✅ COMPLETE

**Goal:** Add non-Reddit sources and tune the system based on real data.

**Deliverables:**
- [x] At least 1 additional source integrated — HN "Who is hiring?" added (monthly, Algolia); Reddit expanded to 5 subreddits
- [x] Scoring keywords tightened — false positives ("report", "analysis") replaced with compound terms; "sop", "data quality", "process documentation" added
- [ ] Template library expanded based on actual gig types — deferred: no real gigs yet to base this on
- [ ] First monthly review — deferred: pipeline needs a full month of live runs first

**Success criteria:** Two sources operational. Keywords tightened — measurably fewer false positives. Structural ceiling identified: inbound alone won't meet Bucket 1 target. Phase 4 outbound warranted.

---

### Phase 4: Outbound + First Revenue

**Goal:** Complement inbound monitoring with proactive outreach. Generate the first actual client engagement and first dollar of revenue.

**Context:** Phase 3 confirmed that inbound monitoring alone hits a structural ceiling. Dylan's best gig types (data cleanup, SOPs, spreadsheet work) are posted by non-technical people who don't use developer platforms. Outbound flips the model: instead of waiting for gigs to appear, Dylan proactively shows up where clients look.

**Deliverables:**
- [ ] GitHub Pages portfolio page — simple 1-pager: who Dylan is, what he does, sample work types, contact/Reddit link
- [ ] [For Hire] post template for relevant subreddits (r/forhire, r/slavelabour, r/freelance_forhire)
- [ ] First proposal submitted and logged in Airtable
- [ ] First monthly pipeline review: source performance, scoring accuracy, time spent

**Success criteria:** At least 1 proposal submitted. At least 1 reply or inquiry from any outbound channel.

**Possible later additions (evaluate after first month of outbound):**
- Auto-response templates for common client follow-up questions
- Client relationship tracking (repeat clients flagged in Airtable)
- Rate optimization based on win/loss data
- Cloud scheduling revisit if a Reddit-unblocked data source is added

---

## 8. Gig Type Fit Matrix

### Good Fits (high AI-leverage, clear scope)
- Spreadsheet/CSV cleanup and formatting
- Data entry and structuring
- Document drafting from notes or outlines
- Policy/procedure template creation
- Data analysis with written summary
- Report generation from raw data

### Acceptable Fits (moderate AI-leverage, some judgment needed)
- Requirements documentation
- Process documentation
- Presentation creation from content
- Translation-adjacent work (formatting, not creative JP↔EN)

### Bad Fits (avoid — time sinks)
- Anything requiring live calls or meetings
- Ongoing virtual assistant roles (scope creep)
- Creative/subjective work (marketing copy, branding)
- Anything requiring access to client systems/credentials
- Ambiguously scoped projects with no clear deliverable

---

## 9. Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-10 | Skip Upwork | Bot competition, connect costs, race-to-the-bottom in our gig types. |
| 2026-03-10 | Start with Reddit as primary source | Free, low friction, direct client contact, no platform fees |
| 2026-03-10 | Airtable over Notion for CRM | More structured, better for tracking metrics, free tier sufficient |
| 2026-03-10 | 2-3 hrs/week hard cap until proven | Protect against sunk cost. Scale only with evidence of ROI. |
| 2026-03-11 | Claude Code for building, Cowork for operating | Claude Code teaches AE-relevant skills. Cowork handles deliverable production once pipeline is live. |
| 2026-03-11 | Session State + Handoff Protocol | Enables "pick up where we left off" across sessions. |
| 2026-03-11 | Use requests + public Reddit JSON instead of praw | Reddit locked down script app registration; public JSON endpoint works without auth and is simpler |
| 2026-03-11 | Discord webhook for notifications instead of email | Gmail app passwords require 2FA Dylan didn't want to set up; Discord webhook is zero-friction |
| 2026-03-11 | Windows Task Scheduler instead of GitHub Actions | Reddit blocks requests from datacenter IPs (403); local runner on residential IP works fine |
| 2026-03-11 | Run pipeline once daily at 5pm instead of 2x/day | Token efficiency; Dylan's schedule means 5pm is the only actionable time anyway |
| 2026-03-11 | Compress timeline from weeks to days | Dylan motivated to move fast; Phase 1 completed in one session with no quality loss |
| 2026-03-11 | Remove r/dataengineering and r/analytics from config | Discussion communities, not job boards; [Hiring] tag filter screens out nearly everything there |
| 2026-03-12 | Add HN as second source (monthly, "Who is hiring?" thread) | Free, no auth, Algolia search API. Require_terms filter keeps only contract/freelance posts to avoid full-time job noise. |
| 2026-03-12 | Eliminate Craigslist | RSS returns 403 from all endpoints including residential IP. Dead end. |
| 2026-03-12 | Eliminate RemoteOK | Free API but 90% full-time engineering roles. Wrong market for Dylan's gig types. |
| 2026-03-12 | Expand Reddit to 5 subreddits | Added r/freelance_forhire, r/WorkOnline, r/HireaWriter. tag_exempt_subreddits config bypasses [Hiring] tag check for subs that don't use it. |
| 2026-03-12 | Tighten keywords — remove "report" and "analysis" | Too broad — catching journalism and research writing posts. Replaced with "data report", "data analysis". Added "sop", "standard operating procedure", "data quality", "process documentation". |
| 2026-03-12 | Acknowledge inbound ceiling; pivot to Phase 4 outbound | High AI-deliverability gigs are posted on non-developer platforms. Passive monitoring alone won't fund the tools — outbound needed. |

---

## 10. Guiding Principles

1. **Dylan's time is the scarcest resource.** Every design decision should minimize Dylan's hours per dollar earned.

2. **Working > perfect.** Ship the ugly MVP. Refine based on real data, not hypothetical optimization.

3. **Over-filter, under-commit.** Better to bid on 1 great gig than 5 mediocre ones. Quality of match > quantity of proposals.

4. **Every piece builds the portfolio.** The pipeline itself, the scripts, the process — all of this is demonstrable AE-relevant work. Treat the repo accordingly.

5. **Fail fast, learn cheap.** If after Phase 3 there are zero wins, diagnose honestly and pivot or kill. Don't zombie. *Applied at end of Phase 3: inbound ceiling diagnosed, Phase 4 pivot to outbound chosen over killing the project.*

6. **Automate the boring, keep the judgment.** Claude handles production. Dylan handles decisions. Never let AI auto-submit anything without human review.

7. **Revenue is the metric that matters for Bucket 1.** Not proposal count, not pipeline volume, not tech sophistication. Dollars in minus costs out.

8. **If Dylan can't explain it, it doesn't count.** Code that works but isn't understood is technical debt and a missed learning opportunity.

---

## 11. How to Use This Document

### Starting a Claude Code session ("Pick up where we left off")

1. Open Claude Code
2. Say: **"Pick up where we left off"**
3. Claude reads the `⚡ SESSION STATE` block at the top and resumes at the current micro-task

### After every Claude Code session

1. Write TIL entry in `/docs/TIL.md`
2. Copy the generated Session State block into the top of this document
3. Check off completed micro-tasks in Section 7
4. Save the file

---

## 12. Open Questions (Resolve As You Go)

- [x] Reddit API: Which auth method? → Resolved: no auth, public JSON endpoint
- [x] Notifications: Slack or email? → Resolved: Discord webhook
- [x] Additional sources beyond Reddit? → Resolved: HN added (monthly). Craigslist (403), RemoteOK (wrong market), Contra (design/product skew), Discord (auth required) all evaluated and eliminated.
- [ ] Scoring prompt: token cost at scale? Monitor after first 30 days of real runs.
- [ ] Pricing strategy: Undercut market to win first gigs, or price fair from day one?
- [ ] Legal: Do we need a simple freelance contract template? Payment terms?
- [ ] Tax implications: At what income level does this need formal tracking? (Consult accountant, not Claude.)
