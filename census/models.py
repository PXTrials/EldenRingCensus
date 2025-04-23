from django.db import models
from django.core.validators import MaxValueValidator

class Platform(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Character(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    rune_level = models.PositiveSmallIntegerField(
                            validators=[MaxValueValidator(713)]
                        )
    weapon_level = models.PositiveSmallIntegerField(
                            validators=[MaxValueValidator(25)]
                        )

    def __str__(self):
        return f'{self.name} ({self.platform} RL{self.rune_level}+{self.weapon_level})'

class Role(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name.capitalize()

class Area(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    sort_order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class Location(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=60)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    sort_order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.area}: {self.name}'

class Outcome(models.Model):
    id = models.SmallAutoField(primary_key=True)
    description = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    is_win = models.BooleanField()
    is_loss = models.BooleanField()
    sort_order = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return f'{self.wl()}: {self.description}'

    def wl(self):
        if self.is_win:
            return 'Win'
        elif self.is_loss:
            return 'Loss'
        else:
            return 'Neutral'


class Encounter(models.Model):
    character = models.ForeignKey(Character, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    host_level = models.PositiveSmallIntegerField(
                            null=True,
                            blank=True,
                            validators=[MaxValueValidator(713)]
                            )
    outcome = models.ForeignKey(Outcome, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.character} as {self.role} => {self.outcome.wl()} @ {self.location.area}"
