from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import traceback
from datetime import datetime

# ✅ Load .env from parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# ✅ Get Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env file.")

# ✅ Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Load the free Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)

# ✅ Gemini chat logic
def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Gemini API error:", e)
        print(traceback.format_exc())
        return "Sorry, I couldn't respond right now. Please try again later."

# ✅ Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    user_name = data.get("user_name", "User")

    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    prompt = f"""Act as a kind and helpful mental health assistant named MindEase.
Respond gently to this message from {user_name}:
{user_message}

Keep your response professional but warm, and try to ask open-ended questions 
to encourage the user to share more about their feelings."""

    ai_response = query_gemini(prompt)
    return jsonify({
        "response": ai_response,
        "timestamp": datetime.now().isoformat()
    })

# ✅ Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(debug=True, host="0.0.0.0", port=port)
