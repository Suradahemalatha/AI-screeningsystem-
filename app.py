from flask import Flask, render_template, request
import os
from skills import SKILLS

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def read_text_file(file_path):
    """Read text from a .txt file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def extract_skills(text):
    """Extract matching skills from the predefined SKILLS list."""
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    # Get uploaded files
    job_file = request.files["job_description"]
    resume_file = request.files["resume"]

    # Validate
    if job_file.filename == "" or resume_file.filename == "":
        return "Please upload both files."

    # Save files
    job_path = os.path.join(app.config["UPLOAD_FOLDER"], job_file.filename)
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)

    job_file.save(job_path)
    resume_file.save(resume_path)

    # Read files
    job_text = read_text_file(job_path)
    resume_text = read_text_file(resume_path)

    # Extract skills
    job_skills = extract_skills(job_text)
    resume_skills = extract_skills(resume_text)

    # Match skills
    matched_skills = list(set(job_skills) & set(resume_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    # Calculate score
    if len(job_skills) == 0:
        score = 0
    else:
        score = round((len(matched_skills) / len(job_skills)) * 100, 2)

    # Recommendation
    if score >= 80:
        recommendation = "Highly Recommended"
    elif score >= 60:
        recommendation = "Recommended"
    else:
        recommendation = "Needs Improvement"

    return render_template(
        "result.html",
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        recommendation=recommendation
    )


if __name__ == "__main__":
    app.run(debug=True)