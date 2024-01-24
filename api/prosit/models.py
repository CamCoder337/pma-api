from django.db import models


class Semester(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

class Prosit(models.Model):
    title = models.CharField(max_length=150)
    data = models.JSONField()
    active = models.BooleanField(default=False)
    achieved = models.BooleanField(default=False)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)

class PrositGroup(models.Model):
    title = models.CharField(max_length=50)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)

class PrositStudent(models.Model):
    prositGroup = models.ForeignKey(PrositGroup)
    student = models.ForeignKey("api_user.User", on_delete=models.CASCADE)

class PrositRole(models.Model):
    prosit = models.ForeignKey(Prosit, on_delete=models.CASCADE)
    prositGroup = models.ForeignKey(PrositGroup, on_delete=models.CASCADE)
    animator  = models.ForeignKey("api_user.User", on_delete=models.CASCADE)
    secretary  = models.ForeignKey("api_user.User", on_delete=models.CASCADE)
    timeKeeper  = models.ForeignKey("api_user.User", on_delete=models.CASCADE)
    scribe  = models.ForeignKey("api_user.User", on_delete=models.CASCADE)



