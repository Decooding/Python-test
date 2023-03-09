import random
import json
import tkinter as tk


class TestApp:
    def __init__(self, questions):
        self.questions = questions
        self.num_questions = len(questions)
        self.score = 0
        self.current_question_index = 0

        self.root = tk.Tk()
        self.root.title("Тест")

        self.prompt_label = tk.Label(
            self.root, text="Вопрос", font=("Helvetica", 16))
        self.prompt_label.pack(padx=10, pady=10)

        self.choice_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="Вариант", font=(
                "Helvetica", 12), width=40, command=lambda i=i: self.answer_question(i))
            button.pack(padx=10, pady=5)
            self.choice_buttons.append(button)

        self.feedback_label = tk.Label(
            self.root, text="", font=("Helvetica", 16))
        self.feedback_label.pack(padx=10, pady=10)

        self.next_button = tk.Button(self.root, text="Следующий вопрос", font=(
            "Helvetica", 16), command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(padx=10, pady=10)

        self.score_label = tk.Label(
            self.root, text=f"Ваш счет: {self.score} / {self.num_questions}", font=("Helvetica", 16))
        self.score_label.pack(padx=10, pady=10)

        self.load_question(self.current_question_index)

        self.root.mainloop()

    def load_question(self, question_index):
        question = self.questions[question_index]
        self.prompt_label.configure(text=question['prompt'])
        choices = question['choices']
        random.shuffle(choices)  # перемешиваем варианты ответов
        for i, choice in enumerate(choices):
            self.choice_buttons[i].configure(text=choice, state=tk.NORMAL)
        self.feedback_label.configure(text="")
        self.next_button.configure(state=tk.DISABLED)

    def answer_question(self, choice_index):
        question = self.questions[self.current_question_index]
        if question['choices'][choice_index] == question['answer']:
            self.feedback_label.configure(text="Верно!", fg="green")
            self.score += 1
        else:
            self.feedback_label.configure(text="Неверно!", fg="red")
        self.score_label.configure(
            text=f"Ваш счет: {self.current_question_index} / {self.num_questions}")
        for button in self.choice_buttons:
            button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.NORMAL)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index >= self.num_questions:
            self.show_results()
            return
        self.load_question(self.current_question_index)
        for button in self.choice_buttons:
            button.configure(state=tk.NORMAL)
        self.next_button.configure(state=tk.DISABLED)

    def show_results(self):
        percent_correct = int(self.score / self.num_questions * 100)
        result_text = f"Вы ответили правильно на {self.score} из {self.num_questions} вопросов ({percent_correct}%)."
        self.prompt_label.configure(text=result_text)
        self.feedback_label.configure(text="")
        for button in self.choice_buttons:
            button.destroy()
        self.next_button.configure(text="Закрыть", command=self.root.destroy)


if __name__ == "__main__":
    filename = input("Введите имя файла: ")
    with open(filename, "r", encoding="utf-8") as f:
        questions = json.load(f)
    random.shuffle(questions)  # перемешивание вопросов

    app = TestApp(questions)
