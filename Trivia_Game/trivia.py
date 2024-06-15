"""
File: trivia.py
Author: Alex Gill
A trivia game.
"""
from tkinter import *
from tkinter import ttk
from question import TriviaQuestion
import random
import pathlib

# --- Global constants ---
WIDTH = 300                         # The width of the window
HEIGHT = 400                        # The height of the window
FILENAME = 'trivia_questions.txt'   # The file name
NUM_ROUNDS = 7                      # The number of rounds

# --- Global variables ---
questions = None        # A list of trivia questions
cur_question = None     # The current TriviaQuestion
round = 0               # The current round
total_points = 0        # The player's total score so far

# --- GUI components ---
round_label = None      # The label for the round
time_label = None       # The label displaying the seconds remaining
question_label = None   # The label for the question
answer_buttons = None   # The buttons for th answers
guess_label = None      # The label for the player's guess
answer_label = None     # The label for the correct answer
points_label = None     # The label for the points earned
total_label = None      # The label for the total points
time = None             # The seconds remaining
run = True              # Indicates whether to continue the countdown

def build_interface(window):
    """Builds the trivia game interface."""
    # --- Question interface ---
    # Create the round label
    global round_label; round_label = ttk.Label(window, text='Round')

    # Create the time label
    global time; time = IntVar(window, 0)
    global time_label; time_label = ttk.Label(window, textvariable=time)

    # Create the question label
    global question_label; question_label = ttk.Label(window, text='Question')

    # Create the answer buttons
    global answer_buttons; answer_buttons = []
    for i in range(4):
        answer_buttons.append(ttk.Button(window, text='Answer ' + str(i)))

    # --- Results interface ---
    # Create the player's guess label
    global guess_label; guess_label = ttk.Label(window, text='Guess')

    # Create the correct answer label
    global answer_label; answer_label = ttk.Label(window, text='Answer')

    # Create the points earned label
    global points_label; points_label = ttk.Label(window, text='Points')

    # Create the total points label
    global total_label; total_label = ttk.Label(window, text='Total')


def next_question(window):
    """Displays the next question."""
    # Get the question and answers
    global cur_question; cur_question = questions.pop(
        random.randint(0, len(questions) - 1))
    question = cur_question.get_question()
    answers = cur_question.get_answers()

    # Remove everything from the window
    for widget in window.winfo_children():
        widget.grid_remove()

    # Increment the round and reset the time
    global round; round += 1
    global run; run = True
    global time; time.set(20)

    # Set the grid geometry
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=18)
    window.grid_rowconfigure(3, weight=2)
    window.grid_rowconfigure(4, weight=2)
    window.grid_rowconfigure(5, weight=2)
    window.grid_rowconfigure(6, weight=2)

    # Display the round
    global round_label
    if round == NUM_ROUNDS:
        round_label.configure(text='Bonus Round')
    else:
        round_label.configure(text='Round ' + str(round))
    round_label.grid(row=0, column=0)

    # Display the time left
    global time_label; time_label.grid(row=1, column=0)

    # Display the question
    global question_label; question_label.configure(text=question)
    question_label.grid(row=2, column=0)

    # Wait for the player to read the question
    window.after(len(question) * 40, lambda: display_answers(window, answers))


def display_answers(window, answers):
    """Displays the answers and starts the countdown."""
    # Display the answers
    global round
    global answer_buttons
    for i in range(4):
        answer_buttons[i].configure(text=answers[i],
            command=lambda ans=answers[i]:
            submit_guess(window, ans, time.get() if round < 7
            else time.get() * 2))
        answer_buttons[i].grid(row=i + 3, column=0)

    # Start the countdown
    countdown(window)


