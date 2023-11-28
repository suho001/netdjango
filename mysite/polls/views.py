# views.py
from django.shortcuts import render
from polls.models import  Question
from django.shortcuts import render, get_object_or_404
from polls.models import Question,Choice
from django.http import HttpResponseRedirect
from polls.forms import NameForm

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html',context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/detail.html',{question:question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html'),{
            'question':question,
            'error_message':"You didn't select a choice",
        }
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

    def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html',{'question':question})


def name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            new_name = form.cleaned_data['name']
            return HttpResponseRedirect('')

    else:
        form = NameForm()
        return render(request, 'polls/name.html',{'form':form})