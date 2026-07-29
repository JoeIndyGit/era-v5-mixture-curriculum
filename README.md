# ERA V5 — Mixture and Curriculum Specification

> **Decision:** GO to the 1B proxy; full-scale training remains gated by the 1B and 3B results.  
> **Reference budget:** 100B tokens. Percentages scale linearly.  
> **Core hypothesis:** an 18% protected Indic lane plus explicit reasoning, agentic and long-context lanes will improve target capabilities without more than 2% regression in general language or code.

## 1. Final mixture

| Capability lane | Share | Data that fills it | Benchmark it must win | Defence |
|---|---:|---|---|---|
| General language and knowledge | 23% | FineWeb-Edu | MMLU, ARC-C, HellaSwag | Broad foundation; supply is abundant, so it is capped |
| Indic languages | 18% | Sangraha verified, unverified and synthetic pools | IndicGenBench, MILU, FLORES-200 | Protected multilingual objective; 10% failed the completed pilot |
| Code | 14% | The Stack v2, deterministic PyPI source snapshot | HumanEval+, MBPP+ | Preserves executable code without allowing Python to dominate |
| Explicit reasoning | 11% | FLAN reasoning/CoT, Super-NaturalInstructions, verified generation | BBH, ARC-C, MuSR | High-priority lane, bounded by verifiable supply |
| Mathematics | 8% | OpenWebMath, OpenMathInstruct-2 | GSM8K, MATH | Real mathematical supply supports the allocation |
| Agentic and tool use | 4% | AgentInstruct, executable tool traces, recovery trajectories | AgentBench, tool validity, recovery rate | Reduced from 7% after exposing the real-data shortage |
| Long context | 6% | Long natural documents, repository-level code, LongAlign task structures | RULER, LongBench | Requires distributed evidence rather than long padding |
| Science and specialist | 4% | peS2o/Dolma academic material, SciRIFF | SciRIFF held-out, GPQA | High-quality scientific supply supports a clean lane |
| Safety and instruction integrity | 2% | BeaverTails, PKU-SafeRLHF, verified counterfactuals | HarmBench and benign over-refusal | Safety is a mandatory gate, not an average |
| Annealing reserve | 10% | Highest-quality subsets only | Final aggregate and stability checks | Protected cooldown; unavailable to the selector |
| **Total** | **100%** | | | |

## 2. Indic allocation

Sangraha contains 251B tokens across 22 languages and reports the following relevant pools: Hindi 34.54B, Tamil 17.36B and Telugu 16.28B. Its original `synthetic` split contains machine-translated native-script text and romanised/transliterated text; V5 separates those into translated and synthetic tiers.

| Language | Verified | Unverified | Translated | Synthetic | Total |
|---|---:|---:|---:|---:|---:|
| Hindi | 3.0B | 2.4B | 1.2B | 0.6B | 7.2B |
| Tamil | 2.5B | 1.4B | 1.0B | 0.5B | 5.4B |
| Telugu | 2.6B | 0.7B | 1.4B | 0.7B | 5.4B |
| **Total** | **8.1B (45%)** | **4.5B (25%)** | **3.6B (20%)** | **1.8B (10%)** | **18B** |

Only Telugu-unverified needs replay: `0.70 / 0.6474 = 1.08×`, below the 1.25× cap for unverified data. Translated and synthetic items retain source ID, generator/translator version, prompt, verification result and contamination status.

## 3. Real-supply accounting

| Lane | Published supply supporting the decision | Target | Replay or generation disclosed |
|---|---:|---:|---|
| General | FineWeb-Edu: 1.3T tokens | 23B | No replay |
| Indic | Sangraha Hindi/Tamil/Telugu: 68.18B tokens | 18B | One 1.08× tier-language replay |
| Code | The Stack v2 train-full: approximately 900B tokens | 14B | No replay after licence filtering |
| Mathematics | OpenWebMath: 14.7B tokens | 8B | No corpus-level replay |
| Reasoning | Curated reasoning sources plus verifiable math/instruction pools | 11B | 4B must be generated and verified |
| Agentic | AgentInstruct-style generated pairs plus executable environments | 4B | 3.2B must be execution-generated |
| Long context | Long natural documents plus 10K LongAlign task structures | 6B | No document replay; task structures may be regenerated |
| Science | Dolma academic publications and SciRIFF | 4B | No replay |
| Safety | Human-labelled safety pairs and comparisons | 2B | 1.6B verified counterfactual tokens required |

