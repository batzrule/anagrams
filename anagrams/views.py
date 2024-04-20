from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from anagrams.models import Anagram, Comment, Solve, Reply
from django.utils import timezone
import datetime
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib import messages


# Create your views here.


def home (request):
    recent_anagrams = Anagram.objects.order_by('-date_posted')
    todays_anagram = recent_anagrams[0]
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    main_list = [list1, list2, list3, list4]
    for x in range(len(recent_anagrams)):
        main_list[x%4].append(recent_anagrams[x])
    

    context = {}
    context['anagram'] = todays_anagram
    context['recent_anagrams'] = main_list

    '''
    if logged_in(request) == True:
        try:
            solution = Solve.objects.get(anagram=todays_anagram, user=request.user, correct=True)
        except Solve.DoesNotExist:
            solution = None
    else:
        solution = None
    '''

    '''
    for object in Solve.objects.all():
        if object.anagram == todays_anagram:
            if object.user == request.user:
                solved = True
                if object.revealed == True:
                    revealed = True
    
    userlist = []
    times = Solve.objects.order_by('solution_date')
    for x in times:
        if not x.revealed and x.user.username != request.user.username and x.anagram == todays_anagram:
            userlist.append(x.user)
    '''

    
    
    if request.user.is_authenticated :
        try:
            solution = Solve.objects.get(anagram=todays_anagram, user=request.user) 
            ''', correct=True'''
        except:
            solution = None
            try:
                attempt = Solve.objects.get(anagram=todays_anagram, user=request.user)
                ''', correct=True'''
            except:
                attempt = None
            
    else:
        solution = None
        attempt = None
        #print ('no user')
    solutions = Solve.objects.filter(anagram=todays_anagram, revealed=False).order_by('time_taken')
    ''', correct=True'''
    user_solutions = Solve.objects.filter(user=request.user, revealed=False)
    ''', correct=True'''

    solved_anagrams = []
    for item in user_solutions:
        if item.anagram not in solved_anagrams:
            solved_anagrams.append(item.anagram)

    comment_list = Comment.objects.filter(anagram=todays_anagram).order_by('date_posted')
    comment_list = comment_list.reverse()
    try:
        source = request.META['HTTP_REFERER']
    except:
        source = None
    if source == 'anagrams:check solution':
        print ('checked')
        print (request.META['HTTP_REFERER'])
        if solution:
            solved_state = 'correct'
        else:
            solved_state = 'incorrect'
    else:
        print ('unchecked')
        solved_state = 'untried'
    
    
    context ['solutions'] = solutions
    context ['user_solution'] = solution
    context ['user_attempt'] = attempt
    context ['user_solutions'] = user_solutions
    context ['comment_list'] = comment_list
    context ['anon'] = logged_in(request)
    context ['solved_anagrams'] = solved_anagrams
    context ['solved_state'] = solved_state

    return render(request, 'anagrams/home.html', context)

def past_anagrams (request):
    (main_list, difficulty) = make_columns(request.POST)
    

    context = {'fil_dif':difficulty}

    context['recent_anagrams'] = main_list

    return render(request, 'anagrams/past_anagrams.html', context)

def leaderboard (request):
    context = {}
    d = {}
    biglist = []
    solutions = []
    for user in User.objects.all():
        objects = Solve.objects.filter(user=user, revealed=False)
        ''', correct=True'''

        total = 0
        num_sol = 0
        easy = 0
        medium = 0
        hard = 0
        for solution in objects:
            if solution.anagram.was_published_last_month == True:
                total += solution.time_taken
                num_sol += 1
                solutions.append(solution)
                if solution.anagram.difficulty == 'easy':
                    easy += 1
                elif solution.anagram.difficulty == 'medium':
                    medium += 1
                else:
                    hard += 1
        

        if num_sol >= 1:
            mean = total/num_sol
            #points = calculate_points(mean)
            points = calculate_points_weighted(solutions)
            '''
            list = [num_sol, mean, points]
            d[user] = mean
            d[user] = list
            current_user_result = d[request.user]
            '''
            difficulties = [easy, medium, hard]
            list = [user, num_sol, mean, points, difficulties]
            biglist.append(list)


     
    for n in range(0,len(biglist)):
        top = 0
        for x in range(n,len(biglist)):
            item = biglist[x]
            if item[3] >= top:
                top = item[3]
                topitem = x
                
        hold = biglist[n]
        biglist[n] = biglist[topitem]
        biglist[topitem] = hold
    #list is now ordered

    for x in range(len(biglist)):
        biglist[x][2] = time_length(biglist[x][2])
        d[x+1] = biglist[x]

    context['user_list'] = d
    context['solutions'] = solutions

    solves = Solve.objects.filter(user=request.user, correct=True).order_by('time_taken')
    #quickest = time_length(solves[1].time_length)

    context['user_solves'] = solves
    #context['quickest_solution'] = quickest

        
    return render(request, 'anagrams/general_leaderboard.html', context)

