# from PIL import Image
# import io
# import random
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok"}

# ===== Deepfake =====

@app.post("/deepfake/detect")
async def detect_deepfake(file: UploadFile = File(None)):

    if not file:
        return {"label":"No file","confidence":0}

    content = await file.read()

    # load image
    img = Image.open(io.BytesIO(content))

    width, height = img.size

    # smart prototype logic (better fake AI)
    score = random.randint(45, 95)

    if width < 500 or height < 500:
        score += 10   # low-res often suspicious

    if file.filename.lower().endswith(".png"):
        score += 5

    score = min(score, 99)

    return {
        "label": "Likely Deepfake" if score > 65 else "Likely Authentic",
        "confidence": score,
        "explanation": "Frame artifacts and resolution anomaly detected.",
        "model": "TRINETRA Vision Prototype v2"
    }

# ===== Harassment =====
@app.post("/harassment/analyze")
async def analyze_harassment(
    text: str = Form(""),
    file: UploadFile = File(None)
):

    lower = text.lower()

    score = 2.0

    if any(x in lower for x in ["kill", "rape", "acid", "die"]):
        score += 4

    if any(x in lower for x in ["sexual", "touch", "body"]):
        score += 2

    if "again" in lower or "daily" in lower:
        score += 1

    score = min(9.9, score)

    threat = "HIGH" if score >= 7 else "MEDIUM" if score >= 4 else "LOW"

    return {
        "threatLevel": threat,
        "severityScore": score,
        "category": "AI Threat Analysis",
        "escalationRisk": "Severe" if score > 7 else "Moderate",
        "indicators": [
            {"name": "Toxicity", "score": score},
            {"name": "Threat Intent", "score": score - 1},
        ],
        "recommendedActions": [
            "Save screenshots",
            "Notify trusted contacts",
            "Escalate if needed"
        ]
    }

# ===== Safe Route =====
@app.post("/safe-route/plan")
async def safe_route(data: dict):

    source = data.get("source", "Unknown")
    destination = data.get("destination", "Unknown")

    # fake intelligent scoring
    risk = 3.4

    if "isolated" in source.lower():
        risk = 7.2

    return {
        "source": source,
        "destination": destination,
        "overallRiskScore": risk,
        "eta": "24 min",
        "safestPath": [
            "Main Road",
            "Market Area",
            "Police Station Road",
            destination
        ],
        "avoidZones": ["Dark Alley", "Industrial Lane"],
        "lightingScore": 8.1,
        "crowdScore": 7.4,
        "incidentDensityScore": 2.6,
        "liveShareUrl": "https://trinetra-demo/live",
        "sosContactsNotified": 3,
    }