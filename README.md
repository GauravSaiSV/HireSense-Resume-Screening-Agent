# HireSense — Resume Screening Agent

HireSense is an AI-powered resume screening agent that analyzes resumes against a job description and ranks candidates based on their suitability.

It uses **Google Gemini** to extract structured information from resumes and job descriptions, followed by deterministic matching and scoring for skills, experience, education, and projects.

## Features

* Resume and job description analysis
* PDF, DOCX, and TXT support
* Required and preferred skill matching
* Experience and education matching
* Project relevance scoring
* Candidate ranking
* Explainable score breakdown
* Multiple resume screening
* Streamlit web interface

## Tech Stack

* Python 3.12
* Google Gemini API
* google-genai
* Pydantic
* Streamlit
* PyMuPDF
* python-docx
* pytest

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GauravSaiSV/HireSense-Resume-Screening-Agent.git
cd HireSense-Resume-Screening-Agent
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## API Key Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

Replace `your_gemini_api_key_here` with your Gemini API key.

**Do not commit `.env` or your API key to GitHub.**

---

## Run the Agent

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the URL shown in the terminal, usually:

```text
http://localhost:8501
```

### End-to-End Usage

1. Upload a job description.
2. Upload one or more resumes.
3. Start the screening process.
4. HireSense extracts the information using Gemini.
5. Candidates are matched and scored.
6. Candidates are ranked from highest to lowest score.

Supported files:

* PDF
* DOCX
* TXT

---

## Scoring

Candidates are scored using:

| Component        | Weight |
| ---------------- | -----: |
| Required Skills  |    40% |
| Preferred Skills |    15% |
| Experience       |    20% |
| Education        |    10% |
| Projects         |    15% |

The result includes the final score, matched skills, missing skills, and individual score components.

---

## Design Choices

### Hybrid LLM + Deterministic Approach

Gemini is used for extracting structured information from unstructured documents.

The final matching and ranking are handled using deterministic Python logic.

```text
Resume / Job Description
          ↓
     Text Extraction
          ↓
    Gemini Extraction
          ↓
 Structured Profiles
          ↓
 Deterministic Matching
          ↓
    Weighted Scoring
          ↓
   Candidate Ranking
```

This approach makes the results easier to **test, explain, debug, and reproduce**.

---

## Tradeoffs & Limitations

* Gemini API access is required.
* API limits may affect large screening runs.
* Matching depends on the defined skill vocabulary and aliases.
* No embedding-based semantic similarity is currently used.
* Experience calculation depends on clearly stated employment dates.
* Scoring weights are manually defined.
* Unusual resume layouts may affect extraction quality.
* Results are intended as decision-support, not autonomous hiring decisions.

---

## Testing

Run the automated tests with:

```bash
pytest
```

Current test suite:

```text
44 passed
```

Tests cover parsing, skill matching, education, experience, project matching, scoring, ranking, and agent integration.

---

## Sample Data

Sample job-description data is available in:

```text
data/JD/
```

The application supports multiple resumes for a single job description.

---

## Project Structure

```text
HireSense-Resume-Screening-Agent/
├── data/
├── src/
│   ├── agent/
│   ├── matching/
│   ├── scoring/
│   ├── extractor.py
│   ├── gemini_client.py
│   ├── models.py
│   └── parser.py
├── tests/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Repository

https://github.com/GauravSaiSV/HireSense-Resume-Screening-Agent
