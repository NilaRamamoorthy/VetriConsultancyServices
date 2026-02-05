from .models import ChatbotFAQ

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

def get_greeting_message(user=None):
    if user and user.is_authenticated:
        name = (
            getattr(user.profile, 'first_name', '') 
            or getattr(user.consultant_profile, 'first_name', '') 
            or user.email
        )

        if hasattr(user, 'subscription') and user.subscription.is_pro():
            return f"👋 Hi {name}! Welcome back 🌟 You’re a Pro member. How can I help you today?"
        else:
            return f"👋 Hi {name}! Welcome to Vetri Consultancy. How can I help you today?"

    return "👋 Hi there! Welcome to Vetri Consultancy. How can I help you today?"
