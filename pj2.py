import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from textblob import TextBlob
from difflib import SequenceMatcher
from docx import Document
import pytesseract
import PyPDF2
import re

# -----------------------------------
# OCR PATH
# -----------------------------------

pytesseract.pytesseract.tesseract_cmd = \
r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------------
# COLORS
# -----------------------------------

BG = "#0F172A"
PANEL = "#1E293B"

CYAN = "#06B6D4"
GREEN = "#10B981"
PURPLE = "#8B5CF6"
ORANGE = "#F97316"
RED = "#EF4444"
PINK = "#EC4899"
BLUE = "#6366F1"
TEAL = "#14B8A6"

WHITE = "#FFFFFF"

BTN_FONT = ("Segoe UI", 10, "bold")

# -----------------------------------
# FUNCTIONS
# -----------------------------------

def correct_spelling(text):

    words = re.findall(
        r"\b[\w']+\b|[^\w\s]|\s+",
        text
    )

    corrected = []
    mistakes = []

    for token in words:

        if token.isspace():
            corrected.append(token)
            continue

        if not re.fullmatch(
            r"\b[\w']+\b",
            token
        ):
            corrected.append(token)
            continue

        suggestion = str(
            TextBlob(token).correct()
        )

        if suggestion.lower() != token.lower():

            mistakes.append(
                (token, suggestion)
            )

        corrected.append(suggestion)

    return "".join(corrected), mistakes


def grammar_check(text):

    tips = []

    if "I is" in text:
        tips.append("Use I am")

    if "he have" in text:
        tips.append("Use he has")

    if "she have" in text:
        tips.append("Use she has")

    if "they is" in text:
        tips.append("Use they are")

    return tips


def analyze_paper(text):

    words = len(text.split())

    questions = len(
        re.findall(r"\?", text)
    )

    return words, questions


def detect_subject(text):

    text = text.lower()

    if "python" in text or "algorithm" in text:
        return "Computer Science"

    if "equation" in text or "triangle" in text:
        return "Mathematics"

    if "atom" in text or "cell" in text:
        return "Science"

    return "General"


def difficulty(text):

    count = len(text.split())

    if count > 500:
        return "Hard"

    elif count > 200:
        return "Medium"

    return "Easy"


def similarity(a, b):

    score = SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()

    return round(score * 100, 2)


def calculate_marks(percent):

    if percent >= 90:
        return 10

    elif percent >= 75:
        return 8

    elif percent >= 60:
        return 6

    elif percent >= 40:
        return 4

    return 2


def solve_math(expression):

    try:
        return str(eval(expression))

    except:
        return "Invalid Expression"


def generate_paragraph(topic):

    return f"""
{topic} is an important topic in modern education.

It helps students improve knowledge and practical skills.

Understanding {topic} develops analytical thinking and problem solving abilities.

The topic is widely used in schools, colleges, industries and research organizations.

Therefore, {topic} plays a significant role in personal and professional development.
"""


def generate_questions(topic):

    return f"""
1. What is {topic}?

2. Explain {topic}.

3. What are the advantages of {topic}?

4. What are the applications of {topic}?

5. Why is {topic} important?

6. Explain {topic} with examples.

7. What are the features of {topic}?

8. Discuss the limitations of {topic}.

9. Write a short note on {topic}.

10. Give a conclusion about {topic}.
"""

# -----------------------------------
# MAIN APP
# -----------------------------------

