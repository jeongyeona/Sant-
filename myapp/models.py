from django.db import models

class Wine(models.Model):
    id = models.IntegerField(primary_key=True)
    name_kr = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    producer = models.CharField(max_length=100, blank=True, null=True)
    nation = models.CharField(max_length=200, blank=True, null=True)
    varieties = models.CharField(max_length=350, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    food = models.CharField(max_length=200, blank=True, null=True)
    abv = models.CharField(max_length=200, blank=True, null=True)
    degree = models.CharField(max_length=200, blank=True, null=True)
    sweet = models.IntegerField(blank=True, null=True)
    acidity = models.IntegerField(blank=True, null=True)
    body = models.IntegerField(blank=True, null=True)
    tannin = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    year = models.CharField(max_length=30, blank=True, null=True)
    ml = models.CharField(max_length=30, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine'


class WineGrade(models.Model):
    iuser = models.ForeignKey('WineUser', models.DO_NOTHING, db_column='iuser')
    iwine = models.OneToOneField(Wine, models.DO_NOTHING, db_column='iwine', primary_key=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine_grade'
        unique_together = (('iwine', 'iuser'))


class WineUser(models.Model):
    id = models.CharField(unique=True, max_length=30)
    pwd = models.CharField(max_length=100)
    nickname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    regdate = models.DateTimeField(blank=True, null=True)
    pid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wine_user'
