from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import folium
from io import BytesIO
import base64

app = Flask(__name__)

# Dummy data for hospitals (latitude, longitude, and name)
hospitals = [
    {"name": "Hospital A", "lat": 12.9716, "long": 77.5946},
    {"name": "Hospital B", "lat": 13.0827, "long": 80.2707},
    {"name": "Hospital C", "lat": 19.0760, "long": 72.8777}
]

# Function to convert text to speech and return the audio in base64
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    
    # Encode audio to base64 to send over the web
    audio_base64 = base64.b64encode(audio_fp.read()).decode('utf-8')
    return audio_base64

# Route to render the main page with hospital map
@app.route('/')
def index():
    # Generate map with hospital markers
    map_center = [12.9716, 77.5946]  # Example for center (latitude, longitude)
    hospital_map = folium.Map(location=map_center, zoom_start=5)

    for hospital in hospitals:
        folium.Marker(
            location=[hospital["lat"], hospital["long"]],
            popup=hospital["name"]
        ).add_to(hospital_map)

    # Save the map to HTML and render it on the webpage
    map_html = hospital_map._repr_html_()

    return render_template('index.html', map_html=map_html)

# Route for Text-to-Speech functionality
@app.route('/speak', methods=['POST'])
def speak():
    # Get text input from the user
    text = request.form.get('text')

    if text:
        audio_base64 = speak_text(text)
        return jsonify({"audio_base64": audio_base64})
    return jsonify({"error": "No text provided"})

if __name__ == '__main__':
    app.run(debug=True)
