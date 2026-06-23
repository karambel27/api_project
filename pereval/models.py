from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    otc = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Coords(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    height = models.IntegerField()

    def __str__(self):
        return f'{self.latitude}, {self.longitude}'


class Level(models.Model):
    winter = models.CharField(max_length=10, blank=True)
    summer = models.CharField(max_length=10, blank=True)
    autumn = models.CharField(max_length=10, blank=True)
    spring = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'Сложность: зима {self.winter}, лето {self.summer}'


class PerevalAdded(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perevals')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.title


class Image(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='images')
    data = models.TextField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
