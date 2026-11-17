# llm-sampling-experiments
# 🧪 LLM Sampling Lab
### Exploring Generation Parameters, Instruction Accuracy & Token Efficiency

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI_SDK-412991?logo=openai&logoColor=white)
![Models](https://img.shields.io/badge/Models_Evaluated-3-blue)
![Runs](https://img.shields.io/badge/Analyzed_Runs-143-brightgreen)
![Study](https://img.shields.io/badge/Type-Experimental_Analysis-orange)

---

## 🎯 Project Overview

**How do LLM sampling parameters influence output quality, instruction-following accuracy, and token consumption?**

This project investigates that question through controlled and exploratory experiments across multiple language models.

Using the OpenAI-compatible API, I tested different configurations of **temperature, top-p, and output-token limits**, moving from simple factual questions to complex multi-step character-decoding problems.

The objective was not merely to generate responses, but to measure the relationship between:

- **Correctness:** Does the model actually solve the task?
- **Consistency:** Does it return the same answer across repeated runs?
- **Token efficiency:** How many tokens does it consume?
- **Sampling behavior:** How do parameter changes affect the output?

### 📊 Explore the Full Analysis

**[View the Interactive HTML Statistical Report](./llm_statistical_report.html)**

The report contains detailed statistical tables, visualizations, individual experiment records, and supporting data.

---

## 📈 Experiment at a Glance

| Metric | Result |
|:---|---:|
| Total recorded API calls | **153** |
| Runs included in final analysis | **143** |
| LLMs tested | **3** |
| Distinct prompt versions | **11** |
| Experiment configurations | **40** |
| Total analyzed tokens | **180,837** |
| Input tokens | 28,503 |
| Output tokens | 152,334 |

**Models:** GPT-4o-mini · GPT-6 Luna · Mistral Nemo

*Ten runs with temperature 0.7 were intentionally excluded from the final analysis.*

---

## 🔬 Experimental Design

The experiments progressed through increasingly difficult tasks:

| Task | What Was Tested |
|---|---|
| 🚗 Text Generation | Response generation under different sampling settings |
| 🌍 Factual QA | Basic and advanced factual responses |
| 🔢 Number Sorting | Deterministic instruction-following |
| 🔤 Character Extraction | Multi-step string manipulation |
| 🧩 8×8 Grid Decoding | Column traversal, character extraction, reversal, and reconstruction |

For deterministic tasks, responses could be compared against programmatically derived correct answers.

This helped separate **plausible-looking responses** from actual task completion.

---

## 🏆 Key Finding: Accuracy vs. Token Efficiency

The most interesting experiment involved decoding a hidden sentence from an **8×8 grid of words**.

Both models received the same puzzle under the logged configuration:

- Temperature: `0`
- Top-p: `0`
- Maximum output tokens: `10,000`

### Head-to-Head Results

| Metric | GPT-4o-mini | GPT-6 Luna |
|---|---:|---:|
| Attempts | 10 | 5 |
| Correct answers | **0/10** | **5/5** |
| Mean output tokens | 42.80 | 2,584.40 |
| Median output tokens | 46.50 | 2,264.00 |
| Mean total tokens | 308.80 | 2,849.40 |
| Median total tokens | 312.50 | 2,529.00 |

### 💡 What This Revealed

Luna achieved **100% observed accuracy** on five recorded attempts, while GPT-4o-mini failed all ten.

However, Luna consumed approximately **9.23× more total tokens per request** on average.

This illustrates an important distinction:

> **Generating fewer tokens does not necessarily mean completing a task more efficiently. Accuracy and resource consumption must be evaluated together.**

These findings apply to this specific puzzle and experimental setup, not to general model capabilities.

---

## 🌡️ How Did Temperature Affect Performance?

On the simpler 30-letter decoding task, Luna produced the correct normalized answer in all **18 included runs** across the tested temperatures.

| Temperature | Runs | Accuracy | Mean Output Tokens |
|---|---:|---:|---:|
| 0.0 | 5 | 5/5 | 513.60 |
| 1.0 | 4 | 4/4 | 540.25 |
| 1.5 | 4 | 4/4 | 694.00 |
| 2.0 | 5 | 5/5 | 655.20 |

**Observations:**

- Higher temperature did not necessarily reduce accuracy.
- Token consumption varied even when responses were correct.
- Output-token usage did not increase monotonically with temperature.
- A single sampling configuration cannot be declared universally optimal from these results.

---

## 📉 Statistical Analysis & Validation

The analysis examined:

- Mean and median token consumption
- Standard deviation and variance-related measures
- Quartiles and interquartile range
- Token-consumption distributions
- Response consistency
- Deterministic answer correctness
- Outliers, empty responses, and token-cap exhaustion

### Data Integrity

The original 153 experiment records underwent independent parsing and validation.

**Verification results:**

- Two parsers agreed on all 153 records.
- All recorded input, output, and total token counts reconciled.
- All 40 configuration groups were independently recomputed.
- 558 plotted raw-data marks and 113 summary values were reconciled.
- CSV exports were checked against the source records.

Two unsuccessful Luna calls returned empty visible responses while consuming a combined **3,530 tokens**. They were retained in the analysis rather than discarded.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Experiment execution |
| OpenAI SDK | Model API integration |
| AICredits | Access to supported LLMs |
| python-dotenv | Environment-based configuration |
| CSV | Structured experimental data |
| HTML | Statistical report and visualizations |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/llm-sampling-experiments.git
cd llm-sampling-experiments
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
pip install -r requirement.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```dotenv
AICREDITS_API_KEY=your_api_key_here
AICREDITS_BASE_URL=https://api.aicredits.in/v1

MODEL=openai/gpt-4o-mini
TEMPERATURE=0.7
TOP_P=1.0
MAX_TOKENS=1000
```

### 4. Run an Experiment

```bash
python llm_call.py
```

The script records the prompt, model configuration, response, timestamp, and API-reported token usage in `llm_outputs.txt`.

Modify `.env` to experiment with different supported models and sampling parameters.

---

## ⚠️ Experimental Limitations

This is an exploratory study, not a standardized general-purpose benchmark.

- Some experiments used different prompts and output-token limits.
- Sample sizes were small and uneven across configurations.
- Runs were collected sequentially rather than randomized.
- Factual QA outputs were not formally scored for accuracy.
- Backend sampling behavior, latency, monetary cost, and reasoning-token breakdowns were not independently verified.

Consequently, the findings are descriptive observations rather than statistically established causal effects.

---

## 🔭 Future Improvements

- Expand testing across multiple independently validated puzzle instances.
- Randomize experiment execution order.
- Use identical sample sizes for each configuration.
- Measure end-to-end latency and monetary cost.
- Separate visible-response correctness from formatting compliance.
- Establish confidence intervals for repeated-run success rates.

---

## 📌 Conclusion

This experiment highlights three important principles for LLM evaluation:

**1. Correctness comes before token efficiency.** A cheap but incorrect answer may provide no practical value.

**2. Sampling parameters interact with task complexity.** Higher temperature does not automatically imply worse results.

**3. Model comparisons require careful experimental controls.** Prompt changes, output caps, and unequal sample sizes can distort conclusions.

The project demonstrates hands-on experimentation with model inference, sampling configuration, API instrumentation, objective evaluation, and statistical analysis.

---

*An experimental AI engineering project focused on understanding LLM behavior through measurable evidence.*