def results_screen(window, guess, points):
    """Displays the results from the previous question."""
    # Get the right answer
    global cur_question; answer = cur_question.right_answer

    # Disable the countdown
    global run; run = False

    # Remove everything from the window
    for widget in window.winfo_children():
        widget.grid_remove()

    # Set the grid geometry
    window.grid_rowconfigure(0, weight=3)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)
    window.grid_rowconfigure(5, weight=3)
    window.grid_rowconfigure(6, weight=0)

    # Display the player's guess
    global guess_label; guess_label.configure(text='You answered: '+guess)
    guess_label.grid(row=1, column=0)

    # Display the correct answer
    global answer_label; answer_label.configure(text='Correct answer: '+answer)
    answer_label.grid(row=2, column=0)

    # Display the earned points
    global points_label; points_label.configure(text='Points earned: ' + \
        str(points))
    points_label.grid(row=3, column=0)

    # Display the total points
    global total_points
    global total_label; total_label.configure(text='Total points: ' + \
        str(total_points))
    total_label.grid(row=4, column=0)

    # Show the next question or show final results if over
    if round < NUM_ROUNDS:
        window.after(3000, lambda: next_question(window))
    else:
        window.after(3000, lambda: final_results(window))


def final_results(window):
    """Displays the final score of game."""
    # Remove everything from the window
    for widget in window.winfo_children():
        widget.grid_remove()

    # Set the grid geometry
    window.grid_rowconfigure(0, weight=3)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=3)
    window.grid_rowconfigure(4, weight=0)
    window.grid_rowconfigure(5, weight=0)
    window.grid_rowconfigure(6, weight=0)

    # Display the total score
    global total_points
    ttk.Label(window, text='Your score: ' + \
        str(total_points)).grid(row=1, column=0)

    # Reset the round and points
    global round; round = 0
    total_points = 0

    # Display a play again button
    ttk.Button(window, text='Play Again', command=lambda:
        next_question(window)).grid(row=2, column=0)


def submit_guess(window, guess, points):
    """Submits the player's guess and checks if it is correct before
    moving to the next question."""
    if guess == cur_question.right_answer:
        global total_points; total_points += points
        results_screen(window, guess, points)
    else:
        results_screen(window, guess, 0)


def countdown(window):
    """Decrements the time every second."""
    window.after(1000, lambda: countdown_helper(window))


def countdown_helper(window):
    """Decrements the time every second."""
    global time; time.set(time.get() - 1)
    global run
    if run:
        window.after(1000, lambda: countdown_helper(window))


def read_questions(filename):
    """
    Builds a list of TriviaQuestion objects from a file with
    the given file name.
    Param filename: The file name
    Return: The list of TriviaQuestion objects
    """
    # Create a list of questions
    questions = []

    # Open the file
    file = open(str(pathlib.Path(__file__).parent.resolve()) + '\\' + \
        filename, 'r')

    # Read the questions from the file into the list
    line_number = 1
    for line in file:
        line = line.strip()
        tokens = line.split('/')
        if len(tokens) != 5:    # Must have 5 tokens; exit
            print('Error: trivia line must have a question and 4 answers.')
            print('\tLine %d: %s' % (line_number, line))
            exit()
        questions.append(TriviaQuestion(*tokens))
        line_number += 1

    # Close the file
    file.close()

    # Return the list of questions
    return questions


def set_window_resize(window):
    """Centers the window and prevents the it from shrinking past its
    default size."""
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + frm_width * 2
    height = window.winfo_height()
    tlb_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + tlb_height + frm_width
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.minsize(width=width, height=height)


def main():
    # Create a list of questions read from the file
    global questions; questions = read_questions(FILENAME)

    # Create the root
    root = Tk()
    root.title('Trivia Game')
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    root.grid_columnconfigure(0, weight=1)

    # Create styles
    s = ttk.Style()
    s.configure('TLabel', wraplength=WIDTH-2, justify=CENTER, font=('', 12))
    s.configure('TButton', wraplength=WIDTH-2, justify=CENTER, font=('', 12))

    # Build the user interface
    build_interface(root)

    # Reset the round and points
    global round; round = 0
    global total_points; total_points = 0

    # Display the first question
    next_question(root)

    # Set the root window's resize properties
    set_window_resize(root)

    # Start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()