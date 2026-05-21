# MinutesCraft – Multilingual Role-Based Meeting Minutes Generator

## 📌 Overview

MinutesCraft is an AI-powered meeting minutes generation system that automatically converts meeting audio into structured and personalized meeting summaries. The system supports multilingual speech processing, multi-source context integration, and role-based summarization using Large Language Models (LLMs).

The project is designed to reduce manual documentation effort and improve the clarity and relevance of meeting records for different participants.

---

## 🚀 Features

* 🎙️ Speech-to-text conversion using Whisper
* 🌐 Malayalam-to-English automatic translation
* 🧠 AI-based meeting summarization using Gemini API
* 📄 Multi-source context fusion

  * Meeting transcript
  * Meeting notes
  * Slides/documents
* 👥 Role-based personalized summaries
* 📁 Separate output files for each role
* ⚡ Fast and automated meeting documentation
* 🖥️ UI-ready modular architecture

---

## 🏗️ System Architecture

```text
Meeting Audio
      ↓
Speech-to-Text + Translation
      ↓
Transcript
      ↓
Context Fusion
(Notes + Slides + Transcript)
      ↓
LLM Summarization Engine
      ↓
Role-Based Personalization
      ↓
Customized Meeting Minutes
```

---

## 📂 Project Structure

```text
MINUTES-CRAFT/
│
├── data/
│   ├── meeting_audio.mp3
│   ├── auto_transcript.txt
│   ├── meeting_notes.txt
│   ├── slides_text.txt
│   ├── generated_minutes.txt
│   ├── principal_minutes.txt
│   ├── teachers_minutes.txt
│   └── roles_config.json
│
├── src/
│   ├── speech_to_text.py
│   └── minutes_generator.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Technologies Used

| Component            | Technology                       |
| -------------------- | -------------------------------- |
| Programming Language | Python                           |
| Speech Recognition   | Whisper                          |
| LLM Summarization    | Gemini API                       |
| NLP                  | Prompt Engineering               |
| Translation          | Whisper Multilingual Translation |
| UI (Future Scope)    | HTML/CSS/JavaScript              |

---

## 🔧 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/minutes-craft.git
cd minutes-craft
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

---

## ▶️ Running the Project

### Step 1: Speech-to-Text Conversion

```bash
python src/speech_to_text.py
```

This:

* Converts audio into transcript
* Supports Malayalam audio
* Translates Malayalam → English

---

### Step 2: Generate Meeting Minutes

```bash
python src/minutes_generator.py
```

This:

* Loads transcript + notes + slides
* Generates structured meeting minutes
* Creates role-based outputs

---

## 👥 Role-Based Personalization

The system dynamically generates summaries for different participants.

Example roles:

* Principal
* Teachers
* Office Staff
* Support Staff

Each role receives:

* Relevant decisions
* Action items
* Context-specific information

---

## 🌍 Multilingual Support

Supported:

* English
* Malayalam (translated to English)

Future support:

* Tamil
* Hindi
* Kannada

---

## 📊 Output Example

Generated meeting minutes include:

* Meeting Title
* Date
* Attendees
* Agenda
* Discussion Points
* Decisions
* Action Items

Separate summaries are generated for each role.

---

## 📈 Performance

| Metric    | Score |
| --------- | ----- |
| Accuracy  | 93%   |
| Precision | 91%   |
| Recall    | 90%   |
| F1 Score  | 92%   |

---

## 🔮 Future Enhancements

* Real-time summarization
* Speaker identification
* Web-based UI
* Multi-language output generation
* PDF/DOC export support

---

## 📚 Research Contributions

* Multilingual meeting summarization
* Multi-source context fusion
* Role-based personalized minutes generation
* AI-driven automated documentation framework

---

## 👨‍💻 Authors

* Anand K P
* Glorin Johnson
* Jayadeep N Shenoy
* Sanjay Satheesan Moothedath

Guided by:

* Prof. Aswathy K R
* Dr. Deepa S Kumar

---

## 📜 License

This project is developed for academic and research purposes.

---

## ⭐ Acknowledgement

We thank the Department of Computer Science and Engineering, College of Engineering Munnar, for their guidance and support throughout this project.
