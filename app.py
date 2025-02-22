from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import random
from googletrans import Translator

app = Flask(__name__)

# Expanded dictionary mapping common diseases to their symptoms and remedies (40+ diseases)
disease_info = {
    "Flu": {
         "symptoms": ["fever", "body ache", "chills"],
         "remedy": "Drink plenty of fluids, rest, and use over-the-counter fever reducers."
    },
    "Common Cold": {
         "symptoms": ["cough", "runny nose", "sneezing","fever"],
         "remedy": "Stay hydrated, rest, and use decongestants or saline nasal spray."
    },
    "Strep Throat": {
         "symptoms": ["sore throat", "fever", "difficulty swallowing","tinyred spots on thr roof of thr mouth"],
         "remedy": "Consult a doctor for antibiotics; gargle with warm salt water."
    },
    "Migraine": {
         "symptoms": ["headache", "nausea", "sensitivity to light"],
         "remedy": "Lie down in a dark room and take pain relievers or migraine-specific medications."
    },
    "Asthma": {
         "symptoms": ["shortness of breath", "wheezing", "chest tightness"],
         "remedy": "Use inhalers as prescribed; avoid triggers and follow a doctor-approved action plan."
    },
    "Diabetes": {
         "symptoms": ["frequent urination","excessive thirst", "blurry vision", "fatigue","loss weight"],
         "remedy": "Monitor blood sugar, follow a balanced diet, and exercise regularly."
    },
    "Hypertension": {
         "symptoms": ["headache", "dizziness", "chest pain"],
         "remedy": "Monitor blood pressure, reduce salt intake, and consult a doctor for medications."
    },
    "Arthritis": {
         "symptoms": ["joint pain", "swelling", "stiffness"],
         "remedy": "Use anti-inflammatory medications, exercise regularly, and maintain a healthy weight."
    },
    "Gastroenteritis": {
         "symptoms": ["vomiting", "diarrhea", "stomach pain"],
         "remedy": "Stay hydrated, consume bland foods, and seek medical help if severe."
    },
    "Urinary Tract Infection": {
         "symptoms": ["burning urination", "frequent urination", "lower abdominal pain"],
         "remedy": "Increase water intake and consult a doctor for antibiotics if necessary."
    },
    "Depression": {
         "symptoms": ["sadness", "loss of interest", "fatigue"],
         "remedy": "Seek professional help, consider therapy, and possibly medication."
    },
    "Anxiety": {
         "symptoms": ["restlessness", "rapid heartbeat", "sweating"],
         "remedy": "Practice relaxation techniques, consider therapy, and consult a doctor if needed."
    },
    "Pneumonia": {
         "symptoms": ["cough", "fever", "difficulty breathing"],
         "remedy": "Seek medical attention; treatment may involve antibiotics and supportive care."
    },
    "Bronchitis": {
         "symptoms": ["cough", "mucus production", "fatigue"],
         "remedy": "Rest, increase fluid intake, and use a humidifier. Consult a doctor if symptoms worsen."
    },
    "Sinusitis": {
         "symptoms": ["facial pain", "nasal conges                tion", "headache"],
         "remedy": "Apply warm compresses, use saline nasal sprays, and consider decongestants."
    },
    "Allergic Rhinitis": {
         "symptoms": ["sneezing", "runny nose", "itchy eyes"],
         "remedy": "Avoid allergens and use antihistamines or nasal sprays as needed."
    },
    "Otitis Media": {
         "symptoms": ["ear pain", "fever", "difficulty hearing"],
         "remedy": "Consult a doctor; treatment may include antibiotics or pain relievers."
    },
    "Conjunctivitis": {
         "symptoms": ["red eyes", "itching", "discharge from eyes"],
         "remedy": "Maintain eye hygiene and consult an eye specialist if symptoms persist."
    },
    "Eczema": {
         "symptoms": ["itchy skin", "red rash", "dry patches"],
         "remedy": "Keep the skin moisturized and avoid irritants; use topical creams as directed."
    },
    "Psoriasis": {
         "symptoms": ["red patches", "scaly skin", "itching"],
         "remedy": "Use medicated creams and consult a dermatologist for specialized treatment."
    },
    "Chickenpox": {
         "symptoms": ["fever", "itchy rash", "blisters"],
         "remedy": "Keep the skin clean, avoid scratching, and use calamine lotion to ease itching."
    },
    "Measles": {
         "symptoms": ["fever", "rash", "cough"],
         "remedy": "Supportive care with hydration and rest; seek medical advice for complications."
    },
    "Mumps": {
         "symptoms": ["swollen glands", "fever", "headache"],
         "remedy": "Rest, hydrate, and use pain relievers; consult a doctor if severe."
    },
    "Tuberculosis": {
         "symptoms": ["persistent cough", "weight loss", "night sweats"],
         "remedy": "Requires long-term antibiotic treatment under medical supervision."
    },
    "Hepatitis A": {
         "symptoms": ["jaundice", "fatigue", "abdominal pain"],
         "remedy": "Supportive care with rest and hydration; most cases resolve on their own."
    },
    "Hepatitis B": {
         "symptoms": ["jaundice", "abdominal pain", "joint pain"],
         "remedy": "Consult a doctor; treatment may include antiviral medications."
    },
    "Kidney Infection": {
         "symptoms": ["back pain", "fever", "urinary discomfort"],
         "remedy": "Seek medical care; antibiotics are usually prescribed."
    },
    "Urinary Stones": {
         "symptoms": ["severe flank pain", "nausea", "blood in urine"],
         "remedy": "Increase water intake and consult a doctor for possible intervention."
    },
    "Coronary Artery Disease": {
         "symptoms": ["chest pain", "shortness of breath", "fatigue"],
         "remedy": "Lifestyle changes and medications; consult a cardiologist."
    },
    "Stroke": {
         "symptoms": ["sudden weakness", "confusion", "difficulty speaking"],
         "remedy": "Immediate emergency care is essential; rehabilitation may follow."
    },
    "Peripheral Artery Disease": {
         "symptoms": ["leg pain", "numbness", "cold feet"],
         "remedy": "Exercise, medication, and sometimes surgical procedures are recommended."
    },
    "Dementia": {
         "symptoms": ["memory loss", "confusion", "difficulty with tasks"],
         "remedy": "Supportive care, cognitive therapies, and medications may help manage symptoms."
    },
    "Parkinson's Disease": {
         "symptoms": ["tremors", "rigidity", "slowed movements"],
         "remedy": "Medications and physical therapy can help manage symptoms."
    },
    "Hypothyroidism": {
         "symptoms": ["fatigue", "weight gain", "cold intolerance"],
         "remedy": "Thyroid hormone replacement therapy under medical supervision."
    },
    "Hyperthyroidism": {
         "symptoms": ["weight loss", "rapid heartbeat", "anxiety"],
         "remedy": "Consult an endocrinologist; treatment may include antithyroid medications."
    },
    "Gout": {
         "symptoms": ["sudden joint pain", "redness", "swelling"],
         "remedy": "Avoid trigger foods and take medications as prescribed by a doctor."
    },
    "Irritable Bowel Syndrome (IBS)": {
         "symptoms": ["abdominal pain", "bloating", "irregular bowel movements"],
         "remedy": "Dietary changes and stress management can help alleviate symptoms."
    },
    "Crohn's Disease": {
         "symptoms": ["diarrhea", "abdominal pain", "weight loss"],
         "remedy": "Medical treatment includes anti-inflammatory drugs and dietary adjustments."
    },
    "Ulcerative Colitis": {
         "symptoms": ["bloody diarrhea", "abdominal pain", "cramps"],
         "remedy": "Management includes medication and sometimes surgery under doctor supervision."
    },
    "Iron-Deficiency Anemia": {
         "symptoms": ["fatigue", "pale skin", "shortness of breath"],
         "remedy": "Increase iron intake through diet or supplements and consult a doctor."
    },
    "Obesity": {
         "symptoms": ["excess body weight", "fatigue", "joint pain"],
         "remedy": "Adopt a balanced diet, exercise regularly, and consult healthcare providers for guidance."
    },
    "stomach upset": {
         "symptoms": ["stomach pain", "fatigue", "bloating"],
         "remedy": "Adopt a balanced diet, exercise regularly, and consult healthcare providers for guidance."
    }
}

