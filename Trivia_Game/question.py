"""
File: question.py
Resources to manage a trivia question and its answers.
"""
import random

class TriviaQuestion:
    """Represents a trivia question"""
    def __init__(self, q, a, a1, a2, a3):
        """
        Constructor creates a TriviaQuestion with the given
        question and answers.
        Param q: The question
        Param a: The correct answer
        Param a1: An incorrect answer
        Param a2: An incorrect answer
        Param a3: An incorrect answer
        """
        self.question = q
        self.right_answer = a
        self.wrong_answers = []
        self.wrong_answers.append(a1)
        self.wrong_answers.append(a2)
        self.wrong_answers.append(a3)

    def get_question(self):
        """Returns the question."""
        return self.question

    def get_answers(self):
        """Returns a list of all answers in a random order."""
        # Create a list with the correct and incorrect answers
        answers = []
        answers.append(self.right_answer)
        for a in self.wrong_answers:
            answers.append(a)

        # Randomize the order of the answers
        random.shuffle(answers)

        # Return the answers
        return answers

    def check_guess(self, guess):
        """
        Checks the argument against the correct answer.
        Return: True if correct; False otherwise
        """
        return guess == self.right_answer