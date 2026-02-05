from .models import ChatbotFAQ
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import get_bot_response
import json


def get_bot_response(user_message):
    user_message = user_message.lower()

    faqs = ChatbotFAQ.objects.all()

    for faq in faqs:
        keywords = [k.strip().lower() for k in faq.keywords.split(',')]

        for keyword in keywords:
            if keyword in user_message:
                return faq.answer

    return (
        "Sorry, I couldn't find an answer for that. "
        "Please contact support or try asking differently."
    )


@csrf_exempt
def chatbot_reply(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        reply = get_bot_response(message)

        return JsonResponse({'reply': reply})

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .utils import get_bot_response

@login_required
@csrf_exempt
def ask_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        bot_reply = get_bot_response(user_message)
        return JsonResponse({'response': bot_reply})
    return JsonResponse({'response': 'Invalid request'})


from django.http import JsonResponse
from .utils import get_greeting_message

def chatbot_greeting_view(request):
    message = get_greeting_message(request.user)
    return JsonResponse({"message": message})