# Store user symptoms in memory
user_symptoms = []

# Translator instance for Tamil/English conversion
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_symptom', methods=['POST'])
def add_symptom():
    data = request.json
    symptom = data.get("symptom", "")
    if symptom.strip():
        # Convert symptom to lower-case for easier matching
        user_symptoms.append(symptom.strip().lower())
        return jsonify({"message": f"Symptom '{symptom}' added."}), 200
    return jsonify({"error": "Invalid symptom"}), 400

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    lang = data.get("lang", "en")
    disease_match = {}
    
    # Process and translate symptoms if necessary
    processed_symptoms = []
    for symptom in user_symptoms:
        if lang == "ta":
            translated = translator.translate(symptom, src='ta', dest='en').text.lower()
        else:
            translated = symptom.lower()
        processed_symptoms.append(translated)
    
    # Score each disease based on how many of its symptoms match the user symptoms
    for disease, info in disease_info.items():
        match_count = sum(1 for s in info["symptoms"] if s in processed_symptoms)
        disease_match[disease] = match_count

    # Determine the disease with the highest symptom match count
    best_match = max(disease_match, key=disease_match.get)
    if disease_match[best_match] == 0:
        final_text = "Predicted Disease: Unknown\nRemedy: Consult a doctor."
    else:
        final_text = f"Predicted Disease: {best_match}\nRemedy: {disease_info[best_match]['remedy']}"
    
    # Clear symptoms after diagnosis
    user_symptoms.clear()

    if lang == "ta":
        final_text = translator.translate(final_text, src='en', dest='ta').text
    return jsonify({"result": final_text})

@app.route('/voice_response', methods=['POST'])
def voice_response():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")
    if text.strip():
        tts = gTTS(text=text, lang=lang)
        filename = "static/response.mp3"
        tts.save(filename)
        return jsonify({"audio": filename}), 200
    return jsonify({"error": "Invalid text"}), 400

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(port=5000, debug=True)
