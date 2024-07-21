import json
from modules.logger import setup_logger

logger = setup_logger('feedback_generation_logger', 'logs/feedback_generation.log')

def generate_feedback(analysis_result):
    """
    Generate user-friendly feedback based on the analysis results.

    :param analysis_result: Dict containing the results of audio and text analysis, or a JSON string
    :return: Dict containing feedback messages
    """
    logger.info("Starting feedback generation")
    feedback = {}

    try:
        # Check if analysis_result is a string, if so, try to parse it as JSON
        if isinstance(analysis_result, str):
            try:
                analysis_result = json.loads(analysis_result)
            except json.JSONDecodeError:
                logger.error("Failed to parse analysis_result as JSON")
                return {"error": "Invalid analysis result format"}

        # Check if analysis_result is now a dictionary
        if not isinstance(analysis_result, dict):
            logger.error(f"analysis_result is not a dictionary: {type(analysis_result)}")
            return {"error": "Invalid analysis result format"}

        # Empathy level feedback
        empathy_level = analysis_result.get('empathy_level', 'medium')
        feedback['empathy'] = get_empathy_feedback(empathy_level)

        # Tone feedback
        tone = analysis_result.get('tone_analysis', 'neutral')
        feedback['tone'] = get_tone_feedback(tone)

        # Communication style feedback
        feedback['communication_style'] = get_communication_style_feedback(analysis_result)

        # Improvement suggestions
        feedback['suggestions'] = get_improvement_suggestions(analysis_result)

        logger.info("Feedback generation completed successfully")
        return feedback

    except Exception as e:
        logger.error(f"Error during feedback generation: {str(e)}")
        return {"error": "An error occurred while generating feedback"}

def get_empathy_feedback(empathy_level):
    if empathy_level == 'high':
        return "Your communication shows a high level of empathy. Great job connecting with others!"
    elif empathy_level == 'medium':
        return "You're showing a moderate level of empathy. There's room for improvement in connecting more deeply with others."
    else:
        return "Your communication could benefit from expressing more empathy. Try to put yourself in the other person's shoes."

def get_tone_feedback(tone):
    return f"Your tone appears to be {tone}. Consider if this aligns with your intended message and audience."

def get_communication_style_feedback(analysis_result):
    # This is a placeholder. In a real implementation, you'd analyze various aspects of the communication style.
    return "Your communication style is clear and direct. Consider varying your approach based on your audience and context."

def get_improvement_suggestions(analysis_result):
    suggestions = []

    # These are placeholder suggestions. In a real implementation, you'd base these on specific analysis results.
    if analysis_result.get('empathy_level') != 'high':
        suggestions.append("Practice active listening and try to understand the other person's perspective.")

    if analysis_result.get('speech_rate', 0) > 150:  # words per minute
        suggestions.append("Consider slowing down your speech rate for better clarity.")

    if analysis_result.get('pause_count', 0) < 5:
        suggestions.append("Try incorporating more pauses in your speech. This can help emphasize key points and allow your audience to process information.")

    return suggestions