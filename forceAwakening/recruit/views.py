from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from .models import *


def index(request: HttpRequest):
    if request.method == 'POST':
        _new_recruit = Recruit( name=request.POST.get('name'),
                                planet_id=request.POST.get('planet_id'),
                                age=request.POST.get('age'),
                                email=request.POST.get('email'))
        _new_recruit.save()
        return render(request, 'recruit/welcome.html', {'title': f'Welcome, {_new_recruit.name}', 'name':_new_recruit.name})
    elif request.method == 'GET':
        _planets_list = Planet.objects.all()           
        return render(request, 'reg_form.html', context={'planets':_planets_list} )

def questions(request: HttpRequest):
    if request.method == 'POST':
        _qid = int(request.POST.get('qid'))
        _answer = request.POST.get('answer')
        if _answer == 'Yes':
            _answer = True
        else:
            _answer = False
        _rec_id = Recruit.objects.all().order_by('-id')[0].id
        _questions = Question.objects.all()
        _question = _questions.get(id=_qid)         
        rec_ans = RecruitAnswer(recruitId=_rec_id, questionId=_qid, answer=_answer)
        rec_ans.save() 
        if _qid < _questions.count():      
            _question = _questions.get(id=_qid + 1)             
            return render(request, 'recruit/questions.html', context={'title': 'Questions', 'qid':_qid + 1, 'question': _question.question})
        else:
            _questions_list = [q.question for q in _questions]            
            _answers = [a.answer for a in RecruitAnswer.objects.filter(recruitId=_rec_id)]
            _res_list = zip(_questions_list, _answers)
            _name = Recruit.objects.get(id=_rec_id).name
            return render(request, 'recruit/endTest.html', context={'title': 'Poll end', 'results': _res_list, 'name': _name, 'id': _rec_id})          

    if request.method == 'GET':
        _first_question = Question.objects.get(id=1)        
        return render(request, 'recruit/questions.html', context={'title': 'Questions', 'qid':1, 'question': _first_question.question})

def sith(request: HttpRequest):    
    return render(request, 'recruit/sith.html', {'title': f'Introduce yourself', 'siths': Sith.objects.all(), 'siths1': Sith.objects.filter(shadowHandsNumber__gte=1)})

def showRecruits(request: HttpRequest):
    if request.method == 'POST':
        _siths_list = Sith.objects.all()       
        _sith_planet_id = _siths_list.get(id=request.POST.get('sith_id')).planet.id             
        _rec_list = [rec for rec in Recruit.objects.filter(planet_id=_sith_planet_id).exclude(mainSith_id=request.POST.get('sith_id'))]
        _sith_sh_list = [sh for sh in Recruit.objects.filter(mainSith_id=request.POST.get('sith_id'))]
        context = {
            'title': 'Recruits list',
            'rec_list': _rec_list,
            'shadowHands': _sith_sh_list,
            'sith_id': request.POST.get('sith_id'),
           }
        return render(request, 'recruit/showRecruits.html', context=context)

def showAnswers(request: HttpRequest):
    if request.method == 'POST':
        _rec_id = request.POST.get('recruit_id')
        _questions = [q.question for q in Question.objects.all()]
        _answers = [a.answer for a in RecruitAnswer.objects.filter(recruitId=_rec_id)]
        _res_list = zip(_questions, _answers)
        _name = Recruit.objects.get(id=_rec_id).name
        _sh_number = Sith.objects.get(id=request.POST.get('sith_id')).shadowHandsNumber
        context = {
            'title': 'Answers',
            'results': _res_list,
            'name': _name,
            'id': _rec_id,
            'sith_id': request.POST.get('sith_id'),
            'sh_number': _sh_number
            }       
        return render(request, 'recruit/endTest.html', context=context)  

def shadowHand(request: HttpRequest):
    if request.method == 'POST':
        _sith_list = Sith.objects.all()
        _sh_number = _sith_list.get(id=request.POST.get('sith_id')).shadowHandsNumber
        if _sh_number < 3:
            _rec_id = request.POST.get('recruit_id')            
            _sith_id = request.POST.get('sith_id')               
            _rec = Recruit.objects.get(id=_rec_id)
            print(_rec.id)
            _rec_name = _rec.name
            _sith = _sith_list.get(id=request.POST.get('sith_id'))
            # _rec.mainSith.set(request.POST.get('sith_id') )
            _rec.mainSith_id = int(request.POST.get('sith_id'))
            _rec.save(update_fields=['mainSith_id'])
            _sith.shadowHandsNumber += 1
            _sith.save()
            # _rec.shadowHand = True
            # _rec.main_sith.set(_sith_id)
            # _rec.save()
            # send_mail('Django mail', 'This e-mail was sent with Django.', 'your@gmail.com', [f'{_rec.email}'], fail_silently=False)
            return render(request, 'recruit/shadowHand.html', context={'title': 'ShadowHand', 'name': _rec_name, 'id': _rec_id}) 
        else:
            return render(request, 'recruit/shadowHand.html', context={'title': 'ShadowHand', })             

        