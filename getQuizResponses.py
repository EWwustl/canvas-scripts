import re
from bs4 import BeautifulSoup
from CanvasSettings import *
from writeToCSV import check_existing_csv


def get_question_answers(quiz):
    questions = quiz.get_questions()

    # map the questions to the answer id and answer text
    question_answers = dict()
    for question in questions:
        question_answers[question.id] = {
            'name': question.question_name,
            'answers': {answer['id']: answer['text'] for answer in question.answers}
        }

    return question_answers


def get_quiz_question_answers(quizzes):
    # map each quiz to their question answers
    quiz_question_answers = dict()
    for quiz in quizzes:
        question_answers = get_question_answers(quiz)
        quiz_question_answers[quiz.title] = question_answers

    return quiz_question_answers


def filter_quizzes(course):
    all_quizzes = course.get_quizzes()

    quiz_titles = {quiz.title for quiz in all_quizzes}

    all_assignments = course.get_assignments()
    quiz_assignments = [assignment for assignment in all_assignments if assignment.name in quiz_titles]

    return all_quizzes, quiz_assignments


def process_submissions(submissions, answers_mapping, quiz_name):
    responses = []
    for submission in submissions:
        submission_histories = submission.submission_history
        # iterate through all submission histories to extract the newest submission only
        newest_submission = None
        for submission_history in submission_histories:
            if not newest_submission or submission_history.submitted_at > newest_submission.submitted_at:
                newest_submission = submission_history

        if newest_submission and 'submission_data' in newest_submission:
            response_dict = generate_response_dict(newest_submission, quiz_name, answers_mapping)
            responses.append(response_dict)
    return responses


def generate_response_dict(submission, quiz_name, answers_mapping):
    quiz_name_sanitized = quiz_name.replace(' ', '_').lower()

    response_dict = {
        'id': submission['id'],
        'hw': quiz_name_sanitized,
        'review_id': SEMESTER + '_' + quiz_name_sanitized + '_' + str(submission['id']),
        'user_id': submission['user_id']
    }

    for result in submission['submission_data']:
        process_submission_result(result, response_dict, answers_mapping)

    return response_dict


def process_submission_result(result, response_dict, answers_mapping):
    question_id = result['question_id']
    if 'answer_id' in result and question_id in answers_mapping:
        answer_id = result['answer_id']
        answer_text = answers_mapping[question_id]['answers'].get(answer_id)
        result['text'] = answer_text

    if 'text' in result:
        answer = result['text']
        question_name_sanitized = answers_mapping[question_id]['name'].replace(' ', '_').lower()
        map_answer_to_response_dict(answer, question_name_sanitized, response_dict)


def map_answer_to_response_dict(answer, question_name, response_dict):
    # use BeautifulSoup to parse and clean HTML content
    soup = BeautifulSoup(answer, 'html.parser')
    cleaned_text = soup.get_text()

    # check if the original answer was enclosed in <p> tags
    if answer.startswith('<p>') and answer.endswith('</p>'):
        response_dict[question_name + '_text'] = cleaned_text
        response_dict[question_name + '_length'] = len(cleaned_text)
    else:
        response_dict[question_name] = cleaned_text


def get_responses(course):
    quizzes, quiz_assignments = filter_quizzes(course)
    quiz_question_answers = get_quiz_question_answers(quizzes)

    responses = dict()
    for quiz_assignment in quiz_assignments:
        try:
            name = quiz_assignment.name
            if check_existing_csv(f"{SEMESTER}_{name.replace(' ', '_').lower()}"):
                continue  # skip processed quiz

            answers_mapping = quiz_question_answers[name]
            submissions = quiz_assignment.get_submissions(include=['submission_history'])
            responses[name] = process_submissions(submissions, answers_mapping, name)
        except Exception as e:
            print(f'Error processing {quiz_assignment.name}: {e}, skipping it...')
            continue  # skip this assignment and continue with the next one

    return responses
