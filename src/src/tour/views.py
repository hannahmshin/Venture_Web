from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import tour_user, Tour, stops
from .forms import tour_user_Form, UserForm, Tour_Form, Stop_Form
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.



'''Overlap'''

#need to fix this.. update but the update doesn't really get applied
@login_required
def profile_page(request):

    current_user = request.user
    user = User.objects.get(pk=current_user.pk)
    tour_user_obj = tour_user.objects.get(pk=current_user.pk)
    user_form = UserForm(instance=user)

    #TESTING PURPOSE#

    ProfileInlineFormset = inlineformset_factory(User, tour_user, fields=('User_Gender', 'phone_number', 'about_you', 'profile_picture', 'languages', 'work', 'hometown', 'alma_meter', 'hobbies',))
    formset = ProfileInlineFormset(instance=user)
    

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
 
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
 
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/tourist/profile/')
 
        return render(request, "tourist/edit_your_profile.html", {
            'current_user' :current_user,
            "form": user_form,
            "formset": formset,
            'user_obj':tour_user_obj,
        })
    else:
        raise PermissionDenied

@login_required
def profile_page_preferences(request):
    current_user = request.user
    context_dict = {
        'current_user': current_user.username,
    }
    return render(request, "tourist/profile_preference.html", context_dict)

@login_required
def tour_detail_page(request, slug=None):
    #instance = Post.objects.get(id = 3) #could raise an error because of id might not exist
    tour_obj = get_object_or_404(Tour, slug=slug) #will give standard 404 eror 

    Stops = stops.objects.all().filter(tour=tour_obj)
    tour_instance = tour_obj
    instance = Stops



    context = {
        "instance" : tour_obj,
        "tour_instance": instance,
    }

    return render(request, "tourguide/tour_detail.html", context)
'''Overlap Ends'''









''' This is TOURIST VIEWS '''
def main_page(request):
    current_user = request.user
    context_dict = {'current_user' :current_user.username }
    return render(request, "tourist/main.html", context_dict)


def about_page(request):
    current_user = request.user
    context_dict = {'current_user' :current_user.username }
    return render(request, "tourist/about.html", context_dict)





#####################################
######## SEARCH PAGES ###############
#####################################

def search_page(request):
    current_user = request.user
    queryset_list = Tour.objects.all()
    #Basic search functionality
    query = request.GET.get("q")
    print "Initial query", query
    if query:
        queryset_list = queryset_list.filter(title__icontains = query)
    context_dict = {
        'current_user' :current_user.username,
        'object_list' : queryset_list,
        'city_name': query,
    }

    request.session['query'] = query
    print query, request.session['query']


    if not query: 
        return render(request, "tourist/search.html", context_dict)
    else:
        return render(request, "tourist/search_result.html", context_dict)



def explore_tour_view(request, slug):
    current_user = request.user
    tour_obj = get_object_or_404(Tour, slug=slug)

    author_user_obj = tour_obj.author
    author_tour_user_obj = tour_user.objects.get(pk=author_user_obj.pk)



    Stops = stops.objects.all().filter(tour=tour_obj)
    tour_instance = tour_obj
    context_dict = {
        'current_user': current_user.username,
        'object':tour_obj,
        'stops':Stops,
        'author':author_tour_user_obj,
        'author_user':author_user_obj,

    }


    return render(request, "tourist/explore_tour.html", context_dict)
    














#Need to implement my page according to the user
@login_required
def my_page(request):
    current_user = request.user
    user_obj = User.objects.get(pk=current_user.pk)
    tour_user_obj = tour_user.objects.get(pk=current_user.pk)


    context_dict = {'current_user' :current_user,
                    'user_obj':user_obj,
                    'tour_user_obj':tour_user_obj,
                     }

    return render(request, "tourist/mypage.html", context_dict)

''' TOURIST VIEWS END '''




















''' THIS IS TOURGUIDE VIEW '''
#Users can create their own tour
@login_required
def create_page(request):

    '''This keeps track of where I am on the website. Think a better way of keep track of current location
    This is for delete page.'''
    request.session['loc'] = 'create_page'



    current_user = request.user
    queryset_list = Tour.objects.all() 
    context_dict = {'current_user' :current_user.username,
                    'object_list' : queryset_list, }

    print request.session['loc']
    return render(request, "tourguide/create_your_tours.html", context_dict)