class AIApp:

    def __init__(self, root):

        self.root = root

        root.title(
            "AI SMART QUESTION PAPER ANALYZER"
        )

        root.state("zoomed")
        root.configure(bg=BG)

        title = tk.Label(
            root,
            text="🤖 AI SMART QUESTION PAPER ANALYZER",
            font=("Segoe UI", 24, "bold"),
            bg=BG,
            fg=CYAN
        )

        title.pack(pady=10)

        self.input_box = tk.Text(
            root,
            font=("Calibri",14),
            bg=PANEL,
            fg=WHITE,
            height=12
        )

        self.input_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        btn_frame = tk.Frame(
            root,
            bg=BG
        )

        btn_frame.pack()

        tk.Button(
            btn_frame,
            text="Check Text",
            bg=CYAN,
            font=BTN_FONT,
            command=self.check_text
        ).grid(row=0,column=0,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Analyze",
            bg=PURPLE,
            font=BTN_FONT,
            command=self.analyze
        ).grid(row=0,column=1,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Upload Image",
            bg=GREEN,
            font=BTN_FONT,
            command=self.upload_image
        ).grid(row=0,column=2,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Upload PDF",
            bg=ORANGE,
            font=BTN_FONT,
            command=self.upload_pdf
        ).grid(row=0,column=3,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Upload DOCX",
            bg=CYAN,
            font=BTN_FONT,
            command=self.upload_docx
        ).grid(row=0,column=4,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Answer Check",
            bg=RED,
            font=BTN_FONT,
            command=self.check_answer
        ).grid(row=0,column=5,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Math Solver",
            bg=TEAL,
            font=BTN_FONT,
            command=self.math_solver
        ).grid(row=1,column=0,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Paragraph",
            bg=PINK,
            font=BTN_FONT,
            command=self.paragraph_generator
        ).grid(row=1,column=1,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Questions",
            bg=BLUE,
            font=BTN_FONT,
            command=self.question_generator
        ).grid(row=1,column=2,padx=5,pady=5)

        tk.Button(
            btn_frame,
            text="Clear",
            bg=RED,
            fg="white",
            font=BTN_FONT,
            command=self.clear_all
        ).grid(row=1,column=3,padx=5,pady=5)

        self.output_box = tk.Text(
            root,
            font=("Calibri",14),
            bg=PANEL,
            fg=GREEN,
            height=12
        )

        self.output_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.report = tk.Label(
            root,
            text="Ready",
            bg=BG,
            fg="yellow",
            font=("Segoe UI",13,"bold")
        )

        self.report.pack(pady=10)

    def clear_all(self):

        self.input_box.delete(
            "1.0","end"
        )

        self.output_box.delete(
            "1.0","end"
        )

        self.report.config(
            text="Ready"
        )

    def check_text(self):

        text = self.input_box.get(
            "1.0",
            "end"
        )

        corrected, mistakes = correct_spelling(text)

        grammar = grammar_check(corrected)

        self.output_box.delete(
            "1.0",
            "end"
        )

        self.output_box.insert(
            "1.0",
            corrected
        )

        self.report.config(
            text=f"Spelling Errors: {len(mistakes)} | Grammar Tips: {len(grammar)}"
        )

    def analyze(self):

        text = self.input_box.get(
            "1.0",
            "end"
        )

        words, questions = analyze_paper(text)

        subject = detect_subject(text)

        level = difficulty(text)

        self.report.config(
            text=f"Words:{words}  Questions:{questions}  Subject:{subject}  Difficulty:{level}"
        )

    def upload_image(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Images","*.png *.jpg *.jpeg")
            ]
        )

        if path:

            img = Image.open(path)

            text = pytesseract.image_to_string(img)

            self.input_box.delete(
                "1.0",
                "end"
            )

            self.input_box.insert(
                "1.0",
                text
            )

    def upload_pdf(self):

        path = filedialog.askopenfilename(
            filetypes=[("PDF","*.pdf")]
        )

        if not path:
            return

        text = ""

        with open(path,"rb") as f:

            pdf = PyPDF2.PdfReader(f)

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

        self.input_box.delete(
            "1.0",
            "end"
        )

        self.input_box.insert(
            "1.0",
            text
        )

    def upload_docx(self):

        path = filedialog.askopenfilename(
            filetypes=[("Word","*.docx")]
        )

        if not path:
            return

        doc = Document(path)

        text = "\n".join(
            p.text for p in doc.paragraphs
        )

        self.input_box.delete(
            "1.0",
            "end"
        )

        self.input_box.insert(
            "1.0",
            text
        )

    def paragraph_generator(self):

        topic = self.input_box.get(
            "1.0",
            "end"
        ).strip()

        self.output_box.delete(
            "1.0",
            "end"
        )

        self.output_box.insert(
            "1.0",
            generate_paragraph(topic)
        )

    def question_generator(self):

        topic = self.input_box.get(
            "1.0",
            "end"
        ).strip()

        self.output_box.delete(
            "1.0",
            "end"
        )

        self.output_box.insert(
            "1.0",
            generate_questions(topic)
        )

    def math_solver(self):

        top = tk.Toplevel()

        top.title("Math Solver")

        top.geometry("400x250")

        tk.Label(
            top,
            text="Enter Expression"
        ).pack(pady=10)

        entry = tk.Entry(
            top,
            width=30
        )

        entry.pack()

        def calculate():

            result = solve_math(
                entry.get()
            )

            messagebox.showinfo(
                "Answer",
                result
            )

        tk.Button(
            top,
            text="Solve",
            command=calculate
        ).pack(pady=15)

    def check_answer(self):

        top = tk.Toplevel()

        top.title("Answer Checker")

        tk.Label(
            top,
            text="Model Answer"
        ).pack()

        model = tk.Text(
            top,
            height=5,
            width=60
        )

        model.pack()

        tk.Label(
            top,
            text="Student Answer"
        ).pack()

        student = tk.Text(
            top,
            height=5,
            width=60
        )

        student.pack()

        def calculate():

            a = model.get(
                "1.0",
                "end"
            )

            b = student.get(
                "1.0",
                "end"
            )

            sim = similarity(a,b)

            marks = calculate_marks(sim)

            messagebox.showinfo(
                "Result",
                f"Similarity: {sim}%\nMarks: {marks}/10"
            )

        tk.Button(
            top,
            text="Evaluate",
            command=calculate
        ).pack(pady=10)

root = tk.Tk()

app = AIApp(root)

root.mainloop()
