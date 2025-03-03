from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import requests
from dotenv import load_dotenv


load_dotenv()
secret_key = os.getenv('SECRET_KEY')

def home(request):
    return render(request, 'home.html')

def chapter1(request):
    quizzes = [
        {
         'id': 1,
         'question': '2 + 3 x (4 / 1)',
         'o1': 29,
         'o2': 87,
         'o3': 19,
         'ans': 'o1'
        },
        {
         'id': 2,
         'question': '2 + 29 = 31',
         'o1': 'True',
         'o2': 'False',
         'o3': 'Maybe',
         'ans': 'o2'
        }
    ]
    return render(request, 'chapter1.html', {'quizzes': quizzes})

def chapter2(request):
    quizzes = [
        {
         'id': 1,
         'question': '2 + 3 x (4 / 1)',
         'o1': 29,
         'o2': 87,
         'o3': 19,
         'ans': 'o1'
        },
        {
         'id': 2,
         'question': '2 + 29 = 31',
         'o1': 'True',
         'o2': 'False',
         'o3': 'Maybe',
         'ans': 'o2'
        }
    ]
    return render(request, 'chapter2.html', {'quizzes': quizzes})


def check_transaction_status(request, transaction_id):
    print(secret_key)
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {secret_key}",
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    return None

def send_study_questions(request, email):
    quizzes = [
        {
         'id': 1,
         'question': '2 + 3 x (4 / 1)',
         'o1': 29,
         'o2': 87,
         'o3': 19,
         'ans': 'o1'
        },
        {
         'id': 2,
         'question': '2 + 29 = 31',
         'o1': 'True',
         'o2': 'False',
         'o3': 'Maybe',
         'ans': 'o2'
        },
        {
         'id': 1,
         'question': '2 + 3 x (4 / 1)',
         'o1': 29,
         'o2': 87,
         'o3': 19,
         'ans': 'o1'
        },
        {
         'id': 2,
         'question': '2 + 29 = 31',
         'o1': 'True',
         'o2': 'False',
         'o3': 'Maybe',
         'ans': 'o2'
        },
        {
         'id': 1,
         'question': '2 + 3 x (4 / 1)',
         'o1': 29,
         'o2': 87,
         'o3': 19,
         'ans': 'o1'
        },
        {
         'id': 2,
         'question': '2 + 29 = 31',
         'o1': 'True',
         'o2': 'False',
         'o3': 'Maybe',
         'ans': 'o2'
        }
    ]
    payment_success_mail = EmailMultiAlternatives(
                    'The Lekki Headmaster Study Questions Chapter 1',
                    '',
                    str(settings.DEFAULT_FROM_EMAIL),
                    [str(email)],
                    reply_to=['munenoreply@mail.com']
                )
    html_page = render_to_string('quizpage.html', {'quizzes': quizzes})
    payment_success_mail.attach_alternative(html_page, 'text/html')
    payment_success_mail.send(fail_silently=False)
    return None


def store_cookie(request, email, transaction_id):
    request.session.__setitem__('transaction_id', str(transaction_id))
    request.session.__setitem__('client_email', str(email))
    return redirect("/verify/")

def activate_order(request):
    transaction_id = request.session.__getitem__('transaction_id')
    email = request.session.__getitem__('client_email')
    transaction_id = int(transaction_id)
    email = str(email)
    # request.session.__delitem__('transaction_id')
    # request.session.__delitem__('client_email')
    print(transaction_id, email)
    if not transaction_id:
        return HttpResponse('Transaction ID missing!')
    transaction_data = check_transaction_status(request, transaction_id)
    print('TRANSACTION DATA: ', transaction_data)

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
