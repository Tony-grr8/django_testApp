from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from .models import *


def index(request: HttpRequest):
    if (request.POST):        
        new_recruit = Recruit(name=request.POST.get('name'), planet_id=Planets.objects.get(name=request.POST.get('planet')).id, age=request.POST.get('age'), email=request.POST.get('email'))
        new_recruit.save()       
        response = HttpResponseRedirect('/recruit/welcome/')
        response.set_cookie('user_id', f'{new_recruit.id}')
        response.set_cookie('q_id', '0')
        return response
    planets_list = Planets.objects.all()
    data = {'planets':planets_list}    
    return render(request, 'reg_form.html', context=data)

def questions(request):
    if request.method == 'POST':
        _qid = int(request.POST.get('qid'))
        _answer = request.POST.get('answer')
        if _answer == 'Yes':
            _answer = True
        else:
            _answer = False
        _rec_id = int(request.COOKIES.get('user_id'))
        _question = Questions.objects.get(id=_qid)         
        rec_ans = RecruitAnswers(recruitId=_rec_id, questionId=_qid, answer=_answer)
        rec_ans.save() 
        if _qid < Questions.objects.all().count():      
            _question = Questions.objects.get(id=_qid + 1)             
            return render(request, 'recruit/questions.html', context={'title': 'Questions', 'qid':_qid + 1, 'question': _question.question})
        else:
            _questions = [q.question for q in Questions.objects.all()]
            _answers = [a.answer for a in RecruitAnswers.objects.filter(recruitId=_rec_id)]
            _res_list = zip(_questions, _answers)
            _name = Recruit.objects.get(id=_rec_id).name
            return render(request, 'recruit/endTest.html', context={'title': 'Poll end', 'results': _res_list, 'name': _name})          

    if request.method == 'GET':
        _first_question = Questions.objects.get(id=1)        
        return render(request, 'recruit/questions.html', context={'title': 'Questions', 'qid':1, 'question': _first_question.question})

def welcome(request):
    _user_id = request.COOKIES.get('user_id')
    _rec_obj = Recruit.objects.get(id=int(_user_id))      
    return render(request, 'recruit/welcome.html', {'title': f'Welcome, {_rec_obj.name}', 'name': _rec_obj.name})

def sith(request):
    _sith_list = [sith for sith in Sith.objects.all()]
    # print(_sith_list)
    return render(request, 'recruit/sith.html', {'title': f'Introduce yourself', 'siths': _sith_list})

def showRecruits(request):
    if request.method == 'POST':        
        _sith_planet_id = Sith.objects.get(id=request.POST.get('sith_id')).planet.id             
        _rec_list = [rec for rec in Recruit.objects.filter(planet_id=_sith_planet_id, shadowHand=False)]
        _sith_sh_list = [sh for sh in Recruit.objects.filter(main_sith=Sith.objects.get(id=request.POST.get('sith_id')))]
        return render(request, 'recruit/showRecruits.html', {'title': f'Introduce yourself', 'rec_list': _rec_list, 'shadowHands': _sith_sh_list, 'sith_id': request.POST.get('sith_id')})

def showAnswers(request):
    if request.method == 'POST':
        _rec_id = request.POST.get('recruit_id')
        _questions = [q.question for q in Questions.objects.all()]
        _answers = [a.answer for a in RecruitAnswers.objects.filter(recruitId=_rec_id)]
        _res_list = zip(_questions, _answers)
        _name = Recruit.objects.get(id=_rec_id).name
        return render(request, 'recruit/endTest.html', context={'title': 'Answers', 'results': _res_list, 'name': _name, 'id': _rec_id, 'sith_id': request.POST.get('sith_id')})  

def shadowHand(request):
    if request.method == 'POST':
        _rec_id = request.POST.get('recruit_id')
        _sith_id = request.POST.get('sith_id')
        _name = Recruit.objects.get(id=_rec_id).name
        # Recruit.objects.filter(id=_rec_id).update(shadowHand=True, main_sith=Sith.objects.get(id=_sith_id))
        _rec = Recruit.objects.get(id=_rec_id)
        _rec.shadowHand = True
        _rec.main_sith.set(_sith_id)
        _rec.save()
        return render(request, 'recruit/shadowHand.html', context={'title': 'ShadowHand', 'name': _name, 'id': _rec_id}) 

        