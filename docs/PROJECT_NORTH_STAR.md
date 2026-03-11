# Project North Star: AI-Assisted Freelance Pipeline

## Last Updated: March 11, 2026

---

## ⚡ SESSION STATE — READ THIS FIRST

> **Claude: When Dylan says "pick up where we left off," read this block and resume accordingly.**

**Current Phase:** 1 — Reddit Scraper + Scoring Pipeline
**Current Micro-Task:** 1.1 — Project setup and environment
**Session Count:** 0
**Progression Level:** Guided (explain everything, heavy checkpoints)
**Last Session Date:** N/A
**Last Session Summary:** N/A
**Blockers / Open Issues:** None yet
**Next Action:** Start micro-task 1.1 — create GitHub repo and Python project structure

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
**Status:** Pre-build / Planning

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

**Sources (prioritized):**
1. Reddit (r/forhire, r/slavelabour, r/dataengineering, r/analytics) — Reddit API, free
2. Contra — job feed (API/RSS if available, light scraping as fallback)
3. Discord servers (data/analytics communities) — via webhooks
4. LinkedIn job alerts — passive input, no automation needed

**Output:** Raw list of candidate gigs with metadata (source, title, description, budget if stated, post date, poster history).

**Tech:** Python script, scheduled via GitHub Actions (free tier) or cron on cheap VPS.

#### Layer 2: Gig Scoring (Filtering)
**Purpose:** Use Claude API to evaluate each gig against Dylan's profile and constraints.

**Scoring prompt should evaluate:**
- Clarity of scope (1-10): Is the deliverable well-defined?
- AI-deliverability (1-10): Can Claude do 80%+ of this?
- Estimated time for Dylan (hours): Including QA and client comms
- Budget-to-effort ratio: Is this worth the time?
- Red flags: Vague scope, "test project" language, no budget mentioned, brand-new poster with no history
- Recommendation: BID / MAYBE / SKIP

**Output:** Scored and ranked shortlist pushed to Dylan.

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
| Scripting | Python 3.x | Free | AE-relevant, good API support |
| AI Engine | Claude API (Sonnet for scoring, Opus for complex work) | ~$5/mo | Already in ecosystem |
| Scheduling | GitHub Actions | Free tier | No infra to manage |
| CRM/Tracker | Airtable | Free tier | Visual, no-code, fast to set up |
| Notifications | Slack webhook or email (SMTP) | Free | Dylan's preference |
| Version Control | GitHub (private repo) | Free | Portfolio-ready, good practice |

**Explicitly not using:** Upwork (connect costs, bot competition, race-to-the-bottom for our gig types), Fiverr (20% fee, not worth it at our volume).

---

## 5. Tooling Context: Claude Code vs Cowork

| Activity | Tool | Why |
|---|---|---|
| Building the pipeline (Python, APIs, git) | Claude Code | Terminal-native, full dev environment, teaches AE-relevant skills |
| Iterating on scoring/proposal prompts | Claude Code or Chat | Conversational prompt engineering |
| Producing client deliverables (file-in → file-out) | Cowork | Non-technical, folder-based, fast for repetitive production tasks |
| Ad hoc analysis or tracking | Either | Depends on complexity |

**Build phase (Weeks 1-6):** Claude Code is primary. Dylan is learning to code, not outsourcing code.

**Operational phase (Week 7+):** Cowork takes over deliverable production. Claude Code stays for pipeline maintenance and new features.

**Key principle:** Claude Code is where the learning happens. Cowork is where the earning happens. Don't skip to Cowork early — the discomfort of the terminal is the point.

---

## 6. Learning Protocol

This section exists to prevent the most likely failure mode: Claude Code builds everything, Dylan learns nothing, and Bucket 2 gets zero value.

### Rules for Claude Code Sessions

**Paste this into Claude Code's project instructions or system prompt:**

