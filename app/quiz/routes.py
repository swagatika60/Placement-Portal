"""
Quiz Routes for Placement Preparation Portal
=============================================
This module handles all quiz-related functionality including:
- Viewing categories
- Starting and taking quizzes
- Submitting answers
- Viewing results
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app.models import Category, Question, QuizResult, StudentActivity
from app import db
from datetime import datetime
import random

quiz = Blueprint('quiz', __name__)


@quiz.route('/categories')
@quiz.route('/')
@login_required
def list_categories():
    """List all quiz categories."""
    aptitude_categories = Category.query.filter_by(type='aptitude').order_by(Category.name).all()
    technical_categories = Category.query.filter_by(type='technical').order_by(Category.name).all()

    # Get user's best scores for each category
    category_scores = {}
    results = QuizResult.query.filter_by(user_id=current_user.id).all()
    for result in results:
        cat_id = result.category_id
        if cat_id not in category_scores or result.percentage > category_scores[cat_id]:
            category_scores[cat_id] = result.percentage

    return render_template('quiz/categories.html',
                           aptitude_categories=aptitude_categories,
                           technical_categories=technical_categories,
                           category_scores=category_scores)


@quiz.route('/category/<int:category_id>')
@login_required
def view_category(category_id):
    """View category details and start quiz."""
    category = Category.query.get_or_404(category_id)
    questions_count = Question.query.filter_by(category_id=category_id).count()

    # Get user's previous attempts for this category
    previous_attempts = QuizResult.query.filter_by(
        user_id=current_user.id,
        category_id=category_id
    ).order_by(QuizResult.taken_at.desc()).all()

    return render_template('quiz/category.html',
                           category=category,
                           questions_count=questions_count,
                           previous_attempts=previous_attempts)


@quiz.route('/start/<int:category_id>', methods=['GET', 'POST'])
@login_required
def start_quiz(category_id):
    """Start a new quiz attempt. Fetch 10 random questions and store in session."""
    category = Category.query.get_or_404(category_id)

    # Get all questions for this category
    all_questions = Question.query.filter_by(category_id=category_id).all()

    if not all_questions:
        flash('No questions available in this category.', 'warning')
        return redirect(url_for('quiz.list_categories'))

    # Select 10 random questions (or all if less than 10)
    num_questions = min(10, len(all_questions))
    selected_questions = random.sample(all_questions, num_questions)

    # Store question IDs and quiz start time in session
    question_ids = [q.id for q in selected_questions]
    session['quiz_question_ids'] = question_ids
    session['quiz_category_id'] = category_id
    session['quiz_start_time'] = datetime.utcnow().isoformat()

    # Log activity
    activity = StudentActivity(
        user_id=current_user.id,
        activity_type='quiz_start',
        description=f'Started quiz for category: {category.name}'
    )
    db.session.add(activity)
    db.session.commit()

    flash(f'Quiz started! You have {num_questions} questions to answer.', 'success')
    return redirect(url_for('quiz.question', question_num=1))


@quiz.route('/question/<int:question_num>')
@login_required
def question(question_num):
    """Display a specific question."""
    # Check if quiz is in progress
    if 'quiz_question_ids' not in session:
        flash('No quiz in progress. Please start a new quiz.', 'warning')
        return redirect(url_for('quiz.list_categories'))

    question_ids = session.get('quiz_question_ids', [])
    category_id = session.get('quiz_category_id')

    if question_num < 1 or question_num > len(question_ids):
        flash('Invalid question number.', 'error')
        return redirect(url_for('quiz.list_categories'))

    # Get the current question
    question_id = question_ids[question_num - 1]
    question = Question.query.get_or_404(question_id)

    # Get category info
    category = Category.query.get(category_id)

    # Calculate progress
    progress = (question_num / len(question_ids)) * 100

    return render_template('quiz/question.html',
                           title=f'Question {question_num}',
                           question=question,
                           question_num=question_num,
                           total_questions=len(question_ids),
                           category=category,
                           progress=progress)


@quiz.route('/submit', methods=['POST'])
@login_required
def submit_quiz():
    """Submit quiz answers, calculate score, save QuizResult, log StudentActivity."""
    if 'quiz_question_ids' not in session:
        flash('No quiz in progress.', 'warning')
        return redirect(url_for('quiz.list_categories'))

    question_ids = session.get('quiz_question_ids', [])
    category_id = session.get('quiz_category_id')
    start_time_str = session.get('quiz_start_time')

    # Calculate score
    score = 0
    total_questions = len(question_ids)

    for qid in question_ids:
        question = Question.query.get(qid)
        answer = request.form.get(f'question_{qid}')
        if answer and question and answer.upper() == question.correct_answer:
            score += 1

    # Calculate percentage
    percentage = (score / total_questions * 100) if total_questions > 0 else 0

    # Create QuizResult
    quiz_result = QuizResult(
        user_id=current_user.id,
        category_id=category_id,
        score=score,
        total_questions=total_questions,
        percentage=round(percentage, 2)
    )
    db.session.add(quiz_result)
    db.session.flush()  # Get the ID without committing

    # Log activity
    category = Category.query.get(category_id)
    activity = StudentActivity(
        user_id=current_user.id,
        activity_type='quiz_complete',
        description=f'Completed quiz for {category.name if category else "Unknown"}: Score {score}/{total_questions} ({percentage:.1f}%)'
    )
    db.session.add(activity)
    db.session.commit()

    # Clear quiz session data
    session.pop('quiz_question_ids', None)
    session.pop('quiz_category_id', None)
    session.pop('quiz_start_time', None)

    flash('Quiz submitted successfully!', 'success')
    return redirect(url_for('quiz.results', result_id=quiz_result.id))


@quiz.route('/take/<int:category_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(category_id):
    """Take the quiz - display questions and handle submission."""
    category = Category.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category_id).all()

    if not questions:
        flash('No questions available in this category.', 'warning')
        return redirect(url_for('quiz.list_categories'))

    if request.method == 'POST':
        # Calculate score
        score = 0
        total_questions = len(questions)

        for question in questions:
            answer = request.form.get(f'question_{question.id}')
            if answer and answer.upper() == question.correct_answer:
                score += 1

        # Calculate percentage
        percentage = (score / total_questions * 100) if total_questions > 0 else 0

        # Save result
        result = QuizResult(
            user_id=current_user.id,
            category_id=category_id,
            score=score,
            total_questions=total_questions,
            percentage=percentage
        )
        db.session.add(result)
        db.session.commit()

        flash('Quiz submitted successfully!', 'success')
        return redirect(url_for('quiz.results', result_id=result.id))

    return render_template('quiz/take.html', category=category, questions=questions)


@quiz.route('/result/<int:result_id>')
@quiz.route('/results/<int:result_id>')
@login_required
def results(result_id):
    """View quiz results."""
    result = QuizResult.query.get_or_404(result_id)

    # Verify result belongs to current user
    if result.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('quiz.list_categories'))

    category = Category.query.get(result.category_id)
    questions = Question.query.filter_by(category_id=result.category_id).all()

    return render_template('quiz/results.html',
                           result=result,
                           category=category,
                           questions=questions)


@quiz.route('/history')
@login_required
def history():
    """View user's quiz attempt history."""
    results = QuizResult.query.filter_by(user_id=current_user.id)\
        .order_by(QuizResult.taken_at.desc()).all()

    # Get category details for each result
    results_with_categories = []
    for result in results:
        category = Category.query.get(result.category_id)
        results_with_categories.append({
            'result': result,
            'category': category
        })

    return render_template('quiz/history.html', results_with_categories=results_with_categories)
