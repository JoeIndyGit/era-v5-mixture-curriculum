# Reviewer Defence

## Why 18% Indic?
The completed pilot rejects the 10% ablation and improves Indic macro accuracy by 12.96%. Published Sangraha supply for Hindi, Tamil and Telugu totals 68.18B tokens, so 18B can be allocated with only one 1.08× replay. The 18% remains a hypothesis until the 1B/3B gates pass.

## Why 4% agentic rather than 7%?
A supply audit showed that 7B would rely too heavily on generated trajectories. At 4B, 0.8B may come from curated/released sources and 3.2B from execution-generated trajectories. The synthetic dependence is explicit and independently gated.

## Why 11% reasoning?
Reasoning is a target capability, but only verifiable traces are admitted. The plan caps it at 11B and openly states that 4B must be generated and verified.

## Why a 10% anneal?
It is large enough to alter the end-of-run quality distribution while leaving 90% for broad capability acquisition. A no-anneal ablation is included in the 1B screen, so the number can be rejected.

## What prevents Hindi from hiding Tamil/Telugu failure?
Indic is reported as a macro average and separately by language. Every language must improve by at least 5%; one language failure blocks advancement.

## How is translated data distinguished from synthetic?
Translated data is native-script machine translation retaining a source-document link. Synthetic data includes romanised/transliterated text and generated capability tasks. Both retain generator metadata, but they have different caps and audits.

## How is long-context validity tested?
An example is admitted only when the answer depends on evidence outside the first and last 20% of the sequence. Evaluation is stratified by length and evidence position.

## How is synthetic reasoning verified?
By deterministic answer checking, code execution, proof checking where available, or dual-review agreement. Unverifiable verbose rationales are rejected.

## Why trust the pilot?
It is used only to reject the 10% Indic candidate and validate experimental plumbing. It is explicitly not used as a substitute for the required transformer proxies.

## What would change the final mixture?
Any failed mandatory gate. Percentages are versioned hypotheses, not commitments protected from evidence.
