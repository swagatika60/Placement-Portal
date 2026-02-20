"""
SQLAlchemy Models for Placement Preparation Portal
===================================================
This module contains all database models for the placement portal including
User management, Quiz system, Resources, and Activity tracking.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """
    User model for authentication and user management.
    Supports both student and admin roles.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')  # 'student' or 'admin'
    college = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    quiz_results = db.relationship('QuizResult', backref='user', lazy='dynamic')
    resources = db.relationship('Resource', backref='author', lazy='dynamic')
    activities = db.relationship('StudentActivity', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Hash and set the password for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name} ({self.email})>'


class Category(db.Model):
    """
    Category model for organizing questions.
    Supports aptitude and technical categories.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # 'aptitude' or 'technical'
    description = db.Column(db.Text)

    # Relationships
    questions = db.relationship('Question', backref='category', lazy='dynamic',
                               cascade='all, delete-orphan')
    quiz_results = db.relationship('QuizResult', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'


class Question(db.Model):
    """
    Question model for quiz questions.
    Supports multiple choice questions with 4 options.
    """
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_answer = db.Column(db.String(1))  # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # 'easy', 'medium', 'hard'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'


class QuizResult(db.Model):
    """
    QuizResult model for tracking user quiz performance.
    Stores score, total questions, and percentage for each quiz attempt.
    """
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QuizResult User:{self.user_id} Score:{self.score}/{self.total_questions}>'


class Resource(db.Model):
    """
    Resource model for placement preparation materials.
    Supports various resource types like interview tips, HR questions, etc.
    """
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50))  # 'interview_tip', 'hr_question', 'coding_link', 'notes'
    content = db.Column(db.Text)
    link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Resource {self.title} ({self.resource_type})>'


class StudentActivity(db.Model):
    """
    StudentActivity model for tracking user activities.
    Logs various user actions like login, quiz attempts, and resource views.
    """
    __tablename__ = 'student_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50))  # 'login', 'quiz', 'resource_view'
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StudentActivity User:{self.user_id} Type:{self.activity_type}>'
