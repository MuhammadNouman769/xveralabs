from .forms import ChatForm
from .models import Budget


def chat_form(request):
    """Makes the chat sidebar form (and its dropdown/checkbox data) available on every page."""
    steps = [[v, l] for v, l in Budget.choices if v != Budget.NOT_SURE]
    return {
        "chat_form": ChatForm(auto_id="cf-%s"),
        "chat_budget_steps": steps,
    }