@login_required
def check_solution (request, anagram_id):

    user_solution = request.POST['solution']
    
    solved_anagram = get_object_or_404(Anagram, id=anagram_id)
    '''
    try:
        solver = request.user
    except User.DoesNotExist:
        solver = None
    '''
    solver = request.user

    time = int(request.POST['time']) / 1000
    
    if solved_anagram.solution_text == user_solution.lower().strip():
        solved=True
        s = Solve.objects.create(user=solver, anagram=solved_anagram, time_taken=time, correct=True)
        s.save()
        messages.info(request, "Correct")
        print ('correct')
        '''
        if solver:
            s = Solve.objects.create(user=solver, anagram=solved_anagram, time_taken=time)
            s.save()
        else:
            s = Solve.objects.create( anagram=solved_anagram, time_taken=time)
            s.save()
        '''
        

    else:
        messages.info(request, "Incorrect")
        solved = False
        s = Solve.objects.create(user=solver, anagram=solved_anagram, time_taken=time, correct=False)
        s.save()


    return redirect (request.META['HTTP_REFERER'])

def reveal_solution (request, anagram_id):
    revealed_anagram = Anagram.objects.get(id=anagram_id)
    solver = request.user
    solved = False

    s = Solve(anagram=revealed_anagram, user=solver, revealed=True)
    s.save()

    return redirect (request.META['HTTP_REFERER'])

def detail (request, anagram_id):
    detailanagram = get_object_or_404(Anagram, id=anagram_id)
    recent_anagrams = Anagram.objects.order_by('-date_posted')
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    main_list = [list1, list2, list3, list4]
    for x in range(len(recent_anagrams)):
        main_list[x%4].append(recent_anagrams[x])
    context = {'anagram': detailanagram, 'recent_anagrams': main_list}

    '''
    if logged_in(request) == True:
        try:
            solution = Solve.objects.get(anagram=detailanagram, user=request.user)
        except Solve.DoesNotExist:
            solution = None
    else:
        solution = None
    '''
    

    
    if request.user.is_authenticated:
        try:
            solution = Solve.objects.get(anagram=detailanagram, user=request.user)
            ''', correct=True'''
        except:
            solution = None
            try:
                attempt = Solve.objects.get(anagram=detailanagram, user=request.user)
                ''', correct=False'''
            except:
                attempt = None
    else:
        solution = None

    solutions = Solve.objects.filter(anagram=detailanagram, revealed=False, correct=True).order_by('time_taken')
    user_solutions = Solve.objects.filter(user=request.user, revealed=False, correct=True).order_by('time_taken')
    
    solved_anagrams = []
    for item in user_solutions:
        if item.anagram not in solved_anagrams:
            solved_anagrams.append(item.anagram)

    comment_list = Comment.objects.filter(anagram=detailanagram).order_by('date_posted')
    comment_list = comment_list.reverse()


    context ['solutions'] = solutions
    context ['user_solution'] = solution
    context ['user_attempt'] = attempt
    context ['user_solutions'] = user_solutions
    context ['solved_anagrams'] = solved_anagrams
    context ['comment_list'] = comment_list
    context ['anon'] = logged_in(request)


    return render(request, 'anagrams/detail.html', context)


def about_page (request):

    (main_list, difficulty) = make_columns(request.POST)
    

    context = {'fil_dif':difficulty}

    context['recent_anagrams'] = main_list
    return render(request, 'anagrams/about_page.html', context)

   

@login_required
def post_comment (request, anagram_id):
    text = request.POST ['comment text']
    user = request.user
    anagram = Anagram.objects.get(id=anagram_id)
    comment = Comment(text=text, author=user, anagram=anagram)
    comment.save()
    return redirect (request.META['HTTP_REFERER'])

@login_required
def like_comment (request, comment_id):
    
    
    try:
        comment = Comment.objects.get(id=comment_id)
        liker_list = comment.likers.all()
        print (comment.likers.all())
        
        user = request.user

        
        if user in liker_list:
            comment.likers.remove(user)
            comment.save()

        else:
            comment.likers.add(user)
            comment.save()

        print (comment.likers.all())
    
        comment.save()
        
    except comment.DoesNotExist:
        raise Http404('comment does not exist')
    return redirect (request.META['HTTP_REFERER'])