#What tours have user forgot to finish?
@login_required
def create_in_progress(request):

    request.session['loc'] = 'in_progress'
    current_user = request.user
    #Get user specific tour that is in draft mode
    queryset_list = Tour.objects.filter(author = current_user)
    #We want to display all these tours
    objects = queryset_list
    

    tour_exists = True
    if(len(queryset_list) == 0):
        tour_exists = False


    context_dict = {
                    'current_user':current_user.username,
                    'objects':objects,
                    'tour_exists':tour_exists,
                    # 'tour_id_session':tour_id_session,
                    # 'stop1_session':stop1_session,
                    # 'stop2_session':stop2_session,
                    # 'stop3_session':stop3_session,
                     }
    return render(request, "tourguide/inprogress.html", context_dict)


@login_required
def clear_the_form(request):
    #just clear all the session id's and return to basic information input 
    if 'tour_id' in request.session:
        del request.session['tour_id']
    if 'stop1' in request.session:
        del request.session['stop1']
    if 'stop2' in request.session:
        del request.session['stop2']
    if 'stop3' in request.session:
        del request.session['stop3']
    return HttpResponse('OK')




#i think it is safe to have slug as filtering variable because it is unique, and will never had
#dupliactes because itself already contains tour_id
@login_required
def delete_tour_instance(request, slug):
    tour_obj = get_object_or_404(Tour, slug=slug)
    if request.user.is_staff or tour_obj.author == request.user:
        Tour.objects.get(slug=slug).delete()
        #message.success(request, "Sucessfully deleted a tour")
    
    if 'loc' in request.session:
        if request.session['loc'] == "create_page":
            return create_page_yourtour(request)
        elif request.session['loc'] == "in_progress":
            return create_in_progress(request)
    else:
        return create_page_yourtour(request)


#later instead of loading whole page, learn how to load part of the page
@login_required
def create_page_yourtour(request):




    request.session['loc'] = 'create_page'
    #Get tours that are not in draft mode
    queryset_list = Tour.objects.all().filter(draft=False, author=request.user) 
    #check to see if the user created any tours
    tour_exists = True
    if(len(queryset_list) == 0):
        tour_exists = False
    
    context = {
        "tour_exists":tour_exists,
        "object_list" : queryset_list,
    }

    return render(request, "tourguide/create_your_tours.html", context)









@login_required
def create_page_create(request):
    current_user = request.user

    #Creating the for the first time
    if request.method == "POST" and not 'tour_id' in request.session:
        form = Tour_Form(request.POST or None,request.FILES or None)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = current_user
            instance.progress = '25%' #if the user is on the first page, she has done 25 percent of work
            instance.draft = True #HERE SET THE DRAFT MODE TO TRUE. FALSE AFTER REVIEW
            instance.save()
            request.session['tour_id'] = instance.id
            
        else:
            print form.errors

    #Updaing the exisiting form
    elif request.method == "POST" and 'tour_id' in request.session:
        Tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
        form = Tour_Form(request.POST or None, instance = Tour_obj)
        if form.is_valid():
            request.session['tour_id'] = Tour_obj.id
            form.save()

    #Retrieve information if user clicks on this link
    else:
        if 'tour_id' in request.session:
            try:
                Tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
                form = Tour_Form(request.POST or None,instance = Tour_obj)
                
            except:
                del request.session['tour_id']
                form = Tour_Form(request.POST or None,request.FILES or None)
        else:
            form = Tour_Form(request.POST or None,request.FILES or None)

    context_dict = {
        'current_user' :current_user.username,
        # 'form_user':form_user,
        'form':form,
    }
    
    return render(request, "tourguide/create_create.html", context_dict)

@login_required
def create_page_stop_1(request):
    current_user = request.user
    #check if the user filled out the basic information
    #include some sort of message 
    if 'tour_id' not in request.session:
        #need some way to give user an error message
        #or go back to the basic information
        return HttpResponseRedirect("/tourist/create/create_tours")

    if request.method == "POST" and not 'stop1' in request.session:
        tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
        form = Stop_Form(request.POST or None, request.FILES or None)

        if form.is_valid():
            
            stop = form.save(commit=False)
            stop.tour = tour_obj

            #Update tour progress
            tour_obj.progress = "50%"
            tour_obj.save()

            stop.save()
 
            request.session['stop1'] = stop.id
            print request.session['stop1']
            
            
        else:
            print form.errors
     
    else: 
        if 'tour_id' in request.session and 'stop1' in request.session:

            tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
            stop_obj = get_object_or_404(stops, id=request.session['stop1'])
            form = Stop_Form(request.POST or None, request.FILES or None, instance = stop_obj)

            print tour_obj.progress
            if form.is_valid():
                form.save()
        else:
            form = Stop_Form(request.POST or None, request.FILES or None)

    context_dict = {
        'current_user' :current_user.username,
        # 'form_user':form_user,
        'form':form,
    }
    
    return render(request, "tourguide/stop1.html", context_dict)



