import tkinter as tk
from tkinter import messagebox
import random

MAROON, GOLD, YELLOW, WHITE = "#800000", "#D4AF37", "#FFD700", "#FFFFFF"
CHOICES = ["A", "B", "C", "D"]
FILENAME = "quiz_data.txt"


class QuestionLoader:
    @staticmethod
    def load_questions(filename):
        try:
            with open(filename, "r") as f:
                raw = f.read().strip().split("=== QUESTION START ===")
        except FileNotFoundError:
            return []

        questions = []
        for block in raw:
            if "Q:" not in block:
                continue
            data = {}
            for line in block.strip().splitlines():
                if line.startswith(("Q:", "A:", "B:", "C:", "D:", "ANSWER:")):
                    key, value = line.split(": ", 1)
                    data["question" if key == "Q" else key.lower()] = value.strip().upper() if key == "ANSWER" else value.strip()

            choices = [(ch, data[ch.lower()]) for ch in CHOICES]
            random.shuffle(choices)

            new_data = {"question": data["question"]}
            correct_text = data[data["answer"].lower()]
            for i, (label, text) in enumerate(choices):
                new_label = CHOICES[i]
                new_data[new_label.lower()] = text
                if text == correct_text:
                    new_data["answer"] = new_label

            questions.append(new_data)

        random.shuffle(questions)
        return questions


class TitleScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Wars")
        self.root.geometry("600x400")
        self.root.config(bg=MAROON)

        tk.Label(self.root, text="Quiz Wars", font=("Arial", 32, "bold"), bg=MAROON, fg=YELLOW).pack(pady=100)
        tk.Button(self.root, text="Start Quiz", font=("Arial", 16), bg=GOLD, fg=MAROON, command=self.start_quiz).pack(pady=20)

    def start_quiz(self):
        questions = QuestionLoader.load_questions(FILENAME)
        if not questions:
            messagebox.showerror("Error", f"No questions found in {FILENAME}")
            return
        self.root.destroy()
        root = tk.Tk()
        QuizApp(root, questions)
        root.mainloop()


class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.score = 0
        self.current = 0
        self.total = len(questions)

        self.root.title("Quiz Wars")
        self.root.geometry("700x500")
        self.root.config(bg=MAROON)

        self.question_label = tk.Label(root, font=("Arial", 18), bg=MAROON, fg=YELLOW, wraplength=550)
        self.question_label.pack(pady=30)

        self.buttons = {}
        self.build_buttons()
        self.show_question()

    def build_buttons(self):
        frame = tk.Frame(self.root, bg=MAROON)
        frame.pack(pady=10)
        for i, ch in enumerate(CHOICES):
            btn = tk.Button(frame, text=ch, width=12, height=2, font=("Arial", 14),
                            bg=GOLD, fg=MAROON, command=lambda c=ch: self.check_answer(c))
            btn.grid(row=0, column=i, padx=10)
            self.buttons[ch] = btn

    def show_question(self):
        if self.current >= self.total:
            self.end_quiz()
            return
        q = self.questions[self.current]
        self.question_label.config(text=q["question"])
        for ch in CHOICES:
            self.buttons[ch].config(text=f"{ch}) {q[ch.lower()]}")

    def check_answer(self, choice):
        correct = self.questions[self.current]["answer"]
        if choice == correct:
            self.score += 1
            messagebox.showinfo("Correct!", "✅ Nice one!")
        else:
            messagebox.showinfo("Better luck next time!", f"❌ Correct answer: {correct}")
        self.current += 1
        self.show_question()

    def end_quiz(self):
        self.root.destroy()
        root = tk.Tk()
        EndScreen(root, self.score, self.total)
        root.mainloop()


class EndScreen:
    def __init__(self, root, score, total):
        self.root = root
        self.root.title("End of Quiz")
        self.root.geometry("600x400")
        self.root.config(bg=MAROON)

        tk.Label(root, text="Thank you for playing!", font=("Arial", 24, "bold"), bg=MAROON, fg=YELLOW).pack(pady=50)
        tk.Label(root, text=f"Your final score: {score}/{total}", font=("Arial", 18), bg=MAROON, fg=WHITE).pack(pady=10)

        tk.Button(root, text="Quit", font=("Arial", 16), bg=GOLD, fg=MAROON, command=root.quit).pack(pady=20)
        tk.Button(root, text="Restart Quiz", font=("Arial", 16), bg=GOLD, fg=MAROON, command=self.restart).pack(pady=10)

    def restart(self):
        self.root.destroy()
        root = tk.Tk()
        TitleScreen(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    TitleScreen(root)
    root.mainloop()
