from flask import Flask, render_template, request
import random

app = Flask(__name__)

DESTINATIONS = [
    {"name": "Old Faithful", "type": "iconic", "location": "Yellowstone", "difficulty": "easy",
     "family_friendly": True, "pet_friendly": False, "tags": ["geyser", "photo", "must-see"],
     "apple_maps": "https://maps.apple.com/?q=Old+Faithful", "elevation_ft": 7324},
    {"name": "Lamar Valley", "type": "wildlife", "location": "Yellowstone", "difficulty": "easy",
     "family_friendly": True, "pet_friendly": False, "tags": ["wildlife", "sunrise", "scenic"],
     "apple_maps": "https://maps.apple.com/?q=Lamar+Valley", "elevation_ft": 6600},
    {"name": "Beehive Basin Trail", "type": "hike", "location": "Big Sky", "difficulty": "moderate",
     "family_friendly": True, "pet_friendly": True, "tags": ["hike", "flowers", "mountain"],
     "apple_maps": "https://maps.apple.com/?q=Beehive+Basin+Trail", "elevation_ft": 7900}
]

LANGUAGES = {
    "en": "Welcome to YellowRoam!",
    "es": "¡Bienvenido a YellowRoam!",
    "hi": "YellowRoam में आपका स्वागत है!",
    "sv": "Välkommen till YellowRoam!"
}

def get_greeting(language):
    return LANGUAGES.get(language, LANGUAGES["en"])

def generate_itinerary(profile):
    results = []
    for dest in DESTINATIONS:
        if profile["family"] and not dest["family_friendly"]:
            continue
        if profile["pet"] and not dest["pet_friendly"]:
            continue
        if profile["difficulty"] != "any" and dest["difficulty"] != profile["difficulty"]:
            continue
        results.append(dest)
    return random.sample(results, min(len(results), profile["days"]))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        language = request.form.get("language")
        days = int(request.form.get("days"))
        family = request.form.get("family") == "yes"
        pet = request.form.get("pet") == "yes"
        difficulty = request.form.get("difficulty")

        profile = {
            "language": language,
            "days": days,
            "family": family,
            "pet": pet,
            "difficulty": difficulty
        }

        greeting = get_greeting(language)
        itinerary = generate_itinerary(profile)

        return render_template("results.html", greeting=greeting, itinerary=itinerary)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
