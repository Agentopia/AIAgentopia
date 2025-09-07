# Trading Squad Improvement Plan (Unified)

Last updated: 2025-09-05 21:20 (local)
Owner: Trading Squad
Repo path: `agents/trading-squad/`

## 1) Purpose

Unify CLI parity/polish tasks and the UI Optimization Plan into a single, incremental, test-driven checklist. We will ship one small change per PR, validate, and then proceed to the next item.

## 2) Working Rules

- One small change per PR.
- Keep UI fully functional at all times.
- Run the smoke test (Section 6) before and after each change.
- Update this file’s checkboxes and notes after each merge.

## 3) Task Checklist (Actionable)

Legend: [ ] not started, [~] in progress, [x] done

### 3.1 High Priority (Parity/Correctness)
- [x] Provider/model/depth parity with CLI
  - Dynamic Ollama model discovery via `/api/tags` in `app/components/sidebar_config.py`
  - OpenAI deep-thinking toggle filters to o1 family when enabled
  - Options and defaults aligned for major providers; depth mapping parity preserved
- [x] Report key normalization for streamed sections
  - In `app/trading_agents_streamlit.py`, normalize any `*_debate_state` keys to current sections so tabs always populate
- [x] Validate after each change (see Section 6)

### 3.2 Medium Priority (Observability & Accessibility)
- [x] Tool Calls panel in the UI (minimal, debug-only)
  - Implemented as a non-invasive, bottom-of-sidebar expander titled "Tool Calls (Debug)"
  - Shows lifecycle-only entries when Debug Mode is ON: `RunInitiated`, `AnalysisStart`, `AnalysisComplete`/`AnalysisFailed`
  - No main-area panels; nothing duplicates the Live Analysis Feed
- [x] Optional tool-call hooks (decision: de-scoped)
  - Deep per-tool instrumentation (durations, arguments, etc.) was evaluated and intentionally deferred
  - Rationale: Limited end-user value vs. complexity; avoids UI noise and maintenance overhead
- [x] Accessibility polish
  - Added descriptive `help` strings in `render_agent_button()` for SR users
  - High-contrast, keyboard-visible focus rings for primary/secondary buttons
  - Reduced visual weight of non-running (secondary) buttons; smaller font and tighter padding
  - Increased team expander title size/weight for clear hierarchy
  - Pending state now shows "- Waiting" on sub-agent buttons

### 3.3 UI Optimization Plan (Integrated Excerpts)

Reference: `docs/UI_optimization_plan.md`

- [x] Phase 1.1–1.3: API key validation + loading states (already done; keep parity)
- [x] Phase 2.1–2.2: CSS foundation & optimization (noted as completed in plan)
- [ ] Phase 2.3: Sidebar configuration streamlining (grouping, progressive disclosure) — de-scoped (very low priority); skipped for now
- [x] Phase 3.1: Agent detail modal optimization — deemed unnecessary; closed without changes
- [ ] Phase 3.2: Real-time data optimization (retention, memory monitoring)
- [ ] Phase 3.3: Results visualization enhancements (charts, dashboards)
- [ ] Phase 7: Utility function extraction (validation/session/streaming helpers)

Note: We will only take items from the optimization plan that do not risk breaking working parity. Priority is correctness, parity, and reliability.

## 4) Branching & PR Conventions

- Branch per task: `feat/trading-squad-<short-task-name>` or `chore/trading-squad-<short-task-name>`
- Small PR with:
  - Summary: what changed and why
  - Validation checklist results (Section 6)
  - Screenshots (when UI-visible)

## 5) Definition of Done (per task)

- Code change is minimal and focused
- Smoke test passes in Debug OFF and Debug ON
- Export buttons work (Markdown, JSONL, Quick Summary)
- No regressions in agent statuses or streaming updates
- This plan’s checkbox updated; brief note added to Section 7

## 6) Smoke Test (Run Each Time)

- Start app: `streamlit run agents/trading-squad/app/trading_agents_streamlit.py`
- Config: Provider OpenAI or Ollama; analysts default all; yesterday’s date; NVDA
- Ollama models: When Provider = Ollama and `Backend URL / Host` is set, verify model dropdowns reflect `/api/tags` results
- Preflight: After ticker confirmation, preflight card disappears immediately and no stale Overview persists
- Debug OFF: Run completes; final report renders; statuses reasonable
- Debug ON: Live messages stream; agent statuses transition; sections update incrementally
- Export: Download Full Report (md), Execution Log (jsonl); toggle Quick Summary works
- Visuals: Buttons styled; no broken animations or layout glitches

## 7) Progress Log (Notes)

- 2025-09-04 14:21: UI parity updates
  - Dynamic Ollama model discovery added to sidebar
  - Preflight confirmation card now disappears immediately upon confirmation; state reset prevents stale sections
  - Run configuration summary visible at run start and logged to Live Analysis Feed
  - Company identity validation and per-section header correction implemented for streamed reports

- 2025-09-05 16:58: Normalization + minor UI polish (merged to main)
  - Implemented `normalize_final_state_keys()` in `app/components/report_components.py` and invoked post `final_state = results.get("result", {})` to ensure consistent tab population even when backend keys vary (e.g., `research_debate_state` → `investment_debate_state`, `investment_plan` → `trader_investment_plan`, `portfolio_decision` → `final_trade_decision`).
  - Fixed duplicate heading in Portfolio Manager tab by removing the inner H4; kept single subheader.
  - Applied conservative top-spacing tweak for the blue header (reduced top gap without affecting toolbar): `.main-header { margin-top: -0.25rem }`, `.main .block-container { padding-top: 0.5rem !important }`.
  - PR #21: "feat(trading-squad): normalize report keys and minor UI polish" merged to `main` via squash.

- 2025-09-05 21:20: Tool Calls finalized (minimal, debug-only)
  - Moved Tool Calls to sidebar only; removed main-area expanders
  - Simplified to lifecycle-only logs to avoid duplication with Live Analysis Feed
  - Removed noisy mirrors, Finnhub and chunk-level logs; reduced maintenance surface
  - Decision: deeper instrumentation de-scoped; feature closed as "minimal and non-invasive"

- 2025-09-06 10:13: Accessibility + progress note (merged to feature branch)
  - Accessibility polish complete: descriptive tooltips for status buttons; high-contrast focus states; subdued secondary buttons; increased expander header size; pending shows "- Waiting"
  - Added dynamic analysts completion note next to "Analysis in Progress" header that updates live (e.g., `2/12 analysts completed`)

- 2025-09-06 10:48: Phase 2.3 de-scoped (very low priority)
  - Sidebar configuration streamlining deemed cosmetic; no functional gaps. Item marked as skipped for now to avoid unnecessary churn.

- 2025-09-06 18:04: Phase 3.1 closed (not needed)
  - Agent detail modal/panel optimization evaluated; determined to add complexity without meaningful user value given Live Analysis Feed and final report. Feature considered and closed with no code changes. Main kept stable; experimental branch reverted.

## 8) Links

- Parity Spec: `agents/trading-squad/docs/streamlit-ui-spec.md`
- UI Optimization Plan: `agents/trading-squad/docs/UI_optimization_plan.md`
- Main UI: `agents/trading-squad/app/trading_agents_streamlit.py`
- Sidebar: `agents/trading-squad/app/components/sidebar_config.py`
- CLI references: `agents/trading-squad/cli/`
