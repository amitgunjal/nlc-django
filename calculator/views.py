from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from calculator import utilities

def home(request):
    submission = request.POST.get('user-input', '')
    output = utilities.process_string(submission)
    if output is None:
        outstring = 'Unable to evaluate your input. Please try again.'
    else:
        outstring = output
    c = {
        'submission': submission,
        'evaluation': outstring,
    }
    c.update(csrf(request))
    return render_to_response("calc.html", c)