A target is reduced rather than silently oversampled when it cannot be met inside these caps:

- verified/expert: 3.0×;
- code: 2.5×;
- translated: 2.0×;
- synthetic: 1.5×;
- unverified web: 1.25×.

## 4. Protected floor and anneal

The selector cannot cross the **53% always-on floor**:

| General | Indic | Code | Reasoning | Math | Agentic | Long | Science | Safety |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 13% | 14% | 8% | 7% | 4% | 2% | 3% | 1% | 1% |

The final **10B anneal reserve** is inaccessible during ordinary training:

- 2.5B verified general/educational;
- 2.0B verified native Indic;
- 1.5B high-quality code;
- 2.0B verifiable reasoning and mathematics;
- 1.0B agentic and long-context;
- 1.0B safety and instruction integrity.

Low-quality web text, unresolved licences, unverified rationales and heavily repeated documents are excluded.

## 5. Curriculum

| Stage | Budget | Difficulty distribution | Reasoning-length emphasis | Context |
|---|---:|---|---|---|
| Foundation | 0–20% | D1 50, D2 35, D3 13, D4 2 | R0–R1: 80% | 2K–8K |
| Capability build | 20–55% | D1 30, D2 40, D3 25, D4 5 | R1–R2: 65% | 4K–16K |
| Integration | 55–80% | D1 15, D2 30, D3 40, D4 15 | R2–R3: 58% | 8K–32K |
| Consolidation | 80–90% | D1 10, D2 25, D3 42, D4 23 | R3–R4: 37% | 16K–target |
| Annealing | final 10% | D1 15, D2 30, D3 40, D4 15 | R1–R3: 83% | Mixed |

**Difficulty examples**

- **D1 – Direct understanding:** Identify the language and source tier of a single training sample (e.g., classify a document as verified Tamil or translated Hindi).
- **D2 – Quality assessment:** Compare two candidate samples and select the higher-quality one based on language confidence, provenance, duplication score, and formatting quality.
- **D3 – Multi-constraint data selection:** Decide whether a Telugu reasoning sample should be included in the training mixture by evaluating licence compliance, contamination risk, reasoning length, difficulty band, and replay limits.
- **D4 – Mixture optimisation:** Analyse dataset inventory, benchmark performance, proxy experiment results, and token budget constraints to recommend an updated data mixture while preserving the protected Indic floor and annealing reserve.

**Reasoning-length examples**

- **R0, 0–1 decisions:** identify Tamil versus Telugu.
- **R1, 2–3:** calculate and format an arrival time.
- **R2, 4–7:** apply four configuration levels.
- **R3, 8–15:** trace request handler → service → domain → adapter.
- **R4, 16+:** complete a multi-tool workflow, recover from failure and verify the final state.

A long-context example qualifies only when its answer depends on evidence outside both the first and last 20% of the sequence.

## 6. Cleaning gate and cumulative target

The cohort may train only after **≥95% of every lane target** is cleaned and documented. The next cleaning sprint is directed at the quantified shortages:

| Priority | Starved slot | Required addition | Admission test |
|---:|---|---:|---|
| 1 | Agentic | 3.2B execution-generated tokens | Tool execution succeeds; state and recovery are verifiable |
| 2 | Reasoning | 4.0B verified generated tokens | Deterministic answer, executable proof or dual-review agreement |
| 3 | Safety | 1.6B counterfactual tokens | Harm label agreement and benign-control audit |
| 4 | Telugu | 0.0526B additional/replayed unverified tokens | Language/script audit and ≤1.25× replay |
| 5 | Long context | 6B admitted task tokens | Evidence-position and answer-dependency checks |

