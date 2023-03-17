from datetime import date
from .models import activity, Activity_Counter
def utilities(request):
    context = {}
    if request.user.is_authenticated:
        context['notification'] = activity.objects.filter(user = request.user).order_by('-id')[:8]
        if Activity_Counter.objects.filter(user = request.user).exists():
            context['notcount'] = Activity_Counter.objects.get(user = request.user)
    return context

