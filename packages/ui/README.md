# 🎓 Smart Tutor - Streamlit UI Package

Welcome to the **User Interface (UI) package** of the [Project Name] Smart Tutoring System. This package leverages [Streamlit](https://streamlit.io/) to provide a responsive, intuitive, and interactive web-based chat interface for human-chatbot tutoring sessions.

## 📖 Overview

This package serves as the frontend layer of the smart tutoring system. It handles all user interactions, displays the conversational history, renders educational content (including code and math equations), and communicates with the backend tutoring engine (LLMs, RAG models, etc.) to generate personalized responses.

## ✨ Features

* **Interactive Chat Interface:** Fluid, real-time messaging between the student and the AI tutor.
* **Rich Text Rendering:** Full support for Markdown, code snippets (syntax highlighting), and LaTeX (for math and science equations).
* **Modular Design:** Clean separation of UI components, state management, and backend API integration.

## 🚀 Usage

To start the Streamlit application, run the following command from within the `ui/` directory:

```bash
(export $(cat envs/ui.env | xargs) && cd packages/ui && uv run streamlit run src/ui/main.py)
```

By default, the application will be hosted locally at `http://localhost:8501`.

## 🔗 Integration with Core Project

This UI package is designed to be a lightweight presentation layer. It integrates with the core tutoring logic in one of two ways depending on your architecture:

1. **API-Driven (Recommended):** The UI uses `requests` or `httpx` in `utils/api_client.py` to send student messages to your FastAPI/Flask backend.
2. **Direct Import:** If this is a monolithic application, the UI imports the chatbot engine directly from the core project (e.g., `from core.tutor_engine import generate_response`).

*See `utils/api_client.py` to configure how the UI sends prompts and receives the AI tutor's responses.*

## 🎨 Customizing the UI

Streamlit's default theme can be customized. To change colors, fonts, or layout, you can edit the `.streamlit/config.toml` file or modify the custom CSS located in `assets/style.css`.

Example `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#4CAF50" # Green for education
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## 🤝 Contributing

When contributing to the UI package:
1. Ensure all new UI components are placed in the `components/` directory.
2. Avoid putting heavy business logic or AI processing directly into `app.py`. Delegate these tasks to the backend or utility functions.
3. Test your UI changes by running the Streamlit app locally before submitting a Pull Request.

---
*Built with ❤️ for better education using Streamlit.*