# Trading Squad Improvement Plan (Unified)

Last updated: 2025-09-04 14:21 (local)
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
- [ ] Report key normalization for streamed sections
  - In `app/trading_agents_streamlit.py`, normalize any `*_debate_state` keys to current sections so tabs always populate
- [ ] Validate after each change (see Section 6)

### 3.2 Medium Priority (Observability & Accessibility)
- [ ] Tool Calls panel in the UI
  - Collapsible panel rendering `st.session_state.tool_calls` (time, agent, tool, summary)
- [ ] Optional tool-call hooks (debug-mode only)
  - Emit start/end/error with durations from `tradingagents/*` and pipe to the UI
- [ ] Accessibility polish
  - Add ARIA labels and ensure high-contrast for agent status buttons in `render_agent_button()`

### 3.3 UI Optimization Plan (Integrated Excerpts)

Reference: `docs/UI_optimization_plan.md`

- [x] Phase 1.1–1.3: API key validation + loading states (already done; keep parity)
- [x] Phase 2.1–2.2: CSS foundation & optimization (noted as completed in plan)
- [ ] Phase 2.3: Sidebar configuration streamlining (grouping, progressive disclosure)
- [ ] Phase 3.1: Agent detail modal optimization (performance, state mgmt)
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

## 8) Links

- Parity Spec: `agents/trading-squad/docs/streamlit-ui-spec.md`
- UI Optimization Plan: `agents/trading-squad/docs/UI_optimization_plan.md`
- Main UI: `agents/trading-squad/app/trading_agents_streamlit.py`
- Sidebar: `agents/trading-squad/app/components/sidebar_config.py`
- CLI references: `agents/trading-squad/cli/`
