"""
Seed Data Script for Placement Preparation Portal
==================================================
This script populates the database with:
- Admin user
- Sample categories (Aptitude and Technical)
- Sample questions for each category
- Sample resources

Run this script after initializing the database:
    python seed_data.py
"""

from app import create_app, db
from app.models import User, Category, Question, Resource, StudentActivity
from datetime import datetime


def create_admin_user():
    """Create the default admin user."""
    # Check if admin already exists
    admin = User.query.filter_by(email='admin@college.edu').first()
    if admin:
        print("Admin user already exists.")
        return admin

    admin = User(
        name='Admin User',
        email='admin@college.edu',
        role='admin',
        college='Placement Portal'
    )
    admin.set_password('admin123')

    db.session.add(admin)
    db.session.commit()
    print("Admin user created: admin@college.edu / admin123")
    return admin


def create_categories():
    """Create sample quiz categories."""
    categories_data = [
        {
            'name': 'Quantitative Aptitude',
            'type': 'aptitude',
            'description': 'Test your numerical ability and mathematical skills. Covers topics like arithmetic, algebra, geometry, and data interpretation.'
        },
        {
            'name': 'Logical Reasoning',
            'type': 'aptitude',
            'description': 'Evaluate your logical thinking and analytical abilities. Includes puzzles, seating arrangements, and pattern recognition.'
        },
        {
            'name': 'Verbal Ability',
            'type': 'aptitude',
            'description': 'Assess your English language skills including reading comprehension, grammar, vocabulary, and verbal reasoning.'
        },
        {
            'name': 'Python Programming',
            'type': 'technical',
            'description': 'Test your Python programming knowledge including syntax, data structures, OOP concepts, and common libraries.'
        },
        {
            'name': 'Data Structures',
            'type': 'technical',
            'description': 'Evaluate your understanding of fundamental data structures like arrays, linked lists, trees, graphs, and hash tables.'
        },
        {
            'name': 'SQL & Databases',
            'type': 'technical',
            'description': 'Test your database knowledge including SQL queries, normalization, indexing, and database design concepts.'
        },
        {
            'name': 'Operating Systems',
            'type': 'technical',
            'description': 'Assess your understanding of OS concepts like processes, threads, memory management, and file systems.'
        },
        {
            'name': 'Computer Networks',
            'type': 'technical',
            'description': 'Test your networking knowledge including OSI model, TCP/IP, protocols, and network security basics.'
        }
    ]

    created_categories = []
    for cat_data in categories_data:
        # Check if category already exists
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if existing:
            print(f"Category '{cat_data['name']}' already exists.")
            created_categories.append(existing)
            continue

        category = Category(
            name=cat_data['name'],
            type=cat_data['type'],
            description=cat_data['description']
        )
        db.session.add(category)
        created_categories.append(category)

    db.session.commit()
    print(f"Created {len([c for c in created_categories if c.name in [d['name'] for d in categories_data]])} categories.")
    return created_categories


