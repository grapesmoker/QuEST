from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from collections import OrderedDict

# Create your models here.

CATEGORIES = (('S-P', 'Science - physics'),
              ('S-C', 'Science - chemistry'),
              ('S-B', 'Science - biology'),
              ('S-O', 'Science - other'),
              ('L-AM', 'Literature - American'),
              ('L-EU', 'Literature - European'),
              ('L-BR', 'Literature - British'),
              ('L-W', 'Literature - World'),
              ('H-AM', 'History - American'),
              ('H-EU', 'History - European'),
              ('H-W', 'History - World'),
              ('R', 'Religion'),
              ('M', 'Myth'),
              ('P', 'Philosophy'),
              ('FA', 'Fine arts'),
              ('SS', 'Social science'),
              ('G', 'Geography'),
              ('O', 'Other'),
              ('PC', 'Pop culture'))

RELIGION_SUBTYPES = (('R-J', 'Religion - Judaism'),
                     ('R-C', 'Religion - Christianity'),
                     ('R-B', 'Religion - Buddhism'),
                     ('R-H', 'Religion - Hinduism'),
                     ('R-I', 'Religion - Islam'),
                     ('R-O', 'Religion - Other'),)

MYTH_SUBTYPES = (('M-GR', 'Myth - Greek'),
                 ('M-R', 'Myth - Roman'),
                 ('M-N', 'Myth - Norse'),
                 ('M-BR', 'Myth - British Isles'),
                 ('M-EE', 'Myth - Eastern Europe'),
                 ('M-IN', 'Myth - India'),
                 ('M-CH', 'Myth - China'),
                 ('M-JP', 'Myth - Japan'),
                 ('M-O', 'Myth - Other'),)

PHILOSOPHY_SUBTYPES = (('P-AN', 'Philosophy - Analytic'),
                       ('P-CO', 'Philosophy - Continental'),
                       ('P-EN', 'Philosophy - Enlightenment'),
                       ('P-CL', 'Philosophy - Classical'),
                       ('P-O', 'Philosophy - Other'),)

FINE_ARTS_SUBTYPES = (('FA-M', 'Fine arts - Music'),
                      ('FA-SC', 'Fine arts - Sculpture'),
                      ('FA-OP', 'Fine arts - Opera'),
                      ('FA-F', 'Fine arts - Film'),
                      ('FA-P', 'Fine arts - Painting'),
                      ('FA-AR', 'Fine arts - Architecture'),
                      ('FA-O', 'Fine arts - Other'),)

SOCIAL_SCIENCE_SUBTYPES = (('SS-SOC', 'Social science - Sociology'),
                           ('SS-EC', 'Social science - Economics'),
                           ('SS-PS', 'Social science - Psychology'),
                           ('SS-O', 'Social science - Other'),)

LIT_SUBTYPES = (('L-PL', 'Literature - play'),
                ('L-PO', 'Literature - poem'),
                ('L-NO', 'Literature - novel'),
                ('L-CR', 'Literature - criticism'),
                ('L-O', 'Literature - other'),)

SCIENCE_SUBTYPES = (('S-P-QM', 'Science - physics - quantum mechanics'),
                    ('S-P-SM', 'Science - physics - statistical mechanics'),
                    ('S-P-M', 'Science - physics - classical mechanics'),
                    ('S-P-R', 'Science - physics - relativity'),
                    ('S-P-MP', 'Science - physics - mathematical physics'),
                    ('S-P-EM', 'Science - physics - electrodynamics'),
                    ('S-P-SS', 'Science - physics - solid state'),
                    ('S-P-MSC', 'Science - physics - miscellaneous'),
                    ('S-C-O', 'Science - chemistry - organic'),
                    ('S-C-P', 'Science - chemistry - physical'),
                    ('S-C-B', 'Science - chemistry - biochem'),
                    ('S-C-MSC', 'Science - chemistry - miscellaneous'),
                    ('S-B-C', 'Science - biology - biochem'),
                    ('S-B-G', 'Science - biology - genetics'),
                    ('S-B-E', 'Science - biology - evolutionary bio'),
                    ('S-B-MSC', 'Science - biology - miscellaneous'),
                    ('S-O-A', 'Science - other - astronomy'),
                    ('S-O-A', 'Science - other - mathematics'),
                    ('S-O-A', 'Science - other - computer science'),
                    ('S-O-A', 'Science - other - engineering'),
                    ('S-O-A', 'Science - other - earth science'),)