@login_required
def create_page_stop_2(request):
    current_user = request.user
    #check if the user filled out the basic information
    if 'tour_id' and 'stop1' not in request.session:
        #need some way to give user an error message
        #or go back to the basic information
        return HttpResponseRedirect("/tourist/create/create_tours")

    if request.method == "POST" and not 'stop2' in request.session:
        tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
        form = Stop_Form(request.POST or None, request.FILES or None)

        if form.is_valid():
            
            stop = form.save(commit=False)
            stop.tour = tour_obj

            #update tour object progress variable
            tour_obj.progress = "75%"
            tour_obj.save()
            
            stop.save()
            request.session['stop2'] = stop.id
            
            
        else:
            print form.errors
     
    else: 
        if 'tour_id' in request.session and 'stop1' in request.session and 'stop2' in request.session:

            tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
            stop_obj = get_object_or_404(stops, id=request.session['stop2'])
            form = Stop_Form(request.POST or None, request.FILES or None, instance = stop_obj)

            if form.is_valid():
                form.save()
        else:
            form = Stop_Form(request.POST or None, request.FILES or None)      
    # form = Tour_Form(request.POST or None,request.FILES or None)
    context_dict = {
        'current_user' :current_user.username,
        # 'form_user':form_user,
        'form':form,
    }
    
    return render(request, "tourguide/stop2.html", context_dict)




#STOP3
@login_required
def create_page_stop_3(request):
    current_user = request.user
    #check if the user filled out the basic information

    if 'tour_id' not in request.session or 'stop1' not in request.session or 'stop2' not in request.session:
        #need some way to give user an error message
        #or go back to the basic information
        return HttpResponseRedirect("/tourist/create/create_tours")

    if request.method == "POST" and not 'stop3' in request.session:
        tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
        form = Stop_Form(request.POST or None, request.FILES or None)

        if form.is_valid():
            
            stop = form.save(commit=False)
            stop.tour = tour_obj
            tour_obj.progress = "90%"
            tour_obj.save()
            stop.save()
            request.session['stop3'] = stop.id
            
            
        else:
            print form.errors
     
    else: 
        if 'tour_id' in request.session and 'stop1' in request.session and 'stop2' in request.session and 'stop3' in request.session:

            tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
            stop_obj = get_object_or_404(stops, id=request.session['stop3'])
            form = Stop_Form(request.POST or None, request.FILES or None, instance = stop_obj)

            if form.is_valid():
                form.save()
        else:
            form = Stop_Form(request.POST or None, request.FILES or None)      
    # form = Tour_Form(request.POST or None,request.FILES or None)
    context_dict = {
        'current_user' :current_user.username,
        # 'form_user':form_user,
        'form':form,
    }
    
    return render(request, "tourguide/stop3.html", context_dict)

@login_required
def create_page_review(request):
    current_user = request.user

    #if at least one of the forms are not completed, bring the user back to the first page
    if 'stop3' not in request.session:
        #need some way to give user an error message
        #or go back to the basic information
        return HttpResponseRedirect("/tourist/create/create_tours")

    tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
    Stops = stops.objects.all().filter(tour=tour_obj)
    tour_instance = tour_obj
    instance = Stops



    context_dict = {
        'current_user':current_user.username,
        'tour_instance':tour_instance,
        'instance':instance,
        
    }

    return render(request, "tourguide/review.html", context_dict)

@login_required
def finish_review(request):
    #After finish button is pressed, clear of all the sessions variable and creater another view with some information
    current_user = request.user

    tour_obj = get_object_or_404(Tour, id=request.session['tour_id'])
    form = Tour_Form(request.POST or None,request.FILES or None,instance=tour_obj)
        
    instance = form.save(commit=False)
    instance.draft = False #Not a draft anymore
    instance.save()
    


    #delete all the session variables
    del request.session['tour_id']
    del request.session['stop1']
    del request.session['stop2']
    del request.session['stop3']

    return render(request, "tourguide/review_finish.html")

#when user press edit page
@login_required
def eidt_tour_instance(request, slug):
    tour_obj = get_object_or_404(Tour, slug=slug)
    #check the progress, so I know how many stops user has already created
    if request.user.is_staff or tour_obj.author == request.user:

        if tour_obj.progress == "25%":
            request.session['tour_id'] = tour_obj.id

        else:
            #if there is only one stop it will return one stop, otherwise many stops
            stop_obj = stops.objects.all().filter(tour=tour_obj)
            stop_string = 'stop'
            counter = 1
            for stop in stop_obj:
                session_var = stop_string + str(counter)
                request.session[session_var] = stop.id

    return create_page_create(request)

''' TOURGUIDE VIEW END '''






