@login_required
def delete_comment (request, comment_id):
    t = Comment.objects.get(id=comment_id)
    t.delete()
    for reply in Reply.objects.all():
        reply.delete()
    return redirect (request.META['HTTP_REFERER'])

@login_required
def create_anagram (request):
    text = request.POST ['anagram text']
    solution_text = request.POST ['solution text']
    author = request.user
    fail = False
    context = {'user': request.user}
    anagrams = Anagram.objects.order_by('-date_posted')
    context['anagrams'] = anagrams
    context ['anon'] = logged_in(request)
    for anagram in Anagram.objects.all():
        if anagram.text == text or anagram.solution_text == solution_text:
            fail = True
    if len(text) < 3 or len(solution_text) < 3 :
        fail = True
    if fail == False:
        if len(text) < 8 :
            difficulty = 'easy'
        elif len(text) > 10 :
            difficulty = 'hard'
        else:
            difficulty = 'medium'
        anagram = Anagram.objects.create(text=text, solution_text=solution_text, difficulty=difficulty, creator=author)
        anagram.save()
    context['fail'] = fail
 
    return render(request,'anagrams/create_anagram.html', context)

@login_required
def create_anagram_page (request):
    context = {'user': request.user}
    anagrams = Anagram.objects.order_by('-date_posted')
    context['anagrams'] = anagrams
    context ['anon'] = logged_in(request)
    
    return render(request, 'anagrams/create_anagram.html', context)

def profile_page (request):
    context = {'user': request.user}
    user = request.user
    solves = Solve.objects.filter(user=user, correct=True)
    number = len(solves)
    context ['solves'] = number
    context ['anon'] = logged_in(request)
    return render (request, 'anagrams/profile.html', context)

#USER STUFF-------------------------------------------------------------------

def login_page (request):
    context = {}
    context ['anon'] = logged_in(request)
    return render(request, 'anagrams/login.html', context)

def signup_page (request):
    context = {}
    context ['anon'] = logged_in(request)
    return render(request, 'anagrams/signup.html', context)

def create_user (request):
    username = request.POST ['username']
    password = request.POST ['password']
    first_name = request.POST ['first_name']
    last_name = request.POST ['last_name']
    email = request.POST ['email_address']

    try:
        new_user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password, email=email, username=username)
        login(request, new_user)
        return redirect('anagrams:about page')
    except:
        return redirect ('anagrams:signup page')

def login_view (request):
    password = request.POST ['password']
    username = request.POST ['username']
    user = authenticate (request, username=username, password=password)
    context = {}
    if user is not None:
        login(request, user)
        print ('logged in')
        context['error_message'] = None
        return redirect('anagrams:home')
    else:
        same_username = User.objects.filter(username=username)
        if same_username == None:
            context['error_message'] = 'No user with this username'
        else:
            context['error_message'] = 'Incorrect password'
        return render(request, 'anagrams/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('anagrams:login page')

    
def logged_in (request):
    if request.user:
        anon = False
    else:
        anon = True
    return anon




def time_length(seconds):
    h = int(seconds// 3600)
    r = int(seconds-(h*3600))
    m = int(r // 60)
    r2 = int(r-(m*60))
    s = int(r2)
    if h <= 10:
        h = '0'+ str(h)
    if m <= 10:
        m = '0' + str(m)
    if s < 10:
        s = '0' + str(s)
    number = (str(h) + ':' + str(m) + ':' + str(s))

    return number

def calculate_points (time):
    points = int(800//time) + 200
    return points

def calculate_points_weighted (solutions):
    totalpoints = 0
    for item in solutions:
        if item.anagram.difficulty == 'easy':
            n = 800
        elif item.anagram.difficulty == 'hard':
            n = 1000
        else:
            n = 1200
        points = int(n//item.time_taken) + 200
        totalpoints += points    
    return totalpoints

def make_columns (posted_data):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    main_list = [list1, list2, list3, list4]

    if posted_data:
        if posted_data['difficulty'] == 'any difficulty':
            difficulty = None
        else:
            difficulty = posted_data['difficulty']

            filtered = Anagram.objects.filter(difficulty=difficulty)
            anagrams = filtered.order_by('-date_posted')



    else:
        difficulty = None
        anagrams = Anagram.objects.order_by('-date_posted')


    for x in range(len(anagrams)):
        main_list[x%4].append(anagrams[x])
    return (main_list, difficulty)
    




