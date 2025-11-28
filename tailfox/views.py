from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from .forms import *
from django.shortcuts import redirect, get_object_or_404
import random
import datetime

# store selected anime IDs for weekly rotation
from django.core.cache import cache

from django.contrib.auth.decorators import login_required

@login_required
def update_like(request, anime_id):
    if "user_id" not in request.session:
        return JsonResponse({"error": "login required"}, status=401)

    user = Animefan.objects.get(id=request.session["user_id"])
    anime = Animevideo.objects.get(id=anime_id)

    if user in anime.like.all():
        anime.like.remove(user)
        liked = False
    else:
        anime.like.add(user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "count": anime.like.count()
    })

def index(request):
    user_id = request.session.get('user_id')
    creator_id=request.session.get('creator_id')
    user_data = None
    creator_data = None

    
    
    if creator_id:
        try:
            creator_data = CreatorID.objects.get(id=creator_id)
        except CreatorID.DoesNotExist:
            pass

    if user_id:
        try:
            user_data = Animefan.objects.get(id=user_id)
        except Animefan.DoesNotExist:
            pass

    popular_items = Animevideo.objects.annotate(
    like_count=models.Count('like')).order_by('-like_count')[:10]   # shows top 10 anime
    comedy_items = Animevideo.objects.filter(Anime_category__contains='CO')
    mystery_items = Animevideo.objects.filter(Anime_category__contains='MY')
    love_items = Animevideo.objects.filter(Anime_category__contains='LO')
    drama_items = Animevideo.objects.filter(Anime_category__contains='DR')
    sport_items = Animevideo.objects.filter(Anime_category__contains='SP')

    tl_language = Animevideo.objects.filter(Language='tl')
    en_language = Animevideo.objects.filter(Language='en')
    hi_language = Animevideo.objects.filter(Language='hi')
    kn_language = Animevideo.objects.filter(Language='kn')
    ml_language = Animevideo.objects.filter(Language='ml')
    te_language = Animevideo.objects.filter(Language='te')
    ja_language = Animevideo.objects.filter(Language='ja')
    ko_language = Animevideo.objects.filter(Language='ko')
    zh_language = Animevideo.objects.filter(Language='zh')
    yu_language = Animevideo.objects.filter(Language='yu')
    fr_language = Animevideo.objects.filter(Language='fr')
    es_language = Animevideo.objects.filter(Language='es')
    top_anime = Animevideo.objects.all().order_by('-Anime_rate') 


    current_week = timezone.now().isocalendar()[1]

    # check cache to see if we already stored random 6 anime for this week
    cached_week = cache.get('carousel_week')
    cached_anime_ids = cache.get('carousel_anime_ids')

    if cached_week != current_week or not cached_anime_ids:
        # pick 6 random anime that have wallpapers
        all_anime = list(Animevideo.objects.exclude(Anime_wallpaper=""))
        random_anime = random.sample(all_anime, min(6, len(all_anime)))

        # store IDs and current week in cache for 7 days
        cache.set('carousel_week', current_week, 60 * 60 * 24 * 7)
        cache.set('carousel_anime_ids', [a.id for a in random_anime], 60 * 60 * 24 * 7)
    else:
        random_anime = Animevideo.objects.filter(id__in=cached_anime_ids)

    anime_list = Animevideo.objects.all()
    
    # ⭐ Anime sorted by most likes

    

    context = {
        # user 
        'animefan': user_data,
        'builder': creator_data,
        # catagery
        'comedy_items': comedy_items,
        'mystery_items': mystery_items,
        'love_items': love_items,
        'drama_items': drama_items,
        'sport_items': sport_items,
        #language
        'tl_language': tl_language,
        'en_language': en_language,
        'hi_language': hi_language,
        'kn_language': kn_language,
        'ml_language': ml_language,
        'te_language': te_language,
        'ja_language': ja_language,
        'ko_language': ko_language,
        'zh_language': zh_language,
        'yu_language': yu_language,
        'fr_language': fr_language,
        'es_language': es_language,
        # carousel
        'carousel_anime': random_anime,
        #views & free
        'popular_items': top_anime,
        'like_count': popular_items,

        'anime_list': anime_list,
    
    }

    # ✅ Pass only ONE dictionary to render()
    return render(request, 'index.html', context)


