# Empathy Analyzer

Empathy Analyzer is a web application that uses AI to analyze audio recordings and transcripts for empathy and communication style. It provides insights on empathy levels, tone, and offers suggestions for improvement.

## Features

- Audio and transcript analysis
- Integration with Claude 3.5 Sonnet AI for advanced language understanding
- Simple web interface for file upload and result display
- Detailed feedback on empathy level, tone, and areas for improvement

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10 or higher
- pip (Python package manager)
- An Anthropic API key for Claude 3.5 Sonnet

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/empathy-analyzer.git
   cd empathy-analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask server:
   ```
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Use the web interface to upload an audio file and its corresponding transcript.

4. Click "Analyze" to process the files and view the results.

## Project Structure

```
empathy_analyzer/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this file)
├── README.md               # This file
├── templates/
│   └── index.html          # Frontend HTML
└── modules/
    ├── audio_analysis.py   # Audio processing module
    ├── text_analysis.py    # Text analysis module
    ├── data_integration.py # Data integration module
    ├── llm_integration.py  # LLM (Claude) integration module
    └── feedback_generation.py # Feedback generation module
```

## Contributing

Contributions to the Empathy Analyzer project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project uses the following license: [MIT License](https://opensource.org/licenses/MIT).

## Contact

If you want to contact me, you can reach me at `your_email@example.com`.

## Acknowledgements

- [Anthropic](https://www.anthropic.com) for providing the Claude 3.5 Sonnet AI model
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [librosa](https://librosa.org/) for audio analysis
- [NLTK](https://www.nltk.org/) for text analysis