Mandatory gates:

1. provenance and licence decision for every admitted shard;
2. exact and near-deduplication across all lanes;
3. benchmark 13-gram matches below 0.1%, with every match reviewed;
4. fewer than one accepted PII/secret leak per 10M audited tokens;
5. human audit acceptance ≥95% verified, ≥85% unverified and ≥90% translated;
6. generated-data verification acceptance ≥85%;
7. tokenizer fertility reported separately for Hindi, Tamil and Telugu;
8. replay limits respected and train–validation divergence checked.

## 7. Proxy evidence and experiment

### Completed pilot

Nine neural micro-proxy runs—three mixtures × three seeds—were completed.

| Proposed 18% Indic versus control | Result |
|---|---:|
| Weighted accuracy | **+9.50%** |
| Weighted NLL | **2.34% lower** |
| Indic accuracy | **+12.96%** |
| General NLL | 1.78% worse |
| Code NLL | 1.81% worse |
| Hindi accuracy | **+40.8%** |
| Tamil accuracy | +4.8% |
| Telugu accuracy | **−10.1%** |

**Pilot decision:** reject the 10% Indic ablation, retain 18% for the transformer proxy, and prioritize Telugu cleaning. The pilot validates direction and experiment plumbing; it is not presented as a 1B result.

### 1B and 3B commitment

The 1B stage screens five mixtures—control, final plan, Indic-14%, agentic-2% and no-anneal—then confirms the top two across three seeds. The 3B stage compares the 1B winner with control.

Full-scale approval requires:

- Indic macro +8% and Hindi, Tamil and Telugu each +5%;
- reasoning and mathematics each +3%;
- agentic and long-context each +5%;
- science +2%;
- general and code regressions no worse than 2%;
- no safety regression;
- 95% paired-bootstrap confidence intervals supporting the gains;
- no material replay-driven train–validation divergence.

Exact configurations are in `configs/proxy_1b.yaml` and `configs/proxy_3b.yaml`.

## 8. Decision

| Gate | Verdict |
|---|---|
| Mixture specification | **PASS** |
| Supply accounting | **PASS — shortages and generation volumes are explicit** |
| Cleaning priority | **PASS — aimed at the starved slots** |
| Completed pilot | **PASS** |
| Advance to 1B | **GO** |
| Advance to 3B | Gated by 1B |
| Full-scale training | **NO-GO until both transformer stages pass** |

This is the testable claim being submitted:

> **An 18% Indic allocation is supportable without wishful accounting; the main risks are not headline supply but Telugu quality, verified agentic trajectories and verifiable long-horizon reasoning. The full mixture is accepted only if the predefined 1B and 3B gates confirm that trade-off.**

## Repository evidence

- `REVIEWER_DEFENCE.md` — answers to the likely challenge questions.
- `EVIDENCE_REGISTER.md` — separates measured, published and proposed claims.
- `data/inventory.csv` — source-level supply and admission decisions.
- `data/indic_allocation.csv` — language × tier accounting.
- `data/cleaning_ledger.csv` — cumulative target and starvation work.
- `data/benchmark_contract.csv` — lane-to-benchmark gates.
- `configs/` — executable 1B and 3B experiment specifications.
- `results/` — completed pilot evidence.

## Primary references

1. FineWeb-Edu dataset card — 1.3T-token educational corpus.
2. IndicLLMSuite/Sangraha paper — 251B tokens and language-level verified, synthetic and unverified counts.
3. The Stack v2 train-full dataset card — approximately 900B code tokens.
4. OpenWebMath dataset card — 14.7B mathematical tokens.
5. Dolma dataset card — 3T-token mixed corpus including academic publications.
6. AgentInstruct paper — large-scale synthetic agentic-data generation.
7. LongAlign paper/repository — 10K long-context instruction examples.
8. BeaverTails and PKU-SafeRLHF papers — human-labelled safety data.
9. IndicGenBench, MILU, RULER and LongBench — target evaluation suites.
10. DoReMi and DataComp-LM — proxy-based mixture and data-selection methodology.