> **LEARNING MODE — ACTIVE**
>
> Dylan is building this project to learn, not just to ship. Follow these rules:
>
> 1. **Explain before writing.** Before producing any code, explain in plain English what you're about to build and why. Use analogies to data governance concepts where helpful (e.g., "this config file is like a data dictionary for the scraper").
>
> 2. **Chunk the work.** Never write more than 30 lines of code in a single block. After each chunk, pause and explain what it does line by line. Ask Dylan if he has questions before continuing.
>
> 3. **Dylan types first (when feasible).** For simple logic (loops, conditionals, variable assignment), describe what to write and let Dylan attempt it. Correct after, not before. This does NOT apply to boilerplate, config files, or complex library-specific syntax — just write those.
>
> 4. **Name the transferable concept.** After each micro-task, explicitly state what AE-relevant skill was just practiced. Examples: "You just parsed JSON — this is the same thing you'll do when working with API responses in dbt or Airflow." / "This config file pattern is how dbt projects manage environment variables."
>
> 5. **Comprehension checkpoints.** At the end of each session (or every ~45 min), ask Dylan to explain what was built in his own words. If he can't, the session moved too fast.
>
> 6. **Never auto-fix silently.** If Dylan's code has an error, show the error message first and ask him what he thinks it means before fixing it. Reading error messages is a core skill.
>
> 7. **Vocabulary building.** When introducing a new term (API, endpoint, JSON, virtual environment, dependency, etc.), define it once in plain language and then use it naturally going forward. Don't re-explain every time, but don't assume prior knowledge either.

### TIL (Today I Learned) Log

After every Claude Code session, Dylan writes 2-3 sentences in a running log. Format:

```
## 2026-03-XX — Session N
**What I built:** [one sentence]
**What I learned:** [one concept or skill]
**What confused me:** [one thing, or "nothing" if clear]
```

