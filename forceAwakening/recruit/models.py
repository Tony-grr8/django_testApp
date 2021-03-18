from django.db import models

# Create your models here.
class Planet(models.Model):
    '''
    Модель описывающая Планету
    '''
    name=models.CharField(max_length=42)

    def __str__(self):
        return self.name      

class Sith(models.Model):
    '''
    Модель описывающая Ситха
    '''
    name = models.CharField(max_length=42)
    planet = models.ForeignKey(Planet, on_delete = models.CASCADE)    

    def __str__(self):
        return self.name 

class Recruit(models.Model):
    '''
    Модель описывающая Рекрута
    '''
    name = models.CharField(max_length=42)
    planet = models.ForeignKey(Planet, on_delete = models.CASCADE)
    age = models.SmallIntegerField()
    email = models.CharField(max_length=42, unique=True)
    mainSith = models.ForeignKey(Sith, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name    


class Question(models.Model):
    '''
    Модель описывающая Вопрос
    '''
    question = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.question    


class RecruitAnswer(models.Model):
    '''
    Модель описывающая ответы рекрутов на вопросы
    '''
    recruitId = models.BigIntegerField()
    questionId = models.BigIntegerField()
    answer = models.BooleanField()

    def __str__(self):
        return 'RecruitAnswer: ' + 'Recruit name and ID: ' + Recruit.objects.get(id=self.recruitId).name + ' ' + str(self.recruitId) +';' + ' Q: ' + Questions.objects.get(id=self.questionId).question + ' A: ' + str(self.answer)      


  
 