def popular(request):
    user_id = request.session.get('user_id')
    creator_id=request.session.get('creator_id')
    user_data = None
    creator_data = None

    
    
    if creator_id:
        try:
            creator_data = CreatorID.objects.get(id=creator_id)
        except CreatorID.DoesNotExist:
            pass

    if user_id:
        try:
            user_data = Animefan.objects.get(id=user_id)
        except Animefan.DoesNotExist:
            pass

    top_anime = Animevideo.objects.all().order_by('-Anime_rate') 
    context = {
        'animefan': user_data,
        'builder': creator_data,
        'top_anime':top_anime

               }

    return render(request, 'popular.html',context)



def action(request):
    user_id = request.session.get('user_id')
    creator_id=request.session.get('creator_id')
    user_data = None
    creator_data = None

    
    
    if creator_id:
        try:
            creator_data = CreatorID.objects.get(id=creator_id)
        except CreatorID.DoesNotExist:
            pass

    if user_id:
        try:
            user_data = Animefan.objects.get(id=user_id)
        except Animefan.DoesNotExist:
            pass

    popular_items = Animevideo.objects.annotate(
    like_count=models.Count('like')).order_by('-like_count')[:10]   # shows top 10 anime
    comedy_items = Animevideo.objects.filter(Anime_category__contains='CO')
    mystery_items = Animevideo.objects.filter(Anime_category__contains='MY')
    love_items = Animevideo.objects.filter(Anime_category__contains='LO')
    drama_items = Animevideo.objects.filter(Anime_category__contains='DR')
    sport_items = Animevideo.objects.filter(Anime_category__contains='SP')

    tl_language = Animevideo.objects.filter(Language='tl')
    en_language = Animevideo.objects.filter(Language='en')
    hi_language = Animevideo.objects.filter(Language='hi')
    kn_language = Animevideo.objects.filter(Language='kn')
    ml_language = Animevideo.objects.filter(Language='ml')
    te_language = Animevideo.objects.filter(Language='te')
    ja_language = Animevideo.objects.filter(Language='ja')
    ko_language = Animevideo.objects.filter(Language='ko')
    zh_language = Animevideo.objects.filter(Language='zh')
    yu_language = Animevideo.objects.filter(Language='yu')
    fr_language = Animevideo.objects.filter(Language='fr')
    es_language = Animevideo.objects.filter(Language='es')
    top_anime = Animevideo.objects.all().order_by('-Anime_rate') 


    current_week = timezone.now().isocalendar()[1]

    # check cache to see if we already stored random 6 anime for this week
    cached_week = cache.get('carousel_week')
    cached_anime_ids = cache.get('carousel_anime_ids')

    if cached_week != current_week or not cached_anime_ids:
        # pick 6 random anime that have wallpapers
        all_anime = list(Animevideo.objects.exclude(Anime_wallpaper=""))
        random_anime = random.sample(all_anime, min(6, len(all_anime)))

        # store IDs and current week in cache for 7 days
        cache.set('carousel_week', current_week, 60 * 60 * 24 * 7)
        cache.set('carousel_anime_ids', [a.id for a in random_anime], 60 * 60 * 24 * 7)
    else:
        random_anime = Animevideo.objects.filter(id__in=cached_anime_ids)

    anime_list = Animevideo.objects.all()
    
    # ⭐ Anime sorted by most likes

    

    context = {
        # user 
        'animefan': user_data,
        'builder': creator_data,
        # catagery
        'comedy_items': comedy_items,
        'mystery_items': mystery_items,
        'love_items': love_items,
        'drama_items': drama_items,
        'sport_items': sport_items,
        #language
        'tl_language': tl_language,
        'en_language': en_language,
        'hi_language': hi_language,
        'kn_language': kn_language,
        'ml_language': ml_language,
        'te_language': te_language,
        'ja_language': ja_language,
        'ko_language': ko_language,
        'zh_language': zh_language,
        'yu_language': yu_language,
        'fr_language': fr_language,
        'es_language': es_language,
        # carousel
        'carousel_anime': random_anime,
        #views & free
        'popular_items': top_anime,
        'like_count': popular_items,

        'anime_list': anime_list,
    
    }

    # ✅ Pass only ONE dictionary to render()
    return render(request, 'action.html', context)




