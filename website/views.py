from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Users,Customer
import urllib.request
import bs4 as bs
from textblob import TextBlob
import tweepy
# Create your views here.
def index(request):
    
    if request.method == 'POST':

        username = request.POST.get('Name')
        password = request.POST.get('Password')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            # usertype = Users.objects.filter(username=username,password=password).first()
            # if usertype and usertype.usertype == 'A':
            #     return render(request,'home.html')
            # else:
            #     return redirect('customer')
            return redirect('home')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/')

    else:
        return render(request,'index.html')
        

def register(request):

    if request.method == 'POST':
         
        first_name = request.POST['Name']
        last_name = request.POST['Name']
        username = request.POST['Name']
        password1 = request.POST['Password']
        password2 = request.POST['Password']
        email = request.POST['mail']
        # usertype = request.POST['usertype']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif  User.objects.filter(email=email).exists():
                 messages.info(request,'Email taken')
                 return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1)
                Users.objects.create(first_name=first_name,last_name=last_name,username=username,password=password1,email=email)
                user.save()
                print('user created')
                return render(request,'index.html')
        else:
            messages.info(request,'password not matching..')
        return redirect('register')
    else:    
        return render(request,'register.html')

def customers(request,id):

    custids = Customer.objects.get(id=id)
    scrap_url = custids.link
    if custids.desc =="":
        source = urllib.request.urlopen(scrap_url).read()
        soup = bs.BeautifulSoup(source,'lxml')
        txt = ""
        for paragraph in soup.find_all('p'):
            block = str(paragraph.text)
            if block == None:
                pass
            else:
                txt = txt+(str(paragraph.text))

        custids.desc =txt
        custids.save()
    return render(request,'info.html',{"custids":custids})

def home(request):

    custs = Customer.objects.all()
    return render(request,'home.html',{'custs':custs})

def logout(request):
    auth.logout(request)
    return redirect('/')
def chat(request):
    custs = Customer.objects.all()

    consumer_key = 'midEzHb8nacvmLGo1c2fmita9'
    consumer_secret = 'nEx2a7AU1N31laL82pr9fK2B1jdLgrtQfxWTVt2II4CetapSwz'
    access_token = '1254277768449347586-Wo5FXro68ailMEV4mMiZRIVNRDT9cY'
    access_token_secret = 's2EJVlVO30RKlsJ7jT1hUVOVb3zDOvYhJg9KOxC4kNcx3'

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api = tweepy.API(auth)


    for names in custs:
        polarity = 0
        subjectivity = 0
        name = str(names.name)
        public_tweets = api.search(name)
        print(name)
        for tweet in public_tweets:
            analysis = TextBlob(tweet.text)
            Sentiment = analysis.sentiment
            polarity += Sentiment.polarity
            subjectivity += Sentiment.subjectivity
            names.pol = polarity
            names.sub = subjectivity
            names.save()



    return render(request,'chat.html',{'custs':custs})        
