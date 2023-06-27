#!/usr/bin/env python
import typer
import requests
import colorama
from time import sleep
from typing import List
from random import shuffle

app = typer.Typer()

API_URL = "https://opentdb.com/api.php"


def get_questions(
    amount: int, category: int, difficulty: str, question_type: str
) -> List[dict]:
    """
    Get trivia questions from the Open Trivia Database API.

    Args:
        amount (int): Number of questions to retrieve.
        category (int): Category ID of the questions.
        difficulty (str): Difficulty level of the questions (easy, medium, hard).
        question_type (str): Type of the questions (multiple, boolean).

    Returns:
        List[dict]: List of question dictionaries.
    """
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty,
        "type": question_type,
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["results"]


def animate_text(text: str):
    """
    Animate text by printing each character with a slight delay.

    Args:
        text (str): The text to animate.
    """
    for char in text:
        sleep(0.05)
        print(char, end="", flush=True)


def display_welcome():
    """
    Display the welcome message and instructions.
    """
    colorama.init()
    print(colorama.Fore.RED)
    animate_text("General Master Quiz? \n")
    sleep(1)
    print(colorama.Fore.RESET)
    print()
    animate_text(f"{colorama.Back.BLUE}HOW TO PLAY{colorama.Style.RESET_ALL}\n")
    sleep(1)
    animate_text("I am a process on your computer.\n")
    animate_text("If you get any question wrong I will be ")
    print(f"{colorama.Back.RED}killed{colorama.Style.RESET_ALL}")
    animate_text("So get all the questions right...\n\n")


def ask_multiple_choice_question(question: dict) -> bool:
    """
    Ask a multiple-choice question and prompt the user for an answer.

    Args:
        question (dict): The question dictionary.

    Returns:
        bool: True if the user's answer is correct, False otherwise.
    """
    print(question["question"])
    choices = question["incorrect_answers"] + [question["correct_answer"]]
    shuffle(choices)
    for i, choice in enumerate(choices):
        print(f"{i + 1}. {choice}")
    while True:
        try:
            answer = int(typer.prompt("Enter your choice (number) "))
            selected_choice = choices[answer - 1]
            return selected_choice == question["correct_answer"]
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")


def ask_boolean_question(question: dict) -> bool:
    """
    Ask a boolean question and prompt the user for an answer.

    Args:
        question (dict): The question dictionary.

    Returns:
        bool: True if the user's answer is correct, False otherwise.
    """
    print(question["question"])
    while True:
        answer = typer.prompt("Enter your answer (True/False) ").lower()
        if answer in ["true", "false"]:
            return answer == question["correct_answer"].lower()
        else:
            print("Invalid choice. Please enter either 'True' or 'False'.")


@app.command()
def quiz(
    num_questions: int = typer.Option(5, help="Number of questions"),
    category: int = typer.Option(18, help="Category ID"),
    difficulty: str = typer.Option(
        "easy", help="Difficulty level (easy, medium, hard)"
    ),
    question_type: str = typer.Option(
        "multiple", help="Question type (multiple, boolean)"
    ),
):
    """
    Run the General Master Quiz.

    Args:

    ✅ num_questions (int): Number of questions to answer.

    ✅ category (int): Category ID of the questions.

    ✅ difficulty (str): Difficulty level of the questions.

    ✅ question_type (str): Type of the questions.

    Returns: None
    """
    display_welcome()
    try:
        questions = get_questions(num_questions, category, difficulty, question_type)
    except requests.exceptions.RequestException as e:
        typer.secho(f"An error occurred: {str(e)}", fg=typer.colors.RED)
        return
    print()
    score = 0
    for index, question in enumerate(questions):
        if index > 0:
            print()
        if question_type == "multiple":
            is_correct = ask_multiple_choice_question(question)
        else:
            is_correct = ask_boolean_question(question)

        if is_correct:
            score += 1
            typer.secho("Nice work! That's a legit answer", fg=typer.colors.GREEN)
        else:
            typer.secho("💀💀💀 Game over! You lose!", fg=typer.colors.RED)
            typer.echo(f"The correct answer was: {question['correct_answer']}")
            return
    typer.secho(
        f"\nCongrats! You have answered {score} out of {num_questions} correctly!",
        fg=typer.colors.GREEN,
    )
    print()


if __name__ == "__main__":
    app()
