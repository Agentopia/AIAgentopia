# Trading Team Profile

## 1. Team Structure & Execution Model

### 1.1 Team Composition

#### 📈 Analyst Team (Sequential Execution)
1. **Market Analyst**
   - **Input**: Stock symbol, analysis date
   - **Output**: Technical analysis report
   - **Key Data**: Price history, moving averages, support/resistance levels

2. **Social Analyst**
   - **Input**: Stock symbol, analysis date
   - **Output**: Sentiment analysis from social media
   - **Key Data**: Social sentiment, trending topics

3. **News Analyst**
   - **Input**: Stock symbol, analysis date
   - **Output**: News article analysis
   - **Key Data**: News sentiment, major announcements

4. **Fundamentals Analyst**
   - **Input**: Stock symbol, analysis date
   - **Output**: Fundamental analysis
   - **Key Data**: Financial statements, valuation ratios

#### 🔍 Research Team (Debate → Judge)
1. **Bull Researcher**
   - **Input**: Analyst team reports (market, social, news, fundamentals)
   - **Output**: Bullish analysis appended to `investment_debate_state.bull_history`
   - **Focus**: Positive indicators and upside potential

2. **Bear Researcher**
   - **Input**: Analyst team reports
   - **Output**: Bearish analysis appended to `investment_debate_state.bear_history`
   - **Focus**: Risks and downside potential

3. **Research Manager (Judge)**
   - **Input**: Bull and Bear debate histories
   - **Output**: `investment_debate_state.judge_decision`
   - **Focus**: Synthesize debate into a research conclusion


#### 💰 Trading Team (Single Agent)
- **Trader**
  - **Input**: All analyst reports and the Research Manager's decision
  - **Output**: `trader_investment_plan` (actionable trading plan)
  - **Focus**: Translate research into concrete strategy (entries/exits, rationale)

#### ⚠️ Risk Management Team (Iterative Debate → Judge)
1. **Risky Analyst**
   - **Input**: Research team outputs
   - **Output**: High-risk assessment
   - **Focus**: Volatility, downside risks

2. **Safe Analyst**
   - **Input**: Research team outputs
   - **Output**: Conservative risk assessment
   - **Focus**: Capital preservation

3. **Neutral Analyst**
   - **Input**: Research team outputs
   - **Output**: Balanced risk assessment
   - **Focus**: Risk-reward analysis

#### 📈 Portfolio Management Team (Final Decision)
- **Portfolio Manager (Risk Judge)**
  - **Input**: Risk debate outputs (risky/safe/neutral) and prior phases
  - **Output**: `final_trade_decision` (Buy/Hold/Sell with justification)
  - **Focus**: Portfolio-level decision and position sizing

## 2. Execution Order & Dependencies

### 2.1 Execution Flow (as implemented)
1. **Analysis Phase (configurable order)**
   - Default: Market → Social → News → Fundamentals
   - Note: The effective order follows `selected_analysts` at runtime; the default matches above.

2. **Research Debate Phase (iterative)**
   - Alternates: Bull ↔ Bear for N rounds (per `max_debate_rounds`)
   - Then: Research Manager issues `investment_debate_state.judge_decision`

3. **Trading Plan Phase**
   - Trader produces `trader_investment_plan` based on analysts + research decision

4. **Risk Assessment Phase (iterative)**
   - Cycles: Risky → Safe → Neutral for N rounds (per `max_risk_discuss_rounds`)
   - Then: Portfolio Manager (Risk Judge) evaluates and concludes

5. **Final Decision Phase**
   - Portfolio Manager (Risk Judge) issues `final_trade_decision` (Buy/Hold/Sell)
   - Position sizing and portfolio-level considerations captured in the decision

## 3. Implementation Details

### 3.1 Code Structure
- **Main Application**: `trading_agents_streamlit.py`
- **Status Tracking**: Real-time updates via `update_agent_status()`
- **Error Handling**: Per-agent error states and recovery
 - **Graph Orchestration**: `tradingagents/graph/setup.py` wires phases and order; analyst order is read from `selected_analysts`

### 3.2 Key Functions
- `run_real_analysis()`: Main orchestration function
- `update_agent_status()`: Tracks agent states
- `_mark_progress()`: Handles progress tracking
- `generate_markdown_report()`: Creates final output
 - `GraphSetup.setup_graph()`: Defines node/edge wiring (analysts → research → trader → risk → portfolio)

## 4. Error Handling & Fallbacks

### 4.1 Data Validation
- Early API key validation
- Symbol verification before analysis
- Graceful degradation for missing data

### 4.2 Error Recovery
- Per-agent error states
- Clear error messages
- Option to retry failed analyses

### 4.3 Fallback Behavior
- Market data fallbacks for delisted/missing data
- Graceful degradation of non-critical analyses
- Clear user notifications for fallback conditions

## 5. Performance Considerations

### 5.1 Sequential Execution Benefits
- Predictable resource usage
- Clear dependency chain
- Easier debugging
- Deterministic behavior

### 5.2 Future Optimization Potential
- Parallel execution where possible
- Caching of intermediate results
- Background processing for long-running tasks

## 6. Integration Points

### 6.1 Data Sources
- Market data APIs
- News feeds
- Social media APIs
- Financial databases

### 6.2 Output Formats
- Markdown reports
- JSON logs
- Real-time streaming updates
- Exportable analysis results

## 7. Glossary of Outputs

- **`market_report`**
  Short-form narrative produced by the Market Analyst.

- **`sentiment_report`**
  Short-form narrative produced by the Social Analyst.

- **`news_report`**
  Short-form narrative produced by the News Analyst.

- **`fundamentals_report`**
  Short-form narrative produced by the Fundamentals Analyst.

- **`investment_debate_state`** (object)
  - `bull_history`: Bull Researcher arguments/history.
  - `bear_history`: Bear Researcher arguments/history.
  - `history`: Full conversation transcript (if provided by backend).
  - `current_response`: Last speaker marker used for debate flow.
  - `count`: Number of messages/turns used to determine when to stop.
  - `judge_decision`: Research Manager’s synthesized conclusion.

- **`trader_investment_plan`**
  Trader’s actionable plan (entries/exits, rationale, constraints). UI normalizes aliases like `investment_plan` or `trader_plan` into this field.

- **`risk_debate_state`** (object)
  - `risky_history`: Aggressive (Risky) Analyst arguments.
  - `safe_history`: Conservative (Safe) Analyst arguments.
  - `neutral_history`: Neutral Analyst arguments.
  - `history`: Full risk debate transcript (if available).
  - `latest_speaker`: Used to rotate speakers in the debate.
  - `count`: Number of messages/turns used to determine when to stop.
  - `judge_decision`: Portfolio Manager (Risk Judge) summary and guidance.

- **`final_trade_decision`**
  Final BUY/HOLD/SELL recommendation and reasoning from the Portfolio Manager (Risk Judge).
