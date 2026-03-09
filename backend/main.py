from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# IMPORTANT: To use a real AI, uncomment these lines and configure your API key
# import google.generativeai as genai
# import os
# genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
# model = genai.GenerativeModel('gemini-pro')

app = FastAPI(title="DentAssist API")

# Enable CORS for the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your actual website URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic system prompt for the AI
SYSTEM_PROMPT = """
You are DentAssist, a warm and professional AI dental assistant for Navadiya Dental Clinic in Surat, Gujarat.

[... Full Prompt omitted in this basic mock. In a real AI implementation, 
this prompt would be passed as a system instruction to the LLM ...]

Tone: Warm, friendly, reassuring — never cold or robotic.
Language: STRICTLY ENGLISH ONLY. Do not use Hindi or Hinglish.
NEVER diagnose — always say "Please consult with the doctor to confirm."
"""

class Message(BaseModel):
    role: str # 'user' or 'bot'
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []

@app.get("/")
def health_check():
    return {"status": "ok", "message": "DentAssist API is running!"}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    user_msg = request.message.lower()
    
    # ==========================================
    # --- REAL AI IMPLEMENTATION (GEMINI EXAMPLE) ---
    # ==========================================
    # try:
    #     # Convert history to Gemini format (example)
    #     chat = model.start_chat()
    #     response = chat.send_message(f"SYSTEM: {SYSTEM_PROMPT}\nUSER: {user_msg}")
    #     return {"reply": response.text}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # ==========================================
    
    # ==========================================
    # --- MOCK LOGIC FOR DEMONSTRATION ---
    # Since we need to run this instantly without an API key, 
    # here is a simple mock logic based on the user's intent.
    # ==========================================
    reply = "I'm sorry, I didn't quite catch that. How can I help you? (Note: This is a demo backend. Please connect your AI API for dynamic responses!)"
    
    if any(word in user_msg for word in ["appointment", "book", "schedule", "visit"]):
        reply = "Sure! May I know your name first? 😊"
    elif any(word in user_msg for word in ["severe pain", "swelling", "bleeding", "broken", "accident"]):
        reply = "This sounds like an emergency! 🚨 Please call us immediately at: 📞 +91-98765-43210. Dr. Sharma is available to help. Please don't panic, we are here for you!"
    elif any(word in user_msg for word in ["cost", "price", "fee", "how much"]):
        if "cleaning" in user_msg:
            reply = "A regular checkup and cleaning costs approximately ₹500–₹800. Prevention is better than cure! Would you like to schedule a visit?"
        elif "root canal" in user_msg or "rct" in user_msg:
            reply = "Root Canal Treatment (RCT) costs approximately ₹3,000–₹6,000 per tooth. Shall I book an appointment for you?"
        else:
            reply = "Treatment costs vary depending on the procedure. For example, fillings are ₹800–₹1,500, and cleaning is ₹500–₹800. Do you have a specific treatment in mind?"
    elif any(word in user_msg for word in ["time", "hours", "open", "saturday"]):
        reply = "We are open Monday–Saturday, from 10:00 AM to 7:00 PM. We are closed on Sundays! ⏰"
    elif any(word in user_msg for word in ["where", "address", "location"]):
        reply = "Our clinic is located at 304, Sunshine Plaza, Ring Road, Surat, Gujarat. There's free parking available! 🚗"
    elif "hurt" in user_msg or "painless" in user_msg or "pain" in user_msg:
        reply = "A regular checkup is completely painless! For procedures like RCT, anesthesia is provided so you won't feel any pain. 😊"
    elif "hello" in user_msg or "hi" in user_msg or "hey" in user_msg:
        reply = "Hello! 👋 I am DentAssist, the AI assistant for Navadiya Dental Clinic. How can I help you today? 🦷"
        
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    # Run development server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
