import json
import logging

from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template

from modules.audio_analysis import analyze_audio
from modules.data_integration import integrate_data
from modules.llm_integration import analyze_with_llm
from modules.text_analysis import analyze_text

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'audio' not in request.files or 'transcript' not in request.files:
            return jsonify({"error": "Both audio and transcript files are required"}), 400

        audio_file = request.files['audio']
        transcript = request.files['transcript'].read().decode('utf-8')
        # print the transcript
        #print("Transcript: " + transcript)

        audio_analysis = analyze_audio(audio_file)
        text_analysis = analyze_text(transcript)
        integrated_data = integrate_data(audio_analysis, text_analysis)

        # Log the integrated data for debugging
        logger.debug(f"Integrated data: {json.dumps(integrated_data, indent=2)}")

        llm_analysis_str = analyze_with_llm(integrated_data)

        # Parse the JSON string returned by analyze_with_llm
        llm_analysis = json.loads(llm_analysis_str)

        # Return the LLM analysis directly
        return jsonify(llm_analysis)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM analysis result")
        return jsonify({"error": "Invalid response from LLM analysis"}), 500
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        return jsonify({"error": "An error occurred during analysis"}), 500

if __name__ == '__main__':
    app.run(debug=True)