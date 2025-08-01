edu-chatbot-opro/
│
├── README.md
├── requirements.txt
├── .env               # For storing API keys securely (e.g., Gemini, Claude)
├── config.yaml        # Optional: for storing model, task, or tuning configs
│
├── prompts/
│   ├── base_prompts/         # Original manually-written prompts
│   ├── tuned_prompts/        # Optimized prompts from OPro runs
│   └── prompt_templates.py   # Jinja or string-template scripts
│
├── models/
│   ├── gemini_flash_client.py    # Gemini 2.0 & 2.5 Flash API wrapper (main task executors)
│   ├── gemini_pro_client.py      # Gemini 2.5 Pro API wrapper (evaluator)
│   ├── claude_client.py          # Claude API wrapper (optional)
│   ├── gpt_client.py             # Optional GPT wrapper
│   └── local_runner.py           # Optional local LLMs via Ollama or HuggingFace
│
├── optimizer/
│   ├── opro_engine.py            # Core logic: OPro optimization pipeline (uses Gemini Flash for prompt optimization)
│   ├── scorer.py                 # Uses Gemini 2.5 Pro as evaluator/reward model
│   └── search_strategies.py      # Grid search, beam, MCTS, etc. (optional)
│
├── evals/
│   ├── run_eval.py           # Run prompt-based chatbot and evaluate responses
│   ├── metrics.py            # Accuracy, coherence, helpfulness, etc.
│   └── human_eval_samples/  # JSON/CSV sample conversations for eval
│
├── results/
│   ├── logs/                 # JSONL or TXT logs of optimization runs
│   └── comparisons/          # Comparisons of prompt variants and scores
│
├── notebooks/
│   └── analysis.ipynb        # Interactive EDA, visualizations of prompt quality
│
├── data/
│   ├── train_examples.json      # Main dataset for optimization/training
│   └── eval_examples.json       # (Optional) Separate eval set
│
└── app/
    ├── main.py               # Optional FastAPI or Streamlit app
    └── ui/                   # Web UI templates or frontend logic
