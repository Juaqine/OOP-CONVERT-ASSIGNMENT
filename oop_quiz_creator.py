class QuizCreator:
    def __init__(self, filename="quiz_data.txt"):
        self.filename = filename
        print("\nWelcome to the Quiz Creator!")

    def get_question_data(self):
        print("\nEnter your quiz questions and choices:")
        question = input("Question: ")
        choice_a = input("A.) ")
        choice_b = input("B.) ")
        choice_c = input("C.) ")
        choice_d = input("D.) ")
        correct_answer = self.get_correct_answer()
        return question, choice_a, choice_b, choice_c, choice_d, correct_answer

    def get_correct_answer(self):
        while True:
            answer = input("Correct answer (A/B/C/D): ").upper()
            if answer in ['A', 'B', 'C', 'D']:
                return answer
            print("❌ Please enter a valid answer: A, B, C, or D.")

    def save_question(self, question, a, b, c, d, answer):
        with open(self.filename, "a") as file:
            file.write("=== QUESTION START ===\n")
            file.write(f"Q: {question}\n")
            file.write(f"A: {a}\n")
            file.write(f"B: {b}\n")
            file.write(f"C: {c}\n")
            file.write(f"D: {d}\n")
            file.write(f"ANSWER: {answer}\n")
            file.write("=== QUESTION END ===\n\n")

    def ask_to_continue(self):
        while True:
            again = input("➕ Add another question? (yes/no): ").lower()
            if again in ["yes", "y"]:
                return True
            elif again in ["no", "n"]:
                print(f"\n✅ Quiz saved to '{self.filename}'. Goodbye!")
                return False
            else:
                print("❌ Invalid input. Please enter 'yes' or 'no'.")

    def run(self):
        while True:
            data = self.get_question_data()
            self.save_question(*data)
            if not self.ask_to_continue():
                break


if __name__ == "__main__":
    quiz_creator = QuizCreator()
    quiz_creator.run()

