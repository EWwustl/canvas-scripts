import csv
import os

from CanvasSettings import SEMESTER


def check_existing_csv(name):
    # check if the name already ends with '.csv', append '.csv' if it doesn't
    output_file_name = name if name.endswith('.csv') else name + '.csv'

    if os.path.exists(output_file_name):
        print(f'{output_file_name} already exists, skipping for efficiency.')
        return True
    else:
        return False


def write_students_to_csv(students_data, output_file_name=f'{SEMESTER}_students.csv'):
    if check_existing_csv(output_file_name):
        return

    with open(output_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['user_id', 'name', 'email', 'sortable_name', 'wustl_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user_id, student_info in students_data.items():
            student_info['user_id'] = user_id
            writer.writerow(student_info)

        print(f'Finished writing to {output_file_name}.')


def write_responses_to_csv(responses):
    for quiz_name, responses_list in responses.items():
        if not responses_list:
            print(f'No responses for {quiz_name}, skipping.')
            continue

        output_file_name = f"{SEMESTER}_{quiz_name.replace(' ', '_').lower()}.csv"

        with open(output_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            # Dynamically get the fieldnames from the first response item
            fieldnames = responses_list[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for response in responses_list:
                writer.writerow(response)

            print(f'Finished writing to {output_file_name}.')


def combine_csv_files(input_files, output_file):
    combined_data = []
    fieldnames = []

    # read content from all input CSV files and merge them
    for input_file in input_files:
        with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            combined_data.extend(list(reader))

    # get fieldnames from the last file
    if input_files:
        with open(input_files[-1], 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames

    # write the merged content into the output CSV file
    if combined_data and fieldnames:
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in combined_data:
                writer.writerow(row)

        print(f'Finished writing to {output_file}.')
    else:
        print('No data to write or no fieldnames available.')
