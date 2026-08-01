"""
Generates a fake resume PDF so we have something real to test our
extraction pipeline on. This is NOT part of the product -- it's a
throwaway test-data generator.
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def build_resume(path="test_resume.pdf"):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, y, "Rohan Sharma")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(60, y, "Email: rohan.sharma@example.com | Phone: 987-654-3210")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "EXPERIENCE")
    y -= 18
    c.setFont("Helvetica", 10)
    lines = [
        "Software Engineering Intern, Acme Corp (2024 - 2025)",
        "- Built REST APIs using Python and FastAPI",
        "- Improved database query performance by 30%",
        "",
        "Machine Learning Intern, DataWorks (2023 - 2024)",
        "- Trained classification models using scikit-learn",
        "- Worked with Pandas and NumPy for data cleaning",
    ]
    for line in lines:
        c.drawString(60, y, line)
        y -= 16

    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "SKILLS")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(60, y, "Python, SQL, Machine Learning, FastAPI, Docker, Git")

    c.save()
    print(f"Wrote {path}")

if __name__ == "__main__":
    build_resume()