def naruto(request):
    user_id = request.session.get('user_id')
    creator_id=request.session.get('creator_id')
    user_data = None
    creator_data = None

    
    
    if creator_id:
        try:
            creator_data = CreatorID.objects.get(id=creator_id)
        except CreatorID.DoesNotExist:
            pass

    if user_id:
        try:
            user_data = Animefan.objects.get(id=user_id)
        except Animefan.DoesNotExist:
            pass

        
    return render(request, 'naruto_file.html', {'animefan': user_data,'builder': creator_data})





def account(request):
    mydata = Animefan.objects.all()
    if(mydata!=""):
        return render(request,"account.html",{"animefan":mydata})
    else:
        return render(request,"account.html") 

def userData(request):
    if request.method == 'POST':
        firstname=request.POST.get("firstnamelog")
        lastname=request.POST.get("lastnamelog")
        username=request.POST.get("usernamelog")
        email=request.POST.get("emaillog")
        password=request.POST.get("passwordlog")   
        confirm_passwords=request.POST.get("confirm_password")
        if password != confirm_passwords:
            return HttpResponse("password not match")
        
        obj=Animefan()
        obj.Firstname=firstname
        obj.Lastname=lastname
        obj.Username=username
        obj.Email=email
        obj.Password=password
        obj.save()
        mydata=Animefan.objects.all()
        return redirect("login")
    return render(request, 'account.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Animefan, CreatorID



def login(request):
    if request.method == 'POST':
        username = request.POST.get("usernamelog")
        password = request.POST.get("password")

        # Try Animefan login
        try:
            user = Animefan.objects.get(Username=username)
            if user.Password == password:
                request.session['user_id'] = user.id
                return redirect("index")
            else:
                messages.error(request, "Invalid password for Animefan account.")
                return redirect("login")
        except Animefan.DoesNotExist:
            pass  # If not found, check CreatorID next

        # Try CreatorID login
        try:
            creator = CreatorID.objects.get(Creator_id=username)
            if creator.Password_cr == password:
                request.session['creator_id'] = creator.id
                return redirect("index")
            else:
                messages.error(request, "Invalid password for Creator account.")
                return redirect("login")
        except CreatorID.DoesNotExist:
            messages.error(request, "User not found in either account type.")
        
        return redirect("login")

    return render(request, "loginpage.html")


def logout(request):
    request.session.pop('user_id', None)
    request.session.pop('creator_id', None)
    return redirect("index")






from django.db.models import Q
from .models import Animevideo   # ← your model

def search(request):
    query = request.GET.get('query', '').strip()
    results = Animevideo.objects.filter(
    Q(Anime_name__icontains=query) |
    Q(Anime_category__icontains=query) |
    Q(Language__icontains=query) |
    Q(Anime_rate__icontains=query)
    )if query else []

    return render(request, 'search.html', {'query': query, 'results': results})

#anime import image and video
def notifications(request):
    user_id = request.session.get('user_id')
    creator_id = request.session.get('creator_id')

    user_data = Animefan.objects.filter(id=user_id).first()
    creator_data = CreatorID.objects.filter(id=creator_id).first()

    if not user_id:
        return redirect('login')

    # ⭐ FIRST GET NOTIFICATIONS
   

    # Anime category
    popular_items = Animevideo.objects.annotate(like_count=models.Count('like')).order_by('-like_count')[:10]
    comedy_items = Animevideo.objects.filter(Anime_category__contains='CO')
    mystery_items = Animevideo.objects.filter(Anime_category__contains='MY')
    love_items = Animevideo.objects.filter(Anime_category__contains='LO')
    drama_items = Animevideo.objects.filter(Anime_category__contains='DR')
    sport_items = Animevideo.objects.filter(Anime_category__contains='SP')

    # Languages
    tl_language = Animevideo.objects.filter(Language='tl')
    en_language = Animevideo.objects.filter(Language='en')
    hi_language = Animevideo.objects.filter(Language='hi')
    kn_language = Animevideo.objects.filter(Language='kn')
    ml_language = Animevideo.objects.filter(Language='ml')
    te_language = Animevideo.objects.filter(Language='te')
    ja_language = Animevideo.objects.filter(Language='ja')
    ko_language = Animevideo.objects.filter(Language='ko')
    zh_language = Animevideo.objects.filter(Language='zh')
    yu_language = Animevideo.objects.filter(Language='yu')
    fr_language = Animevideo.objects.filter(Language='fr')
    es_language = Animevideo.objects.filter(Language='es')

    user = request.session.get("user_id")
    notes = Notification.objects.filter(user_id=user).order_by('-created_at')

    # 🆕 fetch watchlist items
    watchlist = Watchlist.objects.filter(user_id=user)

    # ⭐ NOW ADD notes to context (AFTER CREATED)
    context = {
        'animefan': user_data,
        'builder': creator_data,

        'popular_items': popular_items,

        'comedy_items': comedy_items,
        'mystery_items': mystery_items,
        'love_items': love_items,
        'drama_items': drama_items,
        'sport_items': sport_items,

        'tl_language': tl_language,
        'en_language': en_language,
        'hi_language': hi_language,
        'kn_language': kn_language,
        'ml_language': ml_language,
        'te_language': te_language,
        'ja_language': ja_language,
        'ko_language': ko_language,
        'zh_language': zh_language,
        'yu_language': yu_language,
        'fr_language': fr_language,
        'es_language': es_language,

        'notes': notes, # now safe

        'watchlist': watchlist,
    }

    return render(request, "acountpage.html", context)



def add_to_watchlist(request, anime_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    anime = get_object_or_404(Animevideo, id=anime_id)
    Watchlist.objects.get_or_create(user_id=user_id, anime=anime)

    # Redirect back to the page where the request came from
    next_url = request.GET.get('next', '/')
    return redirect(next_url)
 # or 'anime_detail', depending on where you came from




def remove_watchlist(request, anime_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    animefan = get_object_or_404(Animefan, id=user_id)
    Watchlist.objects.filter(user=animefan, anime_id=anime_id).delete()

    return redirect('notifications') # page that lists all watchlist items


def update_profile(request):
    user_id = request.session.get("user_id")
    animefan = Animefan.objects.get(id=user_id)

    if request.method == 'POST':
        animefan.Username = request.POST.get("Username")
        
        if 'Profile_img' in request.FILES:           # ← save uploaded image
            animefan.Profile_img = request.FILES['Profile_img']
        
        animefan.save()
        return redirect('notifications')  # or profile page

    return render(request, 'update_profile.html', {"animefan": animefan})






def upload_anime(request):
    form = AnimeForm()

    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            anime = form.save()

            # Get all episode info from POST and FILES
            episode_numbers = request.POST.getlist('episode_numbers')
            episode_names = request.POST.getlist('episode_names')
            videos = request.FILES.getlist('videos')

            # Loop through each uploaded video and create AnimeVideoFile
            for ep_num, ep_name, video_file in zip(episode_numbers, episode_names, videos):
                AnimeVideoFile.objects.create(
                    anime=anime,
                    episode_number=int(ep_num),
                    episode_name=ep_name,
                    video_file=video_file
                )

            return redirect('upload_anime')

    return render(request, "upload.html", {"form": form})

def anime_detail(request, slug):
    anime = get_object_or_404(Animevideo, slug=slug)
    videos = anime.videos.all().order_by('episode_number')  # get all related videos
    return render(request, 'naruto_file.html', {'anime': anime, 'videos': videos})