def create_questions(categories):
    """Create sample questions for each category."""
    questions_data = {
        'Quantitative Aptitude': [
            {
                'question_text': 'If a number is increased by 20% and then decreased by 20%, what is the net percentage change?',
                'option_a': '0%',
                'option_b': '4% decrease',
                'option_c': '4% increase',
                'option_d': '2% decrease',
                'correct_answer': 'B',
                'explanation': 'Let the number be 100. After 20% increase: 120. After 20% decrease: 120 - 24 = 96. Net change = -4% (4% decrease)',
                'difficulty': 'easy'
            },
            {
                'question_text': 'A train 200m long is running at 72 km/h. In how much time will it cross a pole?',
                'option_a': '8 seconds',
                'option_b': '10 seconds',
                'option_c': '12 seconds',
                'option_d': '15 seconds',
                'correct_answer': 'B',
                'explanation': 'Speed = 72 km/h = 20 m/s. Time = Distance/Speed = 200/20 = 10 seconds',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the sum of first 50 natural numbers?',
                'option_a': '1225',
                'option_b': '1275',
                'option_c': '1325',
                'option_d': '1375',
                'correct_answer': 'B',
                'explanation': 'Sum = n(n+1)/2 = 50 * 51 / 2 = 1275',
                'difficulty': 'easy'
            },
            {
                'question_text': 'If A:B = 3:4 and B:C = 5:6, then A:B:C is:',
                'option_a': '15:20:24',
                'option_b': '3:5:6',
                'option_c': '15:25:24',
                'option_d': '12:16:20',
                'correct_answer': 'A',
                'explanation': 'A:B = 3:4 = 15:20, B:C = 5:6 = 20:24. So A:B:C = 15:20:24',
                'difficulty': 'medium'
            },
            {
                'question_text': 'A can do a work in 12 days and B can do the same work in 18 days. In how many days can they complete the work together?',
                'option_a': '6.2 days',
                'option_b': '7.2 days',
                'option_c': '8.2 days',
                'option_d': '9.2 days',
                'correct_answer': 'B',
                'explanation': 'Combined work = 1/12 + 1/18 = 5/36 per day. Total days = 36/5 = 7.2 days',
                'difficulty': 'medium'
            }
        ],
        'Logical Reasoning': [
            {
                'question_text': 'If COMPUTER is coded as RFUVQNPC, how is MEDICINE coded?',
                'option_a': 'MFEJDJOF',
                'option_b': 'ENICIDME',
                'option_c': 'FOJDJEFM',
                'option_d': 'MEDICINF',
                'correct_answer': 'C',
                'explanation': 'The word is reversed and each letter is shifted by +1. MEDICINE reversed = ENICIDEM, shifted = FOJDJEFM',
                'difficulty': 'hard'
            },
            {
                'question_text': 'Find the next number in the series: 2, 6, 12, 20, 30, ?',
                'option_a': '38',
                'option_b': '40',
                'option_c': '42',
                'option_d': '44',
                'correct_answer': 'C',
                'explanation': 'Pattern: 1*2=2, 2*3=6, 3*4=12, 4*5=20, 5*6=30, 6*7=42',
                'difficulty': 'easy'
            },
            {
                'question_text': 'All roses are flowers. Some flowers are red. Therefore:',
                'option_a': 'All roses are red',
                'option_b': 'Some roses are red',
                'option_c': 'No rose is red',
                'option_d': 'None of the above necessarily follows',
                'correct_answer': 'D',
                'explanation': 'From the given statements, we cannot determine if any roses are red. The roses could all be of other colors.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'If A is the brother of B, B is the sister of C, and C is the father of D, how is A related to D?',
                'option_a': 'Uncle',
                'option_b': 'Nephew',
                'option_c': 'Cousin',
                'option_d': 'Grandfather',
                'correct_answer': 'A',
                'explanation': 'A is brother of B, B is sister of C, so A and B are siblings of C. C is father of D, so A is uncle of D.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'In a row of students, Ram is 7th from left and Shyam is 12th from right. If they interchange, Ram becomes 22nd from left. How many students are in the row?',
                'option_a': '31',
                'option_b': '32',
                'option_c': '33',
                'option_d': '34',
                'correct_answer': 'C',
                'explanation': 'After interchange, Ram is at Shyam\'s position which is 22nd from left. Shyam was 12th from right. Total = 22 + 12 - 1 = 33',
                'difficulty': 'hard'
            }
        ],
        'Verbal Ability': [
            {
                'question_text': 'Choose the synonym of "EPHEMERAL":',
                'option_a': 'Eternal',
                'option_b': 'Transient',
                'option_c': 'Permanent',
                'option_d': 'Everlasting',
                'correct_answer': 'B',
                'explanation': 'Ephemeral means lasting for a very short time, so transient is the synonym.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Choose the correct meaning of the idiom "Bite the bullet":',
                'option_a': 'To eat quickly',
                'option_b': 'To face a difficult situation bravely',
                'option_c': 'To be aggressive',
                'option_d': 'To make a mistake',
                'correct_answer': 'B',
                'explanation': '"Bite the bullet" means to endure a painful or difficult situation with courage.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Select the correct sentence:',
                'option_a': 'Neither the students nor the teacher were present',
                'option_b': 'Neither the students nor the teacher was present',
                'option_c': 'Neither the student nor the teachers was present',
                'option_d': 'Neither students nor teacher were present',
                'correct_answer': 'B',
                'explanation': 'When using "neither...nor", the verb agrees with the noun closest to it. Here "teacher" is singular, so "was" is correct.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Choose the antonym of "BENEVOLENT":',
                'option_a': 'Kind',
                'option_b': 'Generous',
                'option_c': 'Malevolent',
                'option_d': 'Caring',
                'correct_answer': 'C',
                'explanation': 'Benevolent means well-meaning and kindly. Malevolent means having evil intentions.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'The word "UBIQUITOUS" means:',
                'option_a': 'Rare',
                'option_b': 'Present everywhere',
                'option_c': 'Unique',
                'option_d': 'Ancient',
                'correct_answer': 'B',
                'explanation': 'Ubiquitous means present, appearing, or found everywhere.',
                'difficulty': 'medium'
            }
        ],
        'Python Programming': [
            {
                'question_text': 'What is the output of: print(type([]))?',
                'option_a': "<class 'tuple'>",
                'option_b': "<class 'list'>",
                'option_c': "<class 'dict'>",
                'option_d': "<class 'set'>",
                'correct_answer': 'B',
                'explanation': '[] creates an empty list in Python, so type([]) returns <class \'list\'>',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which of the following is NOT a valid Python data type?',
                'option_a': 'list',
                'option_b': 'tuple',
                'option_c': 'array',
                'option_d': 'frozenset',
                'correct_answer': 'C',
                'explanation': 'Python has list, tuple, and frozenset as built-in types. Array is from the array module, not a built-in type.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the output of: print(2 ** 3 ** 2)?',
                'option_a': '64',
                'option_b': '512',
                'option_c': '36',
                'option_d': '81',
                'correct_answer': 'B',
                'explanation': 'Exponentiation is right-associative. 2 ** 3 ** 2 = 2 ** (3 ** 2) = 2 ** 9 = 512',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which keyword is used to create a generator function?',
                'option_a': 'return',
                'option_b': 'yield',
                'option_c': 'generate',
                'option_d': 'async',
                'correct_answer': 'B',
                'explanation': 'The yield keyword is used to create generator functions in Python.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is a decorator in Python?',
                'option_a': 'A function that modifies another function',
                'option_b': 'A design pattern for classes',
                'option_c': 'A type of comment',
                'option_d': 'A variable naming convention',
                'correct_answer': 'A',
                'explanation': 'A decorator is a function that takes another function and extends its behavior without modifying it explicitly.',
                'difficulty': 'hard'
            }
        ],
        'Data Structures': [
            {
                'question_text': 'What is the time complexity of searching an element in a balanced BST?',
                'option_a': 'O(1)',
                'option_b': 'O(n)',
                'option_c': 'O(log n)',
                'option_d': 'O(n log n)',
                'correct_answer': 'C',
                'explanation': 'In a balanced BST, each comparison eliminates half of the remaining nodes, giving O(log n) complexity.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which data structure uses LIFO principle?',
                'option_a': 'Queue',
                'option_b': 'Stack',
                'option_c': 'Linked List',
                'option_d': 'Tree',
                'correct_answer': 'B',
                'explanation': 'Stack follows Last In First Out (LIFO) principle where the last element added is removed first.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the worst-case time complexity of QuickSort?',
                'option_a': 'O(n)',
                'option_b': 'O(n log n)',
                'option_c': 'O(n^2)',
                'option_d': 'O(log n)',
                'correct_answer': 'C',
                'explanation': 'QuickSort has O(n^2) worst-case when the pivot is always the smallest or largest element.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'In a hash table, what is a collision?',
                'option_a': 'Two keys hash to the same index',
                'option_b': 'The table is full',
                'option_c': 'Invalid key type',
                'option_d': 'Memory overflow',
                'correct_answer': 'A',
                'explanation': 'A collision occurs when two different keys produce the same hash value and map to the same index.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the space complexity of a recursive implementation of factorial?',
                'option_a': 'O(1)',
                'option_b': 'O(n)',
                'option_c': 'O(n^2)',
                'option_d': 'O(log n)',
                'correct_answer': 'B',
                'explanation': 'Recursive factorial uses O(n) stack space for n recursive calls.',
                'difficulty': 'medium'
            }
        ],
        'SQL & Databases': [
            {
                'question_text': 'Which SQL command is used to remove all records from a table without removing the table itself?',
                'option_a': 'DELETE',
                'option_b': 'DROP',
                'option_c': 'TRUNCATE',
                'option_d': 'REMOVE',
                'correct_answer': 'C',
                'explanation': 'TRUNCATE removes all rows from a table without logging individual row deletions. It\'s faster than DELETE.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What type of JOIN returns all rows when there is a match in either table?',
                'option_a': 'INNER JOIN',
                'option_b': 'LEFT JOIN',
                'option_c': 'RIGHT JOIN',
                'option_d': 'FULL OUTER JOIN',
                'correct_answer': 'D',
                'explanation': 'FULL OUTER JOIN returns all rows when there is a match in either the left or right table.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which normal form deals with eliminating partial dependencies?',
                'option_a': '1NF',
                'option_b': '2NF',
                'option_c': '3NF',
                'option_d': 'BCNF',
                'correct_answer': 'B',
                'explanation': '2NF deals with eliminating partial dependencies, where non-key attributes depend on only part of a composite key.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is an ACID property in databases?',
                'option_a': 'A type of query',
                'option_b': 'A database indexing method',
                'option_c': 'Properties ensuring reliable transactions',
                'option_d': 'A backup strategy',
                'correct_answer': 'C',
                'explanation': 'ACID (Atomicity, Consistency, Isolation, Durability) are properties that guarantee reliable transaction processing.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which index type is best for range queries?',
                'option_a': 'Hash Index',
                'option_b': 'B-Tree Index',
                'option_c': 'Bitmap Index',
                'option_d': 'Full-text Index',
                'correct_answer': 'B',
                'explanation': 'B-Tree indexes maintain sorted order and support efficient range queries, unlike hash indexes.',
                'difficulty': 'hard'
            }
        ],
        'Operating Systems': [
            {
                'question_text': 'What is a deadlock in operating systems?',
                'option_a': 'A process waiting for I/O',
                'option_b': 'Two or more processes waiting indefinitely for resources held by each other',
                'option_c': 'System crash',
                'option_d': 'Memory overflow',
                'correct_answer': 'B',
                'explanation': 'Deadlock occurs when two or more processes are waiting indefinitely for resources held by each other.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which scheduling algorithm is preemptive?',
                'option_a': 'First Come First Serve',
                'option_b': 'Shortest Job First',
                'option_c': 'Round Robin',
                'option_d': 'Non-preemptive Priority',
                'correct_answer': 'C',
                'explanation': 'Round Robin is preemptive as it allocates a fixed time quantum to each process.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is thrashing?',
                'option_a': 'High CPU utilization',
                'option_b': 'Excessive paging causing system slowdown',
                'option_c': 'Disk fragmentation',
                'option_d': 'Network congestion',
                'correct_answer': 'B',
                'explanation': 'Thrashing occurs when the system spends more time paging than executing applications.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'What is the purpose of virtual memory?',
                'option_a': 'To increase RAM speed',
                'option_b': 'To allow execution of processes larger than physical memory',
                'option_c': 'To speed up disk access',
                'option_d': 'To create backup copies',
                'correct_answer': 'B',
                'explanation': 'Virtual memory allows programs to use more memory than physically available by using disk space.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'Which of the following is NOT a process state?',
                'option_a': 'Ready',
                'option_b': 'Running',
                'option_c': 'Sleeping',
                'option_d': 'Blocked',
                'correct_answer': 'C',
                'explanation': 'The basic process states are New, Ready, Running, Blocked/Waiting, and Terminated. Sleeping is not a standard state.',
                'difficulty': 'medium'
            }
        ],
        'Computer Networks': [
            {
                'question_text': 'Which layer of the OSI model is responsible for routing?',
                'option_a': 'Data Link Layer',
                'option_b': 'Network Layer',
                'option_c': 'Transport Layer',
                'option_d': 'Session Layer',
                'correct_answer': 'B',
                'explanation': 'The Network Layer (Layer 3) is responsible for logical addressing and routing.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What protocol is used for secure web browsing?',
                'option_a': 'HTTP',
                'option_b': 'FTP',
                'option_c': 'HTTPS',
                'option_d': 'SMTP',
                'correct_answer': 'C',
                'explanation': 'HTTPS (HTTP Secure) uses TLS/SSL to encrypt web traffic for secure communication.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the default subnet mask for a Class C IP address?',
                'option_a': '255.0.0.0',
                'option_b': '255.255.0.0',
                'option_c': '255.255.255.0',
                'option_d': '255.255.255.255',
                'correct_answer': 'C',
                'explanation': 'Class C addresses use 255.255.255.0 as the default subnet mask, allowing 254 host addresses.',
                'difficulty': 'medium'
            },
            {
                'question_text': 'Which protocol uses port 80 by default?',
                'option_a': 'HTTPS',
                'option_b': 'FTP',
                'option_c': 'HTTP',
                'option_d': 'SSH',
                'correct_answer': 'C',
                'explanation': 'HTTP (Hypertext Transfer Protocol) uses port 80 by default for unencrypted web traffic.',
                'difficulty': 'easy'
            },
            {
                'question_text': 'What is the purpose of DNS?',
                'option_a': 'File transfer',
                'option_b': 'Email delivery',
                'option_c': 'Domain name to IP address translation',
                'option_d': 'Network security',
                'correct_answer': 'C',
                'explanation': 'DNS (Domain Name System) translates human-readable domain names to IP addresses.',
                'difficulty': 'easy'
            }
        ]
    }

    total_questions = 0
    for category in categories:
        if category.name in questions_data:
            for q_data in questions_data[category.name]:
                # Check if question already exists
                existing = Question.query.filter_by(
                    question_text=q_data['question_text'],
                    category_id=category.id
                ).first()
                if existing:
                    continue

                question = Question(
                    category_id=category.id,
                    question_text=q_data['question_text'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data['explanation'],
                    difficulty=q_data['difficulty']
                )
                db.session.add(question)
                total_questions += 1

    db.session.commit()
    print(f"Created {total_questions} questions.")
    return total_questions


def create_resources():
    """Create sample resources."""
    resources_data = [
        {
            'title': 'Interview Preparation Tips',
            'description': 'Comprehensive guide for campus placement interviews including common questions and best practices.',
            'resource_type': 'interview_tip',
            'content': '''# Interview Preparation Tips

## Before the Interview
1. Research the company thoroughly
2. Practice common interview questions
3. Prepare your resume and documents
4. Dress professionally

## During the Interview
1. Be confident and maintain eye contact
2. Listen carefully to questions
3. Provide structured answers (STAR method)
4. Ask relevant questions about the role

## After the Interview
1. Send a thank-you email
2. Follow up if you haven\'t heard back
3. Reflect on your performance for improvement''',
            'link': None
        },
        {
            'title': 'Common HR Questions and Answers',
            'description': 'List of frequently asked HR interview questions with suggested answer approaches.',
            'resource_type': 'hr_question',
            'content': '''# Common HR Questions

## Tell me about yourself
Keep it professional and relevant to the job. Cover your education, experience, and key achievements.

## Why do you want to work here?
Research the company and mention specific aspects that appeal to you.

## What are your strengths and weaknesses?
Be honest but strategic. For weaknesses, mention how you\'re working to improve.

## Where do you see yourself in 5 years?
Show ambition but be realistic and align with the company\'s growth path.

## Why should we hire you?
Highlight your unique skills and how they match the job requirements.''',
            'link': None
        },
        {
            'title': 'Data Structures and Algorithms Practice',
            'description': 'Useful resources for practicing DSA problems for technical interviews.',
            'resource_type': 'coding_link',
            'content': None,
            'link': 'https://leetcode.com'
        },
        {
            'title': 'Resume Writing Guide',
            'description': 'Best practices for creating an effective resume for campus placements.',
            'resource_type': 'notes',
            'content': '''# Resume Writing Guide

## Key Sections
1. **Header**: Name, contact info, LinkedIn/GitHub
2. **Summary**: Brief professional overview
3. **Education**: Degree, college, GPA, relevant coursework
4. **Skills**: Technical and soft skills
5. **Projects**: Brief description with technologies used
6. **Experience**: Internships and work experience

## Tips
- Keep it to 1-2 pages
- Use action verbs
- Quantify achievements
- Tailor for each application
- Proofread carefully''',
            'link': None
        },
        {
            'title': 'Group Discussion Tips',
            'description': 'How to perform well in group discussions during campus placements.',
            'resource_type': 'notes',
            'content': '''# Group Discussion Tips

## Do\'s
- Initiate the discussion if you\'re confident
- Listen actively to others
- Support your points with examples
- Allow others to speak
- Summarize key points

## Don\'ts
- Don\'t interrupt others
- Don\'t dominate the discussion
- Don\'t get aggressive
- Don\'t go off-topic
- Don\'t remain silent''',
            'link': None
        },
        {
            'title': 'Python Programming Resources',
            'description': 'Useful links and resources for Python programming practice.',
            'resource_type': 'coding_link',
            'content': None,
            'link': 'https://www.hackerrank.com/domains/python'
        }
    ]

    total_resources = 0
    for res_data in resources_data:
        # Check if resource already exists
        existing = Resource.query.filter_by(title=res_data['title']).first()
        if existing:
            continue

        resource = Resource(
            title=res_data['title'],
            description=res_data['description'],
            resource_type=res_data['resource_type'],
            content=res_data['content'],
            link=res_data['link']
        )
        db.session.add(resource)
        total_resources += 1

    db.session.commit()
    print(f"Created {total_resources} resources.")
    return total_resources


def main():
    """Main function to seed the database."""
    print("=" * 50)
    print("Seeding Placement Portal Database")
    print("=" * 50)

    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        print("\n1. Creating admin user...")
        create_admin_user()

        print("\n2. Creating categories...")
        categories = create_categories()

        print("\n3. Creating questions...")
        create_questions(categories)

        print("\n4. Creating resources...")
        create_resources()

        print("\n" + "=" * 50)
        print("Database seeding completed!")
        print("=" * 50)
        print("\nYou can now login with:")
        print("  Email: admin@college.edu")
        print("  Password: admin123")


if __name__ == '__main__':
    main()
