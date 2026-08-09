# AI ATS Resume System

An AI-powered Applicant Tracking System (ATS) resume analyzer — parses resumes,
scores them against job descriptions using a hybrid of classic NLP/ML and LLM-based
feedback, and gives candidates actionable suggestions to improve their match rate.

## Why hybrid?

Most ATS-checker projects go one of two shallow routes: pure keyword matching
(no semantic understanding) or a thin LLM wrapper (no real ML engineering).
This project combines both deliberately:

- **Lexical matching** (TF-IDF/BM25) — literal keyword overlap, the way real
  legacy ATS systems work today.
- **Semantic matching** (sentence embeddings) — understands paraphrases and
  synonyms a keyword search would miss.
- **Trained classifier** — predicts shortlist likelihood from labeled data.
- **LLM feedback layer** — turns raw scores into specific, human-readable advice.

## Status

🚧 Actively in development. See commit history for daily progress.

## Architecture

See `docs/architecture.md` (coming soon) for the full system design and
reasoning behind each component.

## Tech stack

- **Backend:** FastAPI, pdfplumber, python-docx, scikit-learn, sentence-transformers, spaCy
- **Frontend:** React
- **Data:** PostgreSQL + a vector store (Chroma/pgvector)
- **Deployment:** Docker, Render/Railway (backend), Vercel (frontend)

## Progress log

- Day 1: Text extraction (PDF/DOCX) + regex field extraction (email, phone) + rule-based section splitter
- Day 2: Lexical matching (TF-IDF + cosine similarity) and semantic matching (sentence embeddings) between resume and job description
- Day 3: Trained shortlist-prediction classifier (Logistic Regression, compared against Random Forest and Gradient Boosting) on engineered match features; combined lexical + semantic + classifier into a unified match report
- Day 4: LLM feedback module — turns match scores into specific, actionable suggestions, with an offline mock mode for development without an API key
- Day 5: Wired everything into a real FastAPI app (`/analyze`, `/health` endpoints), fixed an eager-model-loading bug that broke testability, added a test suite (health check + input validation run anywhere; full pipeline test requires network for the embedding model)
- Day 6: React frontend (Vite) — resume/JD input form calling the backend `/analyze` endpoint, score breakdown display, suggestions list. CORS configured on the backend so the two can actually talk to each other locally.
- Day 7: Auth + saved analysis history via Supabase (`/auth/signup`, `/auth/login`, `/history`) — gracefully returns a clean 501 until real Supabase credentials are added, rather than crashing
- Day 8: PDF report export (`/report/pdf`) using reportlab — verified real, valid PDF output; snippet-only history storage decided deliberately for privacy
