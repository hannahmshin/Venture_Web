from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import RegexValidator #This is for phonenumber
from django.contrib.auth.models import User #We are going to extend on User profile

# Create your models here.
def upload_location(instance,filename):
    return "%s/%s" %(instance.id, filename)

#This is extending the existing user model.
#What information do I need from Guides
#User comes with username, first_name, last_name, email, password
#We know that User will have many related TOURS. For example, interested tours, previous tours, and my tours(one that user created)
class tour_user(models.Model):
    #one user can only have one tour_user
    user = models.OneToOneField(User, unique=True)
    #Ask for Gender. But do not share with other people
    
    MALE = 'male'
    FEMALE = 'female'
    #Choices between male and female
    user_gender = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    User_Gender = models.CharField(
        max_length = 10,
        choices = user_gender,
        default = MALE,
    )

    #Ask for phonenumber. 
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(blank = True, max_length = 15)

    

    #Describe yourself to other people.
    about_you = models.TextField(blank = True)

    #maybe add preferences section here
    def __unicode__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = tour_user(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)


User.profile = property(lambda u: tour_user.objects.get_or_create(user=u)[0])

#This class is for when tourGuide makes his/her own tourguide
class Tour(models.Model):

    #who is giving a tour. no need to show this field when creating a field
    author = models.ForeignKey(to=User)

    #related field for Tour. Update later with more functionality
    country = models.CharField(max_length = 120,  blank=True,default='your country')
    state = models.CharField(max_length = 120,  blank=True,default='your state')
    cityname = models.CharField(max_length = 120,  blank=True,default='your city')
    

    #Theme, later implement duplicate choices
    ART = 'art'
    ACTIVITY = 'activity'
    HISTORIC = 'historic'
    GENERAL = 'generic'

    #Choices between male and female
    theme = (
        (ART, 'Art'),
        (ACTIVITY, 'Activity'),
        (HISTORIC, 'Historic'),
        (GENERAL, 'General'),
    )

    tour_theme = models.CharField(
        max_length = 10,
        choices = theme,
        blank=True,
        default = GENERAL,

    )

    #how many tourists can you handle?
    capacity = models.IntegerField(blank=True,default=0,null=True)

    #how long will your tour lasts?
    #duration = models.IntegerField(default=0, blank=True)

    #How physically tired this tour will make your tourist be ?
    Sandals = 'sandals'
    Reg_shoes = 'regular shoes'
    Gym_shoes = 'gym shoes'
    Hiking_shoes = 'hiking shoes'

    intensity = (
        (Sandals, 'Sandals'),
        (Reg_shoes, 'Regular shoes'),
        (Gym_shoes, 'Gym Shoes'),
        (Hiking_shoes, 'Hiking shoes'),
    )

    tour_intensity = models.CharField(
        blank=True,
        max_length = 20,
        choices = intensity,
        default = Sandals,
    )

    #title of the tour
    title = models.CharField(blank=True,max_length = 120)

    image = models.ImageField(upload_to = "images", null=True, blank=True, height_field= "height_field", width_field="width_field" )
    content = models.TextField(blank=True) #desciprt of the picture
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    
    #Text box for tour description. Here user can talk about how much they want to get paid, and what days work best for them.
    description = models.TextField( blank=True)
    slug = models.CharField( blank=True,max_length=150, unique=True, default="", null=True)

    #is this Tour done being edited? or still in draft mode?
    draft = models.BooleanField(default=True)

    #progress fields for progress bar
    progress = models.TextField(default="0%") #bootstrap takes in number% format

    def __unicode__(self):
        return self.title

    def save(self):
        super(Tour, self).save()
        self.slug = '%s/%s/%i' %(self.author, slugify(self.title), self.id)
        super(Tour,self).save()

    def get_absoulte_url(self):
        return reverse("tourist:tour_detail", kwargs={"slug": self.slug})




#I can't separate one form across multiple pages 
class stops(models.Model):
    tour = models.ForeignKey(to=Tour)
    #STOP
    image = models.ImageField(upload_to = "images", null=True, blank=True, height_field= "height_field", width_field="width_field" )
    content = models.TextField(blank=True) #desciprt of the picture
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)





