# Smritify - Study-Focused Mobile Application

Smritify is a mobile application designed to help students avoid distractions from social media platforms like Instagram Reels and YouTube Shorts. Instead of watching videos, students can scroll through their study questions in a similar interface.

## Features

- **Reels-style Study Mode**: Scroll through questions in a familiar interface
- **Interactive Learning**: Swipe right to reveal answers
- **Question Management**: Add, bookmark, and mark questions as understood
- **AI Integration**: Generate answers using ChatGPT API
- **Subject Filtering**: Organize questions by subject
- **Bookmark System**: Save important questions for later review

## Technology Stack

- **Frontend**: Kivy (Python)
- **Backend**: SQLite
- **AI Integration**: OpenAI ChatGPT API
- **Deployment**: Android (using Kivy framework)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smritify.git
cd smritify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application file
- `database.py`: Database management module
- `ai_integration.py`: ChatGPT API integration
- `requirements.txt`: Project dependencies
- `smritify.db`: SQLite database file

## Usage

1. Launch the app
2. Start scrolling through questions
3. Swipe right to reveal answers
4. Use the bottom-right icons to:
   - Bookmark important questions
   - Generate AI answers
   - Mark questions as understood

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 