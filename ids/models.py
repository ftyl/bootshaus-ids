from django.conf import settings
from django.db import models
from django.utils import timezone 
from datetime import date
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string

# Create your models here.

class Position(models.Model):
    name = models.CharField(max_length=32, verbose_name="Name")
    beschreibung = models.CharField(blank=True, max_length=256, verbose_name="Beschreibung")

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positionen"
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Position")
    bild = ResizedImageField(size=[300,400], crop=['middle', 'center'], keep_meta=False, upload_to="photos/", verbose_name="ID-Bild", blank=True, null=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ACLTyp(models.Model):
    name = models.CharField(max_length=32, verbose_name="Name")
    beschreibung = models.CharField(blank=True, max_length=256, verbose_name="Beschreibung")

    class Meta:
        verbose_name = "Rechte-Typ"
        verbose_name_plural = "Rechte-Typen"
        ordering = ['name']

    def __str__(self):
        return self.name

class Identifikation(models.Model):
    def getRandomString():
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(50))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(primary_key=True, default=getRandomString)
    aaa = models.BooleanField(default=False, help_text="ID matched positiv bei allen Rechte-Typen!", verbose_name="Access All Areas")
    active = models.BooleanField(default=True, help_text="ID Karten die verloren gehen hier deaktivieren", verbose_name="Aktiv")

    class Meta:
        verbose_name = "ID Karte"
        verbose_name_plural = "ID Karten"

    def __str__(self):
        if self.active is False:
            return "Inaktiv - (%s)" % (self.user.username) if self.user != None else "Inaktiv - (%s)" % (self.slug)
        return "%s, %s (%s)" % (self.user.last_name, self.user.first_name, self.user.username) if self.user != None else self.slug

class ACL(models.Model):

    PLUS_CHOICES = [
        (0, "Keine Extra Personen!"),
        (1, "Eine Extra Person"),
        (3, "Drei Extra Personen"),
        (99, "Unendlich!"),
    ]

    description = models.CharField(blank=True, max_length=256, verbose_name="Beschreibung")
    type = models.ManyToManyField(ACLTyp, verbose_name="Rechte-Typ", blank=True)
    identifikation = models.ForeignKey(Identifikation, verbose_name="ID Karte", on_delete=models.CASCADE)
    plus = models.IntegerField(default=0, choices=PLUS_CHOICES, help_text="Angeben ob der Halter dieser Karte weitere Personen mitnehmen kann", verbose_name="Personen mitnehmen")
    beginn = models.DateField(null=True, default=timezone.now, verbose_name="Beginn")
    ende = models.DateField(null=True, default=date(2070, 12, 31), verbose_name="Ende")

    class Meta:
        verbose_name = "Berechtigung"
        verbose_name_plural = "Berechtigungen"

    def __str__(self):
        if self.description != '':
            return "%s - %s (%s bis %s)" % (self.description, self.identifikation.__str__(), self.beginn.strftime("%d.%m.%Y"), self.ende.strftime("%d.%m.%Y"))
        else:
            return "%s (%s bis %s)" % (self.identifikation.__str__(), self.beginn.strftime("%d.%m.%Y"), self.ende.strftime("%d.%m.%Y"))

class IDLog(models.Model):
    identifikation = models.ForeignKey(Identifikation, verbose_name="ID Karte", related_name="idlogs", on_delete=models.PROTECT)
    logged_at = models.DateTimeField(auto_now_add=True)
    matched_type = models.ForeignKey(ACLTyp, verbose_name="Rechte-Typ", blank=True, null=True, on_delete=models.PROTECT)
    matched_acl = models.ForeignKey(ACL, verbose_name="Berechtigung", blank=True, null=True, on_delete=models.PROTECT)
    match_success = models.BooleanField(default=False)

    class Meta:
        verbose_name = "ID Log"
        verbose_name_plural = "ID Logs"

    def __str__(self):
        return self.identifikation.__str__()

