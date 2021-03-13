from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from .models import *


def index(request: HttpRequest):
    if request.method == 'POST':
        _recruit_data = {
            'name': request.POST.get('name'),
            'planet_id': Planets.objects.get(name=request.POST.get('planet')).id,
            'age': request.POST.get('age'),
            'email': request.POST.get('email'),
        }        
        _new_recruit = Recruit(name=_recruit_data['name'], planet_id=_recruit_data['planet_id'], age=_recruit_data['age'], email=_recruit_data['email'])
        _new_recruit.save()       
        _response = HttpResponseRedirect('/recruit/welcome/')
        _response.set_cookie('user_id', f'{_new_recruit.id}')
        _response.set_cookie('q_id', '0')
        return _response
    elif request.method == 'GET':
        _planets_list = Planets.objects.all()
        _data = {'planets':_planets_list}    
        return render(request, 'reg_form.html', context=_data)

def questions(request: HttpRequest):
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
            return render(request, 'recruit/endTest.html', context={'title': 'Poll end', 'results': _res_list, 'name': _name, 'id': _rec_id})          

    if request.method == 'GET':
        _first_question = Questions.objects.get(id=1)        
        return render(request, 'recruit/questions.html', context={'title': 'Questions', 'qid':1, 'question': _first_question.question})

def welcome(request: HttpRequest):
    _user_id = request.COOKIES.get('user_id')
    _rec_obj = Recruit.objects.get(id=int(_user_id))      
    return render(request, 'recruit/welcome.html', {'title': f'Welcome, {_rec_obj.name}', 'name': _rec_obj.name})

def sith(request: HttpRequest):
    _siths_list = [sith for sith in Sith.objects.all()]  
    _dict_sith_sh_count = {} 
    for sith in _siths_list:
        _dict_sith_sh_count[sith.name] = Recruit.objects.filter(main_sith=sith.id).count()
    print(_dict_sith_sh_count)        
    return render(request, 'recruit/sith.html', {'title': f'Introduce yourself', 'siths': _siths_list, 'dict_siths_sh_counter':_dict_sith_sh_count})

def showRecruits(request: HttpRequest):
    if request.method == 'POST':        
        _sith_planet_id = Sith.objects.get(id=request.POST.get('sith_id')).planet.id             
        _rec_list = [rec for rec in Recruit.objects.filter(planet_id=_sith_planet_id, shadowHand=False)]
        _sith_sh_list = [sh for sh in Recruit.objects.filter(main_sith=Sith.objects.get(id=request.POST.get('sith_id')))]
        context = {
            'title': 'Introduce yourself',
            'rec_list': _rec_list,
            'shadowHands': _sith_sh_list,
            'sith_id': request.POST.get('sith_id'),
           }
        return render(request, 'recruit/showRecruits.html', context=context)

def showAnswers(request: HttpRequest):
    if request.method == 'POST':
        _rec_id = request.POST.get('recruit_id')
        _questions = [q.question for q in Questions.objects.all()]
        _answers = [a.answer for a in RecruitAnswers.objects.filter(recruitId=_rec_id)]
        _res_list = zip(_questions, _answers)
        _name = Recruit.objects.get(id=_rec_id).name
        _rec_count = Recruit.objects.filter(main_sith=request.POST.get('sith_id')).count()
        context = {
            'title': 'Answers',
            'results': _res_list,
            'name': _name,
            'id': _rec_id,
            'sith_id': request.POST.get('sith_id'),
            'rec_count': _rec_count
            }       
        return render(request, 'recruit/endTest.html', context=context)  

def shadowHand(request: HttpRequest):
    if request.method == 'POST':
        _rec_count = Recruit.objects.filter(main_sith=request.POST.get('sith_id')).count()
        if _rec_count < 3:
            _rec_id = request.POST.get('recruit_id')
            _sith_id = request.POST.get('sith_id')               
            _rec = Recruit.objects.get(id=_rec_id)
            _name = _rec.name
            _rec.shadowHand = True
            _rec.main_sith.set(_sith_id)
            _rec.save()
            # send_mail('Django mail', 'This e-mail was sent with Django.', 'your@gmail.com', [f'{_rec.email}'], fail_silently=False)
            return render(request, 'recruit/shadowHand.html', context={'title': 'ShadowHand', 'name': _name, 'id': _rec_id}) 
        else:
            return render(request, 'recruit/shadowHand.html', context={'title': 'ShadowHand', })             

        