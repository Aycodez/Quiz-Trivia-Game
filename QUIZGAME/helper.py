# Importing the necessary libraries
import os
import sys
# import pandas as pd
import csv
import random


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



# function to get a particular quiz from the QUIZ file
def get_quiz(category, difficulty):
    # quiz file name
    quiz_name = resource_path(f'QUIZ/{category}-{difficulty}quiz.csv')

    # checking if its a file
    if not os.path.isfile(quiz_name):
        print('Invalid File')
        raise FileNotFoundError
    quiz = {'question': [],
            'incorrect_answers': [],
            'correct_answer': []}
    # reading the quiz file
    count = 0
    with open(quiz_name, 'r',encoding='utf8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if count > 20:
                break

            quiz['question'].append(row['question'])
            quiz['incorrect_answers'].append(row['incorrect_answers'])
            quiz['correct_answer'].append(row['correct_answer'])
            count += 1

    # reformatting the quiz texts
    questions = [i.replace('&quot;', '"').replace('&oacute;', 'ò').replace('&#039;', "'").replace('&rsquo;', "'") \
                     .replace('&ldquo;', "'").replace('&rdquo;', "'").replace('&shy;', "").replace('&prime',
                                                                                                   '').replace('&Prime',
                                                                                                               '') \
                     .replace('&lt', "<").replace('&gt', ">").replace('&eacute;', 'é').replace('&circ;', 'ê')
                 for i in quiz['question']]

    incorrect_answers = [
        i.replace('&quot;', '"').replace('&#039;', "'").replace('&rsquo;', "'").replace('[', '').replace(']',
                                                                                                         '').replace(
            ',', '') \
            .replace('&ldquo;', "'").replace('&rdquo;', "'").replace('&shy;', "").replace('&prime', '').replace(
            '&Prime', '') \
            .replace('&lt', "<").replace('&gt', ">").replace('&eacute;', 'é').replace('&circ;', 'ê').replace('&oacute;',
                                                                                                             'ò')
        for i in quiz['incorrect_answers']]

    correct_answer = [i.replace('&quot;', '"').replace('&#039;', "'").replace('&rsquo;', "'") \
                          .replace('&ldquo;', "'").replace('&rdquo;', "'").replace('&shy;', "").replace('&prime',
                                                                                                        '').replace(
        '&Prime', '') \
                          .replace('&lt', "<").replace('&gt', ">").replace('&eacute;', 'é').replace('&circ;',
                                                                                                    'ê').replace(
        '&oacute;', 'ò')
                      for i in quiz['correct_answer']]

    answers = []
    for i, j in enumerate(correct_answer):
        incorrect_answers[i] = [i for i in incorrect_answers[i].split("'") if i != '' and i != ' ']
        options = [j] + incorrect_answers[i]
        random.shuffle(options)
        answers.append(options)
    return [questions, correct_answer, answers]


def reshape_quiz(quiz):
    # reshaping the quiz so it can fit in the quiz label in the GUI
    if len(quiz) > 60 and len(quiz) < 90:
        quiz_question = f'{" ".join(quiz.split(" ")[:-2])} \n {" ".join(quiz.split(" ")[-2:])}'

    elif len(quiz) >= 90 and len(quiz) < 100:
        mid = int(len(quiz.split(' ')) / 2) + 2

        quiz_question = f'{" ".join(quiz.split(" ")[:mid])} \n {" ".join(quiz.split(" ")[mid:])}'

    elif len(quiz) >= 100:

        mid = int(len(quiz.split(' ')) / 2) + 1

        quiz_question = f'{" ".join(quiz.split(" ")[:mid])} \n {" ".join(quiz.split(" ")[mid:])}'

    else:
        quiz_question = f'{" "}{quiz}'

    return quiz_question

