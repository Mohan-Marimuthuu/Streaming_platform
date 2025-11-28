from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify





class CreatorID(models.Model):
    Creator_id=models.CharField(max_length=20)
    Password_cr=models.CharField(max_length=10)
    Email_cr=models.EmailField(default="")
    login_time=models.TimeField(default="")

class Animefan(models.Model):
    Firstname = models.CharField(max_length=20,default="")
    Lastname = models.CharField(max_length=20,default="")
    Username = models.CharField(max_length=20,default="")
    Email = models.EmailField(default="")
    Password = models.CharField(max_length=20,default="")
    Profile_img = models.ImageField(upload_to='profile_images/', null=True, blank=True)


class Animevideo(models.Model):

    STATE_CHOICES = [
        ('Comedy', 'Comedy'),
        ('MYSTERY', 'Mystery'),
        ('LOVE', 'Love'),
        ('DRAMA', 'Drama'),
        ('SPORT', 'Sport'),
        ('ACTION', 'Action'),
        ('FANTASY', 'Fantasy'),
        ('ADVENTURE', 'Adventure'),
        ('HORROR', 'Horror'),
        ('SCI-FI', 'Sci-Fi'),
    ]

    LANGUAGE_CHOICES = [
        ('Tamil', 'Tamil'),
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Kannada', 'Kannada'),
        ('Malayalam', 'Malayalam'),
        ('Telugu', 'Telugu'),
        ('Japanese', 'Japanese'),
        ('Korean', 'Korean'),
        ('Chinese', 'Chinese'),
        ('French', 'French'),
        ('Spanish', 'Spanish'),
    ]


    Anime_category = MultiSelectField(choices=STATE_CHOICES, max_length=200)
    Language = MultiSelectField(choices=LANGUAGE_CHOICES, max_length=200,default=['en'])
    Anime_name = models.CharField(max_length=200)
    Anime_poster = models.ImageField(upload_to='anime_posters/', blank=True, null=True)
    Anime_wallpaper = models.ImageField(upload_to='images/', null=True, blank=True)
    Anime_rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    Anime_description = models.TextField(max_length=500, null=False, blank=False)
    like = models.ManyToManyField("Animefan", related_name="liked_animes", blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Anime_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.Anime_name


class AnimeVideoFile(models.Model):
    anime = models.ForeignKey(Animevideo, on_delete=models.CASCADE, related_name='videos')
    episode_number = models.IntegerField()
    episode_name = models.CharField(max_length=200, blank=True, null=True)
    video_file = models.FileField(upload_to='anime_videos/')

    def __str__(self):
        return f"{self.anime.Anime_name} - Episode {self.episode_number}"




from django.utils import timezone
  # your user model

class Notification(models.Model):
    user = models.ForeignKey(Animefan, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"
    


class Watchlist(models.Model):
    user = models.ForeignKey(Animefan, on_delete=models.CASCADE)
    anime = models.ForeignKey(Animevideo, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')