ACF_DISTRO = OrderedDict([('S', (5, 5)),
                          ('L', (5, 5)),
                          ('H', (5, 5)),
                          ('R', (1, 1)),
                          ('M', (1, 1)),
                          ('P', (1, 1)),
                          ('FA', (3, 3)),
                          ('SS', (1, 1)),
                          ('G', (1, 1)),
                          ('PC', (1, 1))])

class Tournament (models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    host = models.CharField(max_length=200)
    address = models.TextField(max_length=200)
    owner = models.OneToOneField('Player', related_name='owner')
    public = models.BooleanField()
    distribution = models.ForeignKey('Distribution')
    #teams = models.ForeignKey('Team')

    class Admin: pass

    def __str__(self):
        return '{0!s}'.format(self.name)

class Team (models.Model):
    
    team_name = models.CharField(max_length=200)
    tournament = models.ForeignKey(Tournament)
    school = models.ForeignKey('School')
    team_owner = models.ForeignKey('Player', related_name='team_owner')
    
    def __str__(self):
        return'{0!s} - {1!s}'.format(self.team_name, self.tournament)
    
class Player(models.Model):
    user = models.OneToOneField(User)
    
    team = models.ManyToManyField(Team)
    tournament = models.ManyToManyField(Tournament)
    school = models.ForeignKey('School')
    
    def __str__(self):
        return '{0!s}'.format(self.user.username)
    
class School(models.Model):
    
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    contact_phone = models.CharField(max_length=50)
    address = models.TextField()
    
    created_by = models.ForeignKey(Player, related_name='created_by')
    
    def __str__(self):
        return '{0!s}'.format(self.name)
    
class Role(models.Model):
    
    player = models.ForeignKey(Player)
    tournament = models.ForeignKey(Tournament)
    category = models.CharField(max_length=500)
    can_view_others = models.BooleanField()
    can_edit_others = models.BooleanField()

class TeamRole(models.Model):
    
    player = models.ForeignKey(Player, blank=True)
    team = models.ForeignKey(Team, blank=True)
    category = models.CharField(max_length=100)
    can_view_others = models.BooleanField(blank=True)
    can_edit_others = models.BooleanField(blank=True)

class Packet (models.Model):
    team_name = models.CharField(max_length=200)
    date_submitted = models.DateField()
    authors = models.ManyToManyField(Player)
    tournament = models.ForeignKey(Tournament)
    team = models.ForeignKey(Team)
    
    created_by = models.ForeignKey(Player, related_name='packet_creator')

class DistributionPerPacket(models.Model):
    
    tournament = models.ManyToManyField(Tournament)
    category = models.CharField(max_length=10, choices=CATEGORIES)
    subcategory = models.CharField(max_length=10)
    num_tossups = models.IntegerField()
    num_bonuses = models.IntegerField()
    
class Distribution(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return '{0!s}'.format(self.name)
    
class DistributionEntry(models.Model):
    
    distribution = models.ForeignKey(Distribution)
    category = models.TextField()
    subcategory = models.TextField()
    num_tossups = models.CharField(max_length=500)
    num_bonuses = models.CharField(max_length=500)
    fin_tossups = models.CharField(max_length=500)
    fin_bonuses = models.CharField(max_length=500)
    
    
class Tossup (models.Model):
    packet = models.ForeignKey(Packet)
    tossup_text = models.TextField()
    tossup_answer = models.TextField()
    
    category = models.CharField(max_length=500, choices=CATEGORIES)
    subtype = models.CharField(max_length=500)
    time_period = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    
    author = models.ForeignKey(Player)
    
    locked = models.BooleanField()

class Bonus(models.Model):
    packet = models.ForeignKey(Packet)
    leadin = models.CharField(max_length=500)
    part1_text = models.TextField()
    part1_answer = models.TextField()
    part2_text = models.TextField()
    part2_answer = models.TextField()
    part3_text = models.TextField()
    part3_answer = models.TextField()
    
    category = models.CharField(max_length=500, choices=CATEGORIES)
    subtype = models.CharField(max_length=500)
    time_period = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    
    author = models.ForeignKey(Player)
    
    locked = models.BooleanField()
    
class Category(models.Model):

    category = models.CharField(max_length=100, choices=CATEGORIES)
    

class Test(models.Model):
    blah = models.CharField(max_length=50)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
