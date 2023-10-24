def calculate_total_points(student):
    return (student.visits * student.group.visit_value) + student.additional_points + student.points_for_standard


def form_visit_history(student) -> str:
    res = []
    for v in student.visits_history:
        res.append(f'  ===========\n  Дата - {v.date}\n  Преподаватель - {v.teacher_name}\n  ===========\n \n')

    return ''.join(res)