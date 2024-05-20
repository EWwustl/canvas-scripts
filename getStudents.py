from writeToCSV import SEMESTER, check_existing_csv


def get_students(course, filename=f'{SEMESTER}_students.csv'):
    if check_existing_csv(filename):
        return

    students = dict()
    for u in course.get_users(enrollment_type=['student', 'observer', 'student_view']):
        user_id = u.id
        profile = dict()
        profile['name'] = u.name
        profile['email'] = u.email if hasattr(u, 'email') else None
        profile['sortable_name'] = u.sortable_name
        profile['wustl_id'] = u.sis_user_id
        students[user_id] = profile

    return students
