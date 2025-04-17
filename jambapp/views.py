from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django.template.loader import render_to_string
import requests
from dotenv import load_dotenv
from . import questions


load_dotenv()
secret_key = os.getenv('SECRET_KEY')

def home(request):
    return render(request, 'home.html')

def chapter1(request):
    quizzes = questions.questions_data
    return render(request, 'chapter1.html', {'quizzes': quizzes})

def chapter2(request):
    quizzes = questions.questions_data_2
    return render(request, 'chapter2.html', {'quizzes': quizzes})

def check_transaction_status(request, transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {secret_key}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def send_study_questions(request, email):

    quiz_emails =[
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 3 (Migration Tales).',
        'questions': questions.questions_data_3
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 4 (A Case of Visa Denied).',
        'questions': questions.questions_data_4
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 5 (Snake in the Roof).',
        'questions': questions.questions_data_5
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 6 (Ade as Well as Jide COMES vs COME).',
        'questions': questions.questions_data_6
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 7 (Ritualists).',
        'questions': questions.questions_data_7
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 8 (Mission Unaccomplished).',
        'questions': questions.questions_data_8
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 9 (Laughing Waterfalls).',
        'questions': questions.questions_data_9
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 10 (Passport Pains).',
        'questions': questions.questions_data_10
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 11 (Point of No Return).',
        'questions': questions.questions_data_11
    },
    {
        'title': 'The Lekki Headmaster Study Questions Chapter 12 (...Dawn).',
        'questions': questions.questions_data_12
    },
    
    ]
    
    connection = get_connection()
    connection.open()

    for email in quiz_emails:
        quiz_email_to_send = EmailMultiAlternatives(
                        str(email['title']),
                        '',
                        str(settings.DEFAULT_FROM_EMAIL),
                        [str(email)],
                        reply_to=['munenoreply@mail.com'],
                        connection=connection
                    )
        html_page = render_to_string('quizpage.html', {'quizzes': email['questions']})
        quiz_email_to_send.attach_alternative(html_page, 'text/html')
        quiz_email_to_send.send(fail_silently=False)

    connection.close()
    return HttpResponse(f'Email sent successfully to {email}')

def store_cookie(request, email, transaction_id):
    request.session.__setitem__('transaction_id', str(transaction_id))
    request.session.__setitem__('client_email', str(email))
    return redirect("/verify/")

def activate_order(request):
    transaction_id = request.session.__getitem__('transaction_id')
    email = request.session.__getitem__('client_email')
    transaction_id = int(transaction_id)
    email = str(email)
    request.session.__delitem__('transaction_id')
    request.session.__delitem__('client_email')
    if not transaction_id:
        return HttpResponse('Transaction ID missing!')
    transaction_data = check_transaction_status(request, transaction_id)

    if transaction_data:
        if str(transaction_data['status']).lower() == 'success' and str(transaction_data['data']['status']).lower() == 'successful':
            email_value = send_study_questions(request, email)
            print(email_value)
            return render(request, 'paymentsuccess.html', {'email': email})
        elif str(transaction_data['data']['status']).lower() == 'failed':
            return render(request, 'paymentfailed.html', {'email': email})
        else:
            return render(request, 'paymentprocessing.html', {'email': email})
    return HttpResponse('No transaction data!')
