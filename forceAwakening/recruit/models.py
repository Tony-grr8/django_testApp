from django.db import models

# Create your models here.
class Planets(models.Model):
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
    planet = models.ForeignKey(Planets, on_delete = models.CASCADE)

    def __str__(self):
        return self.name 

class Recruit(models.Model):
    '''
    Модель описывающая Рекрута
    '''
    name = models.CharField(max_length=42)
    planet = models.ForeignKey(Planets, on_delete = models.CASCADE)
    age = models.SmallIntegerField()
    email = models.CharField(max_length=42, unique=True)
    shadowHand = models.BooleanField(default=False)
    main_sith = models.ManyToManyField(Sith, default=None)

    def __str__(self):
        return self.name    


class Questions(models.Model):
    '''
    Модель описывающая Вопрос
    '''
    question = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.question    


class RecruitAnswers(models.Model):
    '''
    Модель описывающая ответы рекрутов на вопросы
    '''
    recruitId = models.BigIntegerField()
    questionId = models.BigIntegerField()
    answer = models.BooleanField()

    def __str__(self):
        return 'RecruitAnswers: ' + 'Recruit name and ID: ' + Recruit.objects.get(id=self.recruitId).name + ' ' + str(self.recruitId) +';' + ' Q: ' + Questions.objects.get(id=self.questionId).question + ' A: ' + str(self.answer)      


# class Sith(models.Model):
#     name = models.CharField(max_length=42)
#     planet = models.ForeignKey(Planets, on_delete = models.CASCADE)

#     def __str__(self):
#         return self.name       
 