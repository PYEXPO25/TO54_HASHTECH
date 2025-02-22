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
    },
     "Acne Vulgaris": {
         "symptoms": ["pimples", "blackheads", "whiteheads", "oily skin"],
         "remedy": "Use topical retinoids, benzoyl peroxide, and/or antibiotics as needed."
    },
    "Cystic Acne": {
         "symptoms": ["painful, deep cysts", "severe inflammation", "redness"],
         "remedy": "Consult a dermatologist for isotretinoin therapy and possible drainage."
    },
    "Hormonal Acne": {
         "symptoms": ["breakouts around the chin and jawline", "recurring lesions", "oily skin"],
         "remedy": "Consider hormonal treatments such as oral contraceptives and anti-androgens."
    },
    "Acne Rosacea": {
         "symptoms": ["persistent facial redness", "papules", "visible blood vessels"],
         "remedy": "Use topical metronidazole and oral tetracyclines; avoid triggers like spicy food."
    },
    "Acne Conglobata": {
         "symptoms": ["severe, interconnected nodules", "abscesses", "scarring"],
         "remedy": "Often treated with isotretinoin combined with systemic corticosteroids."
    },
    "Acne Mechanica": {
         "symptoms": ["acne in areas of friction", "papules", "localized inflammation"],
         "remedy": "Reduce friction (e.g., adjust sports gear) and use appropriate topical treatments."
    },
    "Acne Fulminans": {
         "symptoms": ["sudden onset of painful nodules", "systemic symptoms such as fever"],
         "remedy": "Requires systemic corticosteroids and isotretinoin under close medical supervision."
    },
    "Acne Inversa": {
         "symptoms": ["deep, painful nodules", "abscesses in axillae or groin"],
         "remedy": "Often managed with antibiotics, biologics, or surgical interventions."
    },
    "Acne Excoriée": {
         "symptoms": ["excoriated lesions", "inflamed papules", "scarring due to picking"],
         "remedy": "Focus on gentle skincare, behavioral therapy, and topical treatments to reduce urge to pick."
    },
    "Infantile Acne": {
         "symptoms": ["small papules and pustules on the face of infants"],
         "remedy": "Usually self-resolving; use gentle cleansers and consult pediatric advice if severe."
    },
     
    "Polycystic Ovary Syndrome (PCOS)": {
        "symptoms": ["irregular periods", "excess hair growth", "acne", "weight gain"],
        "remedy": "Lifestyle changes, hormonal therapy, and medications like metformin."
    },
    "Endometriosis": {
        "symptoms": ["pelvic pain", "painful periods", "infertility", "heavy bleeding"],
        "remedy": "Pain management, hormonal therapy, and surgical intervention if needed."
    },
    "Uterine Fibroids": {
        "symptoms": ["heavy menstrual bleeding", "pelvic pain", "frequent urination"],
        "remedy": "Medications, hormonal therapy, or surgery depending on severity."
    },
    "Pelvic Inflammatory Disease (PID)": {
        "symptoms": ["lower abdominal pain", "fever", "painful urination", "unusual discharge"],
        "remedy": "Antibiotic treatment and early detection to prevent complications."
    },
    "Cervical Cancer": {
        "symptoms": ["abnormal bleeding", "pelvic pain", "pain during intercourse"],
        "remedy": "HPV vaccination, regular screenings, and treatment options like surgery or radiation."
    },
    "Ovarian Cysts": {
        "symptoms": ["bloating", "pelvic pain", "irregular periods", "nausea"],
        "remedy": "Observation, hormonal therapy, or surgical removal if needed."
    },
    "Erectile Dysfunction (ED)": {
        "symptoms": ["difficulty maintaining an erection", "reduced sexual desire"],
        "remedy": "Lifestyle changes, medications like sildenafil, or therapy."
    },
    "Prostate Cancer": {
        "symptoms": ["difficulty urinating", "blood in urine", "pelvic discomfort"],
        "remedy": "Screening, active surveillance, surgery, or radiation therapy."
    },
    "Hypogonadism": {
        "symptoms": ["low testosterone", "fatigue", "loss of muscle mass", "low libido"],
        "remedy": "Hormone replacement therapy and lifestyle changes."
    },
    "Premature Ovarian Failure": {
        "symptoms": ["irregular or missed periods", "hot flashes", "infertility"],
        "remedy": "Hormone therapy, lifestyle adjustments, and fertility treatments."
    },
    "Sexually Transmitted Infections (STIs)": {
        "symptoms": ["genital sores", "painful urination", "abnormal discharge"],
        "remedy": "Antibiotics for bacterial STIs, antiviral medications for viral infections."
    },
    "Testicular Cancer": {
        "symptoms": ["lump in testicle", "swelling", "heaviness in the scrotum"],
        "remedy": "Surgical removal, chemotherapy, or radiation therapy."
    },
    "Infertility": {
        "symptoms": ["difficulty conceiving", "hormonal imbalances", "irregular periods"],
        "remedy": "Fertility treatments, lifestyle changes, and medical interventions."
    },
    "Vaginitis": {
        "symptoms": ["vaginal itching", "unusual discharge", "burning sensation"],
        "remedy": "Antifungal or antibiotic treatment based on cause."
    },
    "Menopause": {
        "symptoms": ["hot flashes", "night sweats", "mood swings", "bone loss"],
        "remedy": "Hormone therapy, lifestyle adjustments, and dietary changes."
    },
    "Varicocele": {
        "symptoms": ["scrotal pain", "swelling", "infertility"],
        "remedy": "Pain management or surgical intervention if fertility is affected."
    },
    "Hydrocele": {
        "symptoms": ["painless swelling in the scrotum"],
        "remedy": "Observation or surgical correction if needed."
    },
    "Dyspareunia (Painful Intercourse)": {
        "symptoms": ["pain during sex", "burning sensation", "vaginal dryness"],
        "remedy": "Lubricants, pelvic therapy, and hormonal treatments."
    },
    "Benign Prostatic Hyperplasia (BPH)": {
        "symptoms": ["frequent urination", "weak urine stream", "difficulty starting urination"],
        "remedy": "Medications, lifestyle changes, or surgical procedures."
    },
    "Premature Ejaculation": {
        "symptoms": ["inability to control ejaculation", "distress in sexual activity"],
        "remedy": "Behavioral therapy, medications, and lifestyle modifications."
    },
     "Liver Cirrhosis": {
        "symptoms": ["fatigue", "jaundice", "swelling in legs and abdomen"],
        "remedy": "Limit alcohol intake, maintain a healthy diet, and follow medical treatment."
    },
    "Hepatitis C": {
        "symptoms": ["dark urine", "fatigue", "jaundice"],
        "remedy": "Antiviral medications, avoid alcohol, and follow a healthy lifestyle."
    },
    "Fatty Liver Disease": {
        "symptoms": ["abdominal discomfort", "fatigue", "weight loss"],
        "remedy": "Exercise regularly, avoid alcohol, and maintain a balanced diet."
    },
    "Liver Cancer": {
        "symptoms": ["unexplained weight loss", "abdominal pain", "jaundice"],
        "remedy": "Medical consultation, chemotherapy, and possible surgical intervention."
    },
    "Autoimmune Hepatitis": {
        "symptoms": ["jaundice", "joint pain", "abdominal pain"],
        "remedy": "Steroid therapy and immunosuppressive medications under doctor supervision."
    },
    "Wilson's Disease": {
        "symptoms": ["tremors", "yellowing of skin and eyes", "speech problems"],
        "remedy": "Copper-chelating agents and dietary modifications."
    },
    "Hemochromatosis": {
        "symptoms": ["joint pain", "fatigue", "diabetes"],
        "remedy": "Regular blood removal (phlebotomy) and iron-reduction diet."

},
 "Coronary Artery Disease": {
        "symptoms": ["chest pain", "shortness of breath", "fatigue"],
        "remedy": "Maintain a healthy diet, exercise regularly, and take prescribed medications like statins or beta-blockers."
    },
    "Heart Attack": {
        "symptoms": ["chest pain", "left arm pain", "shortness of breath", "nausea"],
        "remedy": "Seek emergency medical help immediately. Chew an aspirin if recommended by a doctor."
    },
    "Heart Failure": {
        "symptoms": ["shortness of breath", "swelling in legs", "rapid heartbeat"],
        "remedy": "Reduce salt intake, monitor fluid levels, and take prescribed medications such as diuretics."
    },
    "Arrhythmia": {
        "symptoms": ["irregular heartbeat", "dizziness", "fainting"],
        "remedy": "Avoid caffeine, manage stress, and follow prescribed medications or procedures like a pacemaker if needed."
    },
      "Conjunctivitis": {
        "symptoms": ["redness", "itchy eyes", "watery discharge"],
        "remedy": "Use prescribed eye drops, maintain hygiene, and avoid touching eyes."
    },
    "Cataracts": {
        "symptoms": ["blurry vision", "light sensitivity", "difficulty seeing at night"],
        "remedy": "Wear UV-protective glasses, improve diet, and consider surgery if severe."
    },
    "Glaucoma": {
        "symptoms": ["vision loss", "eye pain", "halo around lights"],
        "remedy": "Use prescribed eye drops, control eye pressure, and undergo regular check-ups."
    },
    "Dry Eye Syndrome": {
        "symptoms": ["eye irritation", "redness", "blurred vision"],
        "remedy": "Use artificial tears, avoid dry environments, and blink frequently."
    },
    "Macular Degeneration": {
        "symptoms": ["central vision loss", "blurred vision", "difficulty recognizing faces"],
        "remedy": "Eat a diet rich in antioxidants, take prescribed medication, and consider laser therapy."
    },
    "Diabetic Retinopathy": {
        "symptoms": ["blurred vision", "dark spots", "vision loss"],
        "remedy": "Control blood sugar levels, undergo laser treatment, and monitor eye health."
    },
    "Retinal Detachment": {
        "symptoms": ["sudden vision loss", "floaters", "flashes of light"],
        "remedy": "Seek immediate medical attention, consider laser surgery, and avoid eye strain."
    },
   
    "Keratitis": {
        "symptoms": ["eye pain", "tearing", "blurry vision"],
        "remedy": "Use antibiotic or antifungal eye drops, avoid contact lenses, and maintain eye hygiene."
    },
    "Amblyopia (Lazy Eye)": {
        "symptoms": ["poor vision in one eye", "crossed eyes", "depth perception issues"],
        "remedy": "Use corrective lenses, practice eye exercises, and consider patch therapy."
    },
    "Strabismus": {
        "symptoms": ["crossed eyes", "double vision", "eye misalignment"],
        "remedy": "Use corrective glasses, perform eye exercises, and consider surgery if necessary."
    },
    "Optic Neuritis": {
        "symptoms": ["sudden vision loss", "eye pain", "color vision issues"],
        "remedy": "Take prescribed steroids, manage underlying conditions, and rest the eyes."
    },
    "Blepharitis": {
        "symptoms": ["eyelid inflammation", "crusty eyelashes", "itching"],
        "remedy": "Clean eyelids daily, use warm compresses, and apply antibiotic ointments if needed."
    },

   
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
