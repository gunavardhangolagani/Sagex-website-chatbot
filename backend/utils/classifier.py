# utils/intent_classifier.py
import re

STATIC_INTENTS = {
    "greetings": {
        "keywords": [r"^\s*hi\s*$", r"^\s*hello\s*$", r"^\s*hey\s*$", r"how are you", r"good morning", r"good afternoon"],
        "answer": "Hello! 👋 I am the Sagex assistant. How can I help you today?"
    },
    "services": {
        "keywords": [r"\bservices\b", r"\bwhat do you do\b", r"\boffer\b", r"\bwhat does sagex do\b"],
        "answer": "**Company Overview & Services**\n\nSagex specializes in three core areas:\n* **Web Development:** High-performance, secure websites optimized with results-driven SEO.\n* **Software Development:** Custom software, scalable backend systems, and API integrations.\n* **Engineering Services:** Precise 2D drafting, advanced 3D modeling, and photorealistic renderings."
    },
    "contact": {
        "keywords": [r"\bcontact\b", r"\blocation\b", r"\baddress\b", r"\bphone\b", r"\bemail\b", r"\breach\b", r"\bwhere is\b"],
        "answer": "**Contact Information**\n\nWe would love to hear from you! You can reach our support team here:\n* **Phone:** +91 8688918144\n* **Email:** support@sagex.io\n* **Office:** Sripada Diamond Towers, Dwaraka Nagar, Visakhapatnam - 530016."
    },
    "portfolio": {
        "keywords": [r"\bpast work\b", r"\bportfolio\b", r"\bcase studies\b", r"\bexamples\b", r"\bprojects\b"],
        "answer": "**Our Past Work & Case Studies**\n\nWe have successfully delivered solutions across various industries:\n* **Citi Neuro Centre (Healthcare):** SEO-optimized platform with online appointment booking.\n* **Perspect.AI (Technology):** UI/UX overhaul for high-converting lead generation.\n* **Jumper (App Development):** High-speed, low-latency B2C video commerce app."
    },
    "why_us": {
        "keywords": [r"\bwhy sagex\b", r"\bchoose sagex\b", r"\bwhy choose you\b", r"\bstand out\b"],
        "answer": "**Why Choose Sagex?**\n\nWe leverage over 20 years of combined team expertise. We stand out by offering:\n* **Smart Investments:** Scalable tools that reduce costs.\n* **Cutting-Edge Tech:** Modern frameworks built to industry standards.\n* **Tailored Expertise:** Custom solutions designed for your specific industry."
    },
    "industries": {
        "keywords": [r"\bindustries\b", r"\bsectors\b", r"\bwho do you serve\b", r"\bwho do you work with\b"],
        "answer": "**Supported Industries**\n\nOur expertise spans across 5+ diverse sectors, including:\n* Industry & Manufacturing\n* Healthcare\n* Technology & AI\n* Home & Living\n* Transportation, Logistics, and Fintech"
    },
    "onboarding": {
        "keywords": [r"\bprocess\b", r"\bget started\b", r"\bonboarding\b", r"\bhappens next\b"],
        "answer": "**Our Consultation Process**\n\nHere is what happens when you partner with us:\n1. **Schedule:** We arrange a call at your convenience.\n2. **Discovery:** We conduct an in-depth call to understand your business challenges.\n3. **Proposal:** We prepare a detailed proposal outlining technologies, timelines, and strategies."
    },
    "irrelevant": {
        "keywords": [r"\d+\s*[\+\-\*\/]\s*\d+", r"\bmath\b", r"\bcalculate\b", r"\bweather\b"],
        "answer": "I am the Sagex assistant, and I'm here to help with your technology and engineering inquiries. I don't handle general calculations or external topics. How can I help you with our services today?"
    },
    "small_talk": {
        "keywords": [r"joke", r"story", r"opinion on", r"what do you think"],
        "answer": "I'm strictly programmed to be the best technology and engineering consultant I can be!  Shall we talk about our projects instead?"
    }
}

def get_static_intent_response(question: str):
    """
    Checks if the user query matches any static intent keywords.
    Returns the static answer if a match is found, otherwise returns None.
    """
    question_lower = question.lower()
    
    for intent, data in STATIC_INTENTS.items():
        for keyword in data["keywords"]:
            if re.search(keyword, question_lower):
                return data["answer"]
                
    return None