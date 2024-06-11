from django.shortcuts import render, get_object_or_404
from home.models import problem
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.


def ProblemDisplay(request):
    problems = problem.objects.all()
    print(problems)

    context = {"problems": problems}
    return render(request, "index.html", context)


def problem_detail(request, pk):
    problems = problem.objects.get(id=pk)
    template = loader.get_template('problem_details.html')
    context = {
        'problems': problems
    }
    return HttpResponse(template.render(context, request))
    # return render(request, "problem_display", {'problems': problems})