This log lives in the repo at `/docs/TIL.md`. It serves three purposes:
1. Forces synthesis (you don't understand it until you can write it down)
2. Provides a reference when you forget something three sessions later
3. Becomes portfolio material ("here's my learning journal from building an end-to-end data pipeline")

### Progression Model

Dylan's comfort level will evolve. The learning protocol should evolve with it:

**Weeks 1-2 (Guided):** Claude Code explains everything. Dylan types simple code, Claude Code handles complex parts. Heavy use of analogies and checkpoints.

**Weeks 3-4 (Collaborative):** Dylan writes more code independently. Claude Code reviews and suggests improvements. Explanations shift from "what is this" to "why this approach vs alternatives."

**Weeks 5-6 (Supervised):** Dylan drives. Claude Code is consulted for unfamiliar territory. Dylan should be able to read and roughly understand any file in the repo without help.

**Week 7+ (Independent with support):** Dylan can make small changes to the pipeline solo. Claude Code handles new features and debugging complex issues. Dylan can explain the full architecture to someone else.

### Session Handoff Protocol

**Run this at the end of every Claude Code session.** This is what makes "pick up where we left off" work.

**Claude Code: At the end of each session, do the following:**

1. **State what was completed.** List the micro-task(s) finished this session.

2. **State what's next.** Identify the next micro-task and give a one-sentence preview.

3. **Log any blockers.** If something didn't work, was confusing, or needs Dylan to do something outside of Claude Code (e.g., sign up for an API, install something), note it clearly.

4. **Prompt the TIL entry.** Ask Dylan: "What did you learn this session? Write your TIL entry now while it's fresh."

5. **Generate the Session State update.** Print a ready-to-paste replacement for the `⚡ SESSION STATE` block at the top of this document. Format:

```
**Current Phase:** [phase number and name]
**Current Micro-Task:** [next incomplete micro-task ID and name]
**Session Count:** [previous count + 1]
**Progression Level:** [Guided / Collaborative / Supervised / Independent]
**Last Session Date:** [today's date]
**Last Session Summary:** [1-2 sentences on what was done]
**Blockers / Open Issues:** [list or "None"]
**Next Action:** [specific first step for next session]
```

**Dylan's job after each session:**
1. Write the TIL entry in `/docs/TIL.md`
2. Copy the generated Session State block into the top of this document
3. Save the updated document

**This takes 3 minutes and is non-negotiable.** It's the only thing that makes multi-session continuity work. Skip it and you'll spend 15 minutes re-orienting next time instead.

---

## 7. Build Phases

### Phase 1: Reddit Scraper + Scoring Pipeline (Weeks 1-2)

**Goal:** Automatically surface scored gig recommendations from Reddit.

**Deliverables:**
- [ ] Python script that polls target subreddits for new posts matching keywords
- [ ] Keyword/filter config (editable without code changes)
- [ ] Claude API integration for scoring each post
- [ ] Output: scored list sent via email or Slack
- [ ] GitHub Actions workflow running on schedule (2x daily minimum)

**Keyword seeds:** data cleanup, spreadsheet, CSV, data entry, documentation, policy, report, analysis, Excel, Google Sheets, data migration, data formatting

**Success criteria:** Pipeline runs reliably for 7 days. At least 1 gig surfaces that Dylan would actually bid on.

**Known risks:**
- Reddit API rate limits / auth changes
- Low volume on target subreddits (may need to cast wider net)
- Scoring prompt may need 2-3 iterations before useful

#### Phase 1 Micro-Tasks

Work through these in order. Each is a single Claude Code session (20-45 min). Do not skip ahead.

**1.1 — Project setup and environment**
- Create a GitHub repo (gigflow)
- Set up a Python virtual environment
- Create requirements.txt
- Create a basic folder structure (src/, config/, docs/, tests/)
- Create docs/TIL.md with the first entry
- **Concepts learned:** Repos, virtual environments, dependency management, project structure
- **AE parallel:** This is how dbt projects, Airflow DAGs, and analytics repos are organized

**1.2 — Reddit API authentication**
- Register a Reddit "script" app at reddit.com/prefs/apps
- Store credentials in a .env file (learn: why credentials don't go in code)
- Write a script that authenticates and prints "connected successfully"
- Add .env to .gitignore (learn: why this matters)
- **Concepts learned:** API authentication, environment variables, secrets management
- **AE parallel:** Every data pipeline authenticates against source systems the same way

**1.3 — Fetch posts from one subreddit**
- Write a function that fetches the 25 newest posts from r/forhire
- Print each post's title, author, URL, and timestamp
- **Concepts learned:** HTTP requests, JSON parsing, API response structure
- **AE parallel:** This is an extract step — pulling raw data from a source

**1.4 — Parse and filter posts**
- Add keyword filtering (match against title + body text)
- Filter out posts older than 24 hours
- Filter to only [Hiring] tagged posts (not [For Hire])
- Print filtered results in a readable format
- **Concepts learned:** String matching, date handling, control flow, list filtering
- **AE parallel:** This is a transform step — cleaning and filtering raw data

**1.5 — Multi-subreddit support + config file**
- Move subreddit list and keywords into a config.yaml file
- Update script to read config and loop through multiple subreddits
- Add r/slavelabour, r/dataengineering, r/analytics
- **Concepts learned:** Config-driven design, YAML, separation of code and config
- **AE parallel:** dbt uses YAML configs for models, sources, and tests — same pattern

**1.6 — Deduplication and state**
- Save seen post IDs to a local JSON file
- On each run, skip posts already seen
- **Concepts learned:** File I/O, state management, idempotency
- **AE parallel:** Incremental loads in data pipelines use the same "only process new records" pattern

**1.7 — Claude API integration for scoring**
- Get an Anthropic API key
- Write a function that sends a post's title + body to Claude with the scoring prompt
- Parse Claude's response into structured scores
- Print scored results
- **Concepts learned:** API integration (different API, same pattern), prompt engineering, structured output parsing
- **AE parallel:** Calling external APIs for enrichment is common in modern data stacks

**1.8 — Scoring prompt development**
- Write v1 of the scoring prompt (use the criteria from Section 3, Layer 2)
- Test it against 5-10 real posts manually
- Iterate the prompt based on results (at least 2 revisions)
- Save the final prompt in config/ as a text file
- **Concepts learned:** Prompt engineering, evaluation, iterative improvement
- **AE parallel:** This is testing and validation — does the transformation produce correct output?

**1.9 — Output formatting + notification**
- Format scored results into a readable digest (markdown or plain text)
- Send via email (SMTP) or Slack webhook (Dylan's choice)
- Include: post title, score breakdown, recommendation, direct link
- **Concepts learned:** String formatting, email/webhook APIs, notification systems
- **AE parallel:** This is the load/serve step — delivering processed data to a consumer

**1.10 — GitHub Actions scheduling**
- Create a GitHub Actions workflow YAML file
- Configure it to run the script 2x daily
- Store API keys as GitHub secrets
- Verify it runs successfully via Actions logs
- **Concepts learned:** CI/CD basics, scheduled jobs, cloud execution, secrets in CI
- **AE parallel:** This is orchestration — the same role Airflow/Dagster/Prefect plays in data pipelines

**1.11 — End-of-phase review**
- Read through the entire codebase and add comments explaining each section
- Update docs/TIL.md with a phase summary
- Write a README.md explaining what the project does, how to set it up, and how to run it
- **Concepts learned:** Documentation, code readability, README writing
- **AE parallel:** Every good analytics project has a README. This is portfolio-ready.

#### Phase 1 Checkpoint

Before moving to Phase 2, Dylan should be able to answer these without looking at the code:
1. What does a virtual environment do and why do we use one?
2. How does the script authenticate with Reddit?
3. What format does the Reddit API return data in?
4. Why do we store credentials in .env instead of the code?
5. What happens if we don't deduplicate posts between runs?
6. How does the scoring prompt decide which gigs to recommend?
7. What does the GitHub Actions YAML file do?

If any answer is "I don't know," revisit that micro-task before proceeding.

### Phase 2: Proposal System + Airtable + Notifications (Weeks 3-4)

**Goal:** End-to-end flow from scored gig → draft proposal → tracking.

**Deliverables:**
- [ ] Proposal template library (3-4 templates)
- [ ] Claude API integration for proposal customization
- [ ] Airtable base with gig tracking schema
- [ ] Slack/email notification with scored gigs + draft proposals
- [ ] Simple "approve and log" workflow

**Success criteria:** Dylan's per-gig time from discovery to proposal submission is under 10 minutes. At least 1 proposal actually submitted.

### Phase 3: Expand Sources + Refine (Weeks 5-6)

**Goal:** Add non-Reddit sources and tune the system based on real data.

**Deliverables:**
- [ ] At least 1 additional source integrated (Contra, Discord, or other)
- [ ] Scoring prompt refined based on Phase 1-2 data (what scored high but was actually bad? what scored low but would have been good?)
- [ ] Template library expanded based on actual gig types encountered
- [ ] First monthly review completed

**Success criteria:** System surfaces viable gigs from 2+ sources. Scoring accuracy improves measurably.

### Phase 4+: Ongoing Iteration

**Goal:** Optimize for revenue and reduce Dylan's time per dollar.

**Possible additions (evaluate based on data, don't pre-build):**
- Auto-response for common follow-up questions
- Client relationship tracking (repeat clients get flagged)
- Portfolio page (simple GitHub Pages site showcasing work types)
- Rate optimization (A/B test pricing on similar gigs)
- Contra or other platform API integration if volume justifies

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

Track major decisions and their rationale so future sessions don't relitigate.

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-10 | Skip Upwork | Bot competition, connect costs, race-to-the-bottom in our gig types. Research confirmed complaints are well-founded in 2026. |
| 2026-03-10 | Start with Reddit as primary source | Free API, low friction, direct client contact, no platform fees |
| 2026-03-10 | Airtable over Notion for CRM | More structured, better for tracking metrics, free tier sufficient |
| 2026-03-10 | 2-3 hrs/week hard cap until proven | Protect against sunk cost. Scale only with evidence of ROI. |
| 2026-03-11 | Claude Code for building, Cowork for operating | Claude Code teaches AE-relevant terminal/coding skills (Bucket 2). Cowork handles file-in/file-out deliverable production once pipeline is live. |
| 2026-03-11 | Learning Protocol added | Prevents "Claude builds everything, Dylan learns nothing" failure mode. Micro-tasks, comprehension checkpoints, TIL log. |
| 2026-03-11 | Session State + Handoff Protocol | Enables "pick up where we left off" across sessions. Session State block at top of doc, handoff runs at end of every session, 3-min update ritual. |

---

## 10. Guiding Principles

1. **Dylan's time is the scarcest resource.** Every design decision should minimize Dylan's hours per dollar earned.

2. **Working > perfect.** Ship the ugly MVP. Refine based on real data, not hypothetical optimization.

3. **Over-filter, under-commit.** Better to bid on 1 great gig than 5 mediocre ones. Quality of match > quantity of proposals.

4. **Every piece builds the portfolio.** The pipeline itself, the scripts, the process — all of this is demonstrable AE-relevant work. Treat the repo accordingly (clean code, READMEs, documentation).

5. **Fail fast, learn cheap.** If after 6 weeks there are zero wins, diagnose honestly: wrong gig types? Wrong sources? Wrong pricing? Pivot or kill, don't zombie.

6. **Automate the boring, keep the judgment.** Claude handles production. Dylan handles decisions. Never let AI auto-submit anything without human review.

7. **Revenue is the metric that matters for Bucket 1.** Not proposal count, not pipeline volume, not tech sophistication. Dollars in minus costs out.

8. **If Dylan can't explain it, it doesn't count.** Code that works but isn't understood is technical debt and a missed learning opportunity. Slow down before moving on.

---

## 11. How to Use This Document

### Starting a Claude Code session ("Pick up where we left off")

1. Open Claude Code
2. Paste this entire document as context (or keep it in project instructions)
3. Say: **"Pick up where we left off"**
4. Claude Code reads the `⚡ SESSION STATE` block at the top and resumes at the current micro-task

That's it. The Session State block tells Claude Code everything it needs.

### Starting a Claude Chat session (planning, strategy, decisions)

1. Paste this document as context
2. State what you want to discuss (e.g., "I want to reconsider the notification approach" or "Help me refine the scoring prompt")
3. After the conversation, update the Decision Log if any decisions were made

### After every Claude Code session

1. Write TIL entry in `/docs/TIL.md` (Claude Code will prompt you)
2. Copy the generated Session State block into the top of this document
3. Check off completed micro-tasks in Section 7
4. Save the file

**This 3-minute ritual is the glue that holds multi-session projects together. Do not skip it.**

### After major decisions or phase completions

1. Update the Decision Log (Section 9)
2. Update phase checklists (Section 7)
3. Note any changes to architecture or strategy

### If the project drifts

Re-read Section 10 (Guiding Principles). If current work doesn't serve Principle 1 or Principle 7, stop and reassess.

---

## 12. Open Questions (Resolve As You Go)

- [ ] Reddit API: Which auth method? Personal script app or OAuth? Rate limits for our polling frequency?
- [ ] Scoring prompt: How many tokens per gig evaluation? Cost implications at scale?
- [ ] Notifications: Slack (faster feedback loop) or email (less tooling)?
- [ ] Pricing strategy: Undercut market to win first gigs, or price fair from day one?
- [ ] Legal: Do we need a simple freelance contract template? Payment terms?
- [ ] Tax implications: At what income level does this need formal tracking? (Consult accountant, not Claude.)
