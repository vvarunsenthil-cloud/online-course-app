from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Course, Question, Choice, Submission, Enrollment


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Get enrollment of logged-in user for this course
    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    # Create submission
    submission = Submission.objects.create(enrollment=enrollment)

    # Get selected choices
    selected_choices = request.POST.getlist('choice')

    for choice_id in selected_choices:
        choice = get_object_or_404(Choice, pk=choice_id)
        submission.choices.add(choice)

    submission.save()

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:exam_result',
            args=(course.id, submission.id)
        )
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Selected choice IDs
    selected_ids = submission.choices.values_list('id', flat=True)

    grade = 0
    possible = 0

    questions = Question.objects.filter(lesson__course=course)

    for question in questions:
        possible += question.grade
        if question.is_get_score(selected_ids):
            grade += question.grade

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': possible
    }

    return render(
        request,
        'course/exam_result_bootstrap.html',
        context
    )

