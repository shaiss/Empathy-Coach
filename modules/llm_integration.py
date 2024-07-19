import json

from anthropic import Anthropic


def analyze_with_llm(integrated_data):
    client = Anthropic()
    #print(integrated_data)

    # Ensure integrated_data is a dictionary
    if isinstance(integrated_data, str):
        try:
            integrated_data = json.loads(integrated_data)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON string provided"}

    # Convert integrated_data to a formatted JSON string for the prompt
    data_str = json.dumps(integrated_data, indent=2)
    #print("data_str " + data_str)

    #prompt = "you are an expert in audio analysis and text analysis. your task is to analyze the following data and provide insights and suggestions for improvement"

    prompt = f"""
    You are an AI assistant specialized in analyzing communication data, including both audio and text features. Please analyze the following integrated data from an audio recording and its transcript:

{data_str}

Before you begin your analysis, here's an explanation of some of the audio features:
Audio features:
1. MFCCs (Mel-frequency cepstral coefficients): Represent the short-term power spectrum of a sound.
2. Spectral Centroid: Indicates where the "center of mass" of the spectrum is.
3. Spectral Rolloff: Represents the frequency below which a certain percentage of the total spectral energy lies.
4. Tempo: The speed or pace of the speech.
5. Pitch mean and variability: Reflect the average pitch and how much it varies.
6. Energy mean and variability: Reflect the overall loudness and its changes.
7. Speech rate: The number of syllables per second.
8. Pauses: The number and duration of pauses.
9. Voice quality (HNR): Harmonics-to-Noise Ratio.
10. Formants: Frequencies that characterize different vowel sounds.

Text features:
1. Sentiment analysis: Measures the overall sentiment (positive, negative, neutral) of the text.
2. Word count and unique words: Indicate the length and vocabulary diversity of the speech.
3. Top words: Most frequently used words in the speech.
4. Emotion analysis: Counts of words associated with different emotions.
5. Readability scores: Indicate the complexity and readability of the text.
6. Sentence analysis: Provides insights into sentence structure and complexity.
7. Named entities: Identifies and categorizes named entities mentioned in the speech.
8. Lexical diversity: Measures the variety of words used relative to the total word count.

Carefully review the data above and follow these steps:

1. Analyze the speaker's tone:
   - Consider the choice of words, sentence structure, and any audio cues provided.
   - Determine if the tone is formal, informal, friendly, serious, enthusiastic, etc.

2. Assess the speaker's sentiment:
   - Evaluate whether the sentiment is positive, negative, or neutral.
   - Look for emotional indicators in the language used and any mentioned audio cues.

3. Gauge the level of empathy:
   - Identify instances where the speaker shows understanding or consideration for others' feelings.
   - Assess how well the speaker relates to or acknowledges the listener's perspective.

4. Identify key points:
   - Extract the main ideas or arguments presented by the speaker.
   - Focus on recurring themes or emphasized information.

5. Act as a speech and communication coach and suggest speech areas for improvement:
   - Based on your analysis, identify aspects of the speaker's communication that could be enhanced.
   - Consider elements such as clarity, tone, phonetic content, and most cruitically emotional intelligence.

After completing your analysis, format your response as a JSON object with the following structure:

{{
  "tone_analysis": "String describing the overall tone",
  "sentiment_analysis": "String describing the sentiment",
  "empathy_level": "String describing the level of empathy displayed by the speaker",
  "key_points": ["Array of strings, each representing a key point"],
  "improvement_areas": ["Array of strings, each suggesting an area for improvement"]
}}

Ensure that your analysis is thorough and based solely on the provided data. Do not make assumptions beyond what is explicitly stated or strongly implied in the input. If certain aspects are unclear or cannot be determined from the given information, indicate this in your analysis.
"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
              max_tokens=1000,
              temperature=0.7,
              messages=[{
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": prompt
                      }
                  ]
              }])

        # Extract the text content from the response
        response_text = response.content[0].text
        print("response: " + response_text)

        # Find the JSON object within the response text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]

        # Parse the JSON string
        analysis = json.loads(json_str)
        return json_str


    except json.JSONDecodeError:
        # Handle case where the response is not valid JSON
        return json.dumps({
            "error": "Failed to parse LLM response",
            "raw_response": response.content[0].text
        })
    except Exception as e:
        # Handle any other exceptions
        return {"error": f"An error occurred: {str(e)}"}
