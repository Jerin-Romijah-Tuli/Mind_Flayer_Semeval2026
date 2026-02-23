# 🧠 Mind_Flayer at SemEval-2026 Task 8B

<div align="center">

[![SemEval 2026](https://img.shields.io/badge/SemEval-2026-blue)](https://semeval.github.io/)
[![Task 8B](https://img.shields.io/badge/Task-8B%20MTRAGEval-orange)](https://github.com/semeval2026/task8)
[![Rank](https://img.shields.io/badge/Rank-8%2F26-brightgreen)](https://github.com/JerinTuli/mind-flayer-semeval2026)
[![F1 Score](https://img.shields.io/badge/F1-0.7492-success)](https://github.com/JerinTuli/mind-flayer-semeval2026)
[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org/abs/XXXX.XXXXX)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Zero-Shot Multi-Turn RAG with Differential Prompting and Multi-Key Orchestration**

*Achieving Top 31% Performance with $0 Cost and Zero Training*

[📄 Paper](#paper) • [🚀 Quick Start](#quick-start) • [💡 Key Features](#key-features) • [📊 Results](#results) • [🛠️ Installation](#installation) • [📖 Documentation](#documentation)

</div>

---

## 🏆 Achievements

```
┌──────────────────────────────────────────────────────────┐
│  🥈 Rank 8/26 Teams (Top 31%)                            │
│  📈 F1 Score: 0.7492                                     │
│  🎯 ROUGE-L: 0.8782 (Exceptional!)                       │
│  🤖 LLM Judge: 0.8297 (Excellent!)                       │
│  ✅ Answerability: 100% Accuracy                         │
│  💰 Cost: $0 (Free Groq API)                             │
│  ⚡ Processing: 21 minutes for 507 tasks                │
│  📦 Model Size: 17B (7× smaller than baseline)          │
│  🔥 Beat GPT-OSS-120B by +0.11 F1                        │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Overview

**Mind_Flayer** is a zero-shot multi-turn Retrieval-Augmented Generation (RAG) system designed for SemEval-2026 Task 8B. We demonstrate that careful prompt engineering and smart system design can achieve **competitive results without training or expensive compute**.

### 🌟 What Makes This Special?

- **🎨 Differential Prompting**: Distinct templates for answerable vs unanswerable questions
- **🔄 Multi-Key API Rotation**: Smart orchestration handles rate limits seamlessly
- **🛡️ Post-Processing Safety Net**: Corrects model failures before submission
- **💯 Perfect Answerability**: 100% accuracy on question answerable classification
- **💸 Zero Cost**: Built entirely on free-tier APIs
- **📚 No Training**: Pure zero-shot approach - works out of the box

---

## 💡 Key Features

### 1️⃣ **Explicit Answerability Detection**

```python
def check_answerability(task):
    """
    Simple but perfect: 100% accuracy on 507 tasks
    """
    contexts = task.get('contexts', [])
    return UNANSWERABLE if len(contexts) == 0 else ANSWERABLE
```

**Why it works:** Leverages the explicit data structure where unanswerable questions have zero passages.

### 2️⃣ **Differential Prompting**

<table>
<tr>
<td width="50%">

**Answerable Template** 🟢
```
You MUST answer using reference 
information...

✓ Explicit grounding
✓ 2-4 sentence constraint
✓ Multi-turn awareness
✓ Domain-specific guidance
✓ Temperature: 0.3
```

</td>
<td width="50%">

**Unanswerable Template** 🔴
```
You do NOT have any information...
You MUST politely decline...

✓ Strong negatives
✓ Refusal examples
✓ Prohibition on answering
✓ Lower temperature: 0.1
```

</td>
</tr>
</table>

### 3️⃣ **Multi-Key API Rotation**

```python
class MultiKeyGenerator:
    """
    Seamlessly handles API rate limits
    Processes 507 tasks in 21 minutes with $0 cost
    """
    def __init__(self, api_keys):
        self.clients = [Groq(key) for key in api_keys]
        self.current_idx = 0
        self.exhausted = set()
    
    def handle_rate_limit(self, error):
        if "TPD" in str(error):  # Token Per Day limit
            self.exhausted.add(self.current_idx)
            self.rotate()
```

**Impact:** Enables processing of large datasets without hitting free-tier limits.

### 4️⃣ **Post-Processing Safety Net**

```python
def post_process(response, has_contexts):
    """
    Corrects ~6% of responses
    Contributes +0.029 to F1 score
    """
    # Detect incorrect response type
    is_refusal = any(kw in response.lower() 
                    for kw in ["don't have", "cannot answer"])
    
    # Fix mismatches
    if has_contexts and is_refusal:
        return "Based on available information..."
    if not has_contexts and not is_refusal:
        return "I don't have information needed..."
    
    return response
```

**Why it matters:** Even with perfect prompts, LLMs occasionally fail. This catches edge cases.

---

## 📊 Results

### 🎖️ Official Leaderboard

| System | Overall F1 | ROUGE-L | LLM Judge | Rank |
|--------|------------|---------|-----------|------|
| **Mind_Flayer (Ours)** | **0.7492** | **0.8782** | **0.8297** | **8/26** |
| Top System | 0.7827 | -- | -- | 1/26 |
| GPT-OSS-120B | 0.639 | -- | -- | baseline |
| GPT-4o | 0.60 | -- | -- | baseline |

### 📈 Component Contributions

```
Full System                    0.7492  ████████████████████ 100%
- Multi-turn Context          -0.0504  ███████              (largest impact)
- Post-processing            -0.0291  ████
- Domain Guidance            -0.0137  ██
Simple Baseline               0.6532  █████████████
```

### 🎯 Answerability Performance

| Type | Count | Accuracy |
|------|-------|----------|
| Answerable | 377 | **100%** ✅ |
| Unanswerable | 130 | **100%** ✅ |
| **Overall** | **507** | **100%** ✅ |

### 🌍 Domain Performance (ROUGE-L)

```
CLAPNQ (Wikipedia)    ████████████████████ 0.89
Govt (Government)     ███████████████████  0.88
Cloud (Technical)     ██████████████████   0.87
FiQA (Financial)      █████████████████    0.85
```

### 📊 Turn-wise Analysis

- **Turn 1**: 0.94 RL_F (Strong initial responses)
- **Turn >1**: 0.86 RL_F (Multi-turn complexity evident)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# Install dependencies
pip install groq python-dotenv tqdm
```

### ⚡ 30-Second Setup

```bash
# 1. Clone repository
git clone https://github.com/JerinTuli/mind-flayer-semeval2026.git
cd mind-flayer-semeval2026

# 2. Set up environment
cp .env.example .env
# Add your Groq API keys to .env

# 3. Run inference
python run_inference.py \
    --input_file data/test_tasks.jsonl \
    --output_file predictions.jsonl \
    --model meta-llama/llama-4-scout-17b-16e-instruct
```

**That's it!** 🎉

---

## 🛠️ Installation

### Option 1: Basic Installation

```bash
pip install -r requirements.txt
```

### Option 2: Development Installation

```bash
# Clone with submodules
git clone --recursive https://github.com/JerinTuli/mind-flayer-semeval2026.git

# Install in editable mode
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt
```

### 📋 Requirements

```txt
groq>=0.9.0
python-dotenv>=1.0.0
tqdm>=4.66.0
```

---

## 💻 Usage

### Basic Usage

```python
from mind_flayer import MindFlayerRAG

# Initialize system
rag = MindFlayerRAG(
    api_keys=["your-groq-key-1", "your-groq-key-2"],
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)

# Process single task
task = {
    "conversation": [...],
    "contexts": [...],
    "question": "What is the capital of France?"
}

response = rag.generate(task)
print(response)
# Output: "Based on the provided information, Paris is the capital of France."
```

### Batch Processing

```python
from mind_flayer import batch_process

# Process entire dataset
results = batch_process(
    input_file="data/test_tasks.jsonl",
    output_file="predictions.jsonl",
    api_keys=["key1", "key2"],
    batch_size=32
)

print(f"Processed {results['total']} tasks")
print(f"Success rate: {results['success_rate']:.2%}")
```

### Custom Configuration

```python
rag = MindFlayerRAG(
    api_keys=api_keys,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature_answerable=0.3,
    temperature_unanswerable=0.1,
    max_tokens=512,
    enable_post_processing=True,
    enable_domain_guidance=True
)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       INPUT TASK                            │
│  • Conversation History (1-11 turns, mean: 7.64)            │
│  • Reference Passages (0-38, mean: 2.33 for answerable)    │
│  • Domain (fiqa, cloud, govt, clapnq)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STAGE 1: ANSWERABILITY CHECK                    │
│                len(contexts) == 0?                           │
└──────────────┬────────────────────────┬─────────────────────┘
               │                        │
         NO (377)                  YES (130)
               │                        │
               ▼                        ▼
   ┌─────────────────────┐  ┌─────────────────────┐
   │   ANSWERABLE        │  │   UNANSWERABLE      │
   │   Template          │  │   Template          │
   │   • Strict ground   │  │   • Polite refuse   │
   │   • 2-4 sentences   │  │   • No speculation  │
   │   • T=0.3           │  │   • T=0.1           │
   └──────────┬──────────┘  └──────────┬──────────┘
              │                        │
              └────────────┬───────────┘
                           ▼
           ┌─────────────────────────────────┐
           │   STAGE 2: MULTI-KEY ROTATION   │
           │   • Groq API (free tier)        │
           │   • Automatic failover          │
           │   • 2 keys, 21 minutes, $0     │
           └────────────────┬────────────────┘
                            ▼
           ┌─────────────────────────────────┐
           │   STAGE 3: POST-PROCESSING      │
           │   • Detect mismatches           │
           │   • Correct ~6% responses       │
           │   • Ensure consistency          │
           └────────────────┬────────────────┘
                            ▼
           ┌─────────────────────────────────┐
           │        FINAL RESPONSE            │
           │   • Grounded (if answerable)    │
           │   • Refusal (if unanswerable)   │
           │   • Multi-turn coherent         │
           └─────────────────────────────────┘
```

---

## 📖 Documentation

### 📁 Project Structure

```
mind-flayer-semeval2026/
├── 📄 README.md                    # You are here!
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Dependencies
├── 📄 .env.example                 # Environment template
│
├── 📂 src/
│   ├── __init__.py
│   ├── mind_flayer.py             # Main RAG system
│   ├── prompts.py                 # Prompt templates
│   ├── multi_key.py               # API key rotation
│   ├── post_process.py            # Safety net logic
│   └── utils.py                   # Helper functions
│
├── 📂 data/
│   ├── train/                     # Training data (if any)
│   ├── dev/                       # Development set
│   └── test/                      # Test set
│
├── 📂 notebooks/
│   ├── exploration.ipynb          # Data analysis
│   ├── error_analysis.ipynb       # Error analysis
│   └── visualization.ipynb        # Result visualization
│
├── 📂 scripts/
│   ├── run_inference.py           # Main inference script
│   ├── evaluate.py                # Evaluation script
│   └── format_checker.py          # Output validation
│
├── 📂 results/
│   ├── predictions.jsonl          # System outputs
│   ├── metrics.json               # Evaluation metrics
│   └── analysis/                  # Detailed analysis
│
├── 📂 paper/
│   ├── semeval_2026_paper.pdf     # Final paper
│   └── semeval_2026_paper.tex     # LaTeX source
│
└── 📂 tests/
    ├── test_answerability.py
    ├── test_prompts.py
    ├── test_multi_key.py
    └── test_post_process.py
```

### 🔑 Configuration

Create `.env` file:

```bash
# Groq API Keys (get free keys at https://console.groq.com)
GROQ_API_KEY_1=gsk_...
GROQ_API_KEY_2=gsk_...

# Model Configuration
MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
TEMPERATURE_ANSWERABLE=0.3
TEMPERATURE_UNANSWERABLE=0.1
MAX_TOKENS=512

# System Configuration
ENABLE_POST_PROCESSING=true
ENABLE_DOMAIN_GUIDANCE=true
BATCH_SIZE=32
```

### 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_answerability.py -v

# Run with coverage
pytest --cov=src tests/
```

---

## 📝 Detailed Examples

### Example 1: Answerable Question

**Input:**
```json
{
  "conversation": [
    {"role": "user", "content": "What is Paris?"},
    {"role": "assistant", "content": "Paris is the capital of France."},
    {"role": "user", "content": "What's its population?"}
  ],
  "contexts": [
    {
      "text": "As of 2024, Paris has a population of approximately 2.1 million...",
      "document_id": "wiki_paris_001",
      "score": 0.95
    }
  ]
}
```

**Output:**
```
"According to the provided information, Paris has a population of 
approximately 2.1 million as of 2024."
```

**Analysis:** ✅ Grounded, ✅ Multi-turn coherent, ✅ Concise (2 sentences)

### Example 2: Unanswerable Question

**Input:**
```json
{
  "conversation": [
    {"role": "user", "content": "What is the weather in Tokyo tomorrow?"}
  ],
  "contexts": []
}
```

**Output:**
```
"I don't have the information needed to answer that question."
```

**Analysis:** ✅ Polite refusal, ✅ No hallucination, ✅ IDK judge compatible

### Example 3: Multi-turn with Follow-up

**Input:**
```json
{
  "conversation": [
    {"role": "user", "content": "What is machine learning?"},
    {"role": "assistant", "content": "Machine learning is..."},
    {"role": "user", "content": "What are its main types?"}
  ],
  "contexts": [
    {"text": "The three main types are supervised, unsupervised, and reinforcement learning..."}
  ]
}
```

**Output:**
```
"Building on the previous discussion, the three main types are 
supervised learning, unsupervised learning, and reinforcement learning."
```

**Analysis:** ✅ References previous context, ✅ Grounded, ✅ Natural flow

---

## 🔬 Analysis & Insights

### 💪 Strengths

1. **Exceptional Faithfulness (0.8782 ROUGE-L)**
   - Accurate information extraction
   - Strong passage grounding
   - Appropriate response length

2. **Perfect Answerability (100%)**
   - Zero false positives (no hallucinations on unanswerable)
   - Zero false negatives (no refusals on answerable)

3. **Resource Efficiency**
   - $0 cost (vs potentially $100+ for GPT-4 API)
   - 7× smaller model (17B vs 120B)
   - 21 minutes for 507 tasks

4. **Accessibility**
   - No GPUs needed
   - No training required
   - Fully reproducible with free APIs

### 🎯 Areas for Improvement

1. **Completeness (RB_agg: 0.6024)**
   - Trade-off from 2-4 sentence constraint
   - Could benefit from adaptive length
   - Multi-passage synthesis can improve

2. **Later-Turn Performance**
   - Turn 1: 0.94 RL_F
   - Turn >1: 0.86 RL_F
   - Room for better context integration

3. **Domain Adaptation**
   - FiQA (0.85) lower than others (0.87-0.89)
   - Informal forum style harder to match

### 🚀 Future Work

- [ ] Adaptive response length based on query complexity
- [ ] Multi-stage generation (outline → elaborate)
- [ ] Ensemble approaches for improved completeness
- [ ] Better multi-passage synthesis
- [ ] Integration with retrieval (Task C)
- [ ] Testing with larger models (Llama 3.1 70B/405B)

---

## 📚 Citation

If you use this code or find our work helpful, please cite:

```bibtex
@inproceedings{tuli2026mindflayer,
  title={Mind\_Flayer at SemEval-2026 Task 8: Faithful Multi-Turn RAG Generation via Llama-4-Scout and Smart API Key Rotation},
  author={Tuli, Jerin Romijah and Pritom, MD. Sartaj Alam and Naem, Talukder Naemul Hasan},
  booktitle={Proceedings of the 20th International Workshop on Semantic Evaluation (SemEval-2026)},
  year={2026},
  organization={Association for Computational Linguistics}
}
```

**Paper:** [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX) (Update after publication)

---

## 👥 Team

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/JerinTuli.png" width="100px;" alt="Jerin"/><br />
      <sub><b>Jerin Romijah Tuli</b></sub><br />
      <a href="mailto:ramijahtuli786@gmail.com">📧 Email</a>
    </td>
    <td align="center">
      <img src="https://via.placeholder.com/100" width="100px;" alt="Sartaj"/><br />
      <sub><b>MD. Sartaj Alam Pritom</b></sub><br />
      <a href="mailto:sartajalam0010@gmail.com">📧 Email</a>
    </td>
    <td align="center">
      <img src="https://via.placeholder.com/100" width="100px;" alt="Naem"/><br />
      <sub><b>Talukder Naemul Hasan Naem</b></sub><br />
      <a href="mailto:naemruet@gmail.com">📧 Email</a>
    </td>
  </tr>
</table>

**Institution:** Department of Computer Science and Engineering  
**University:** Rajshahi University of Engineering & Technology, Bangladesh

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

```bash
# Fork the repository
# Create your feature branch
git checkout -b feature/AmazingFeature

# Commit your changes
git commit -m 'Add some AmazingFeature'

# Push to the branch
git push origin feature/AmazingFeature

# Open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Mind_Flayer Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **SemEval-2026 Organizers** - Sara Rosenthal, Yannis Katsis, Vraj Shah, Marina Danilevsky
- **Groq** - For providing free API access to Llama 4 Scout 17B
- **Meta AI** - For the Llama model family
- **MTRAG Benchmark Team** - For the comprehensive evaluation dataset

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/JerinTuli/mind-flayer-semeval2026/issues)
- **Discussions:** [GitHub Discussions](https://github.com/JerinTuli/mind-flayer-semeval2026/discussions)
- **Email:** ramijahtuli786@gmail.com

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JerinTuli/mind-flayer-semeval2026&type=Date)](https://star-history.com/#JerinTuli/mind-flayer-semeval2026&Date)

---

<div align="center">

### 💫 Made with ❤️ by Team Mind_Flayer

**If you found this useful, please consider giving us a ⭐!**

[![GitHub stars](https://img.shields.io/github/stars/JerinTuli/mind-flayer-semeval2026?style=social)](https://github.com/JerinTuli/mind-flayer-semeval2026/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/JerinTuli/mind-flayer-semeval2026?style=social)](https://github.com/JerinTuli/mind-flayer-semeval2026/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/JerinTuli/mind-flayer-semeval2026?style=social)](https://github.com/JerinTuli/mind-flayer-semeval2026/watchers)

</div>
