from django import forms
from .models import Animevideo

class AnimeForm(forms.ModelForm):
    class Meta:
        model = Animevideo
        fields = [
            'Anime_name', 'Anime_category', 'Language',
            'Anime_poster', 'Anime_wallpaper', 'Anime_rate', 'Anime_description'
        ]
