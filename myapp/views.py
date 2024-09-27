from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from myapp.models import E_learning,feedback,Course,course_skills,enrolled,coursefeedback
import razorpay
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from django.db.models import Q
from django.contrib.auth.decorators import login_required





# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else: 
        us =request.POST['username']
        e = request.POST['email']
        n =  request.POST['name']
        pas = request.POST['password']

        user=User.objects.filter(username = us)
        mil=User.objects.filter(email = e)
        nam = str(User.objects.filter(first_name = n))
        if user.exists():
            messages.warning(request,"username already taken!")
            return redirect('/register')
        
        if mil.exists():
            messages.warning(request,"Email id already exists!")
            return redirect('/register')
        
        if not nam.isalpha():
            # messages.warning(request,"name cant be number!")
            # return redirect('/register')
        

            u=User.objects.create(email=e,first_name=n,username = us)
            u.set_password(pas)
            u.save()
            messages.info(request,'Account created successfully')
            return redirect('/login')
        else:
            messages.warning(request,"name cant be number!")
            return redirect('/register')
            # u=User.objects.create(email=e,first_name=n,username = us)
            # u.set_password(pas)
            # u.save()
            # messages.info(request,'Account created successfully')
            # return redirect('/login')

def login_page(request):
    if  request.method == "GET":
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username = username).exists:
            messages.warning(request,'Invalid username!')
            return redirect('/login')
        
        user = authenticate(username = username , password = password)
        
        if user is None:
            messages.warning(request,'Invalid password!')
            return redirect('/login')
        
        else:
            login(request,user)
            messages.error(request,'Login successfully!')
            return redirect('/')
        
def logout_page(request):
    logout(request)
    messages.error(request,'User logout successfully')
    return redirect('/')

def Elearning(request):
    userid=request.user.id
    context={}
    if userid is None:
        messages.warning(request,'please login so as to watch videos')
        return render(request,'login.html',context)
    else:
        context={}
        data= E_learning.objects.all()
        context['Elearn']=data
        return render(request,'E-learning.html',context)
    
def watchonline(request,id):
    context = {}
    data = E_learning.objects.get(id = id)
    context['watch']=data
    return render(request,'watchonline.html',context)

def feedbackRating(request,id):
    user = request.user
    e_learning_instance = E_learning.objects.get(id=id)
    if request.method == "POST":
        review = request.POST.get('review', 'no feedback given') 
        rating = request.POST.get('rating')

        if not rating:

            messages.error(request, 'Please provide a rating...')
            return redirect(f'http://127.0.0.1:8000/watchonline/{e_learning_instance.id}')  # Redirect to an appropriate page

        # Create and save the Feedback object
        data= feedback.objects.create(uid=user,E_learning_id=e_learning_instance,review=review,ratings=rating)
        data.save()

        # Show a success message
        messages.success(request, 'Thank you for your feedback. Explore more content!')
        return redirect('/e-learning')  # Redirect to an appropriate page after saving
    else:
    # Handle non-POST requests
        return redirect('/e-learning')
    

def courses(request, code):
    userid=request.user.id
    context={}
    if userid is None:
        messages.warning(request,'please login for course detail')
        return render(request,'login.html',context)
    else:
        context = {}
        
        # Get course data
        course_data = Course.objects.get(title=code)
        context["course"] = course_data

        # Get course skills data
        course_skill_data = course_skills.objects.filter(course_name=code)
        
        # Prepare the course skills and chapters data
        skills_chapters = []
        for skill in course_skill_data:
            chapters = skill.chapter.split(',')  # Split the chapter string by comma
            skills_chapters.append({
                'skill': skill.skill,  # Include the skill name
                'chapter_list': [chapter.strip() for chapter in chapters]  # List of chapters
            })
        
        context["course_skills"] = skills_chapters

        return render(request, "c++_course.html", context)



def payment(request,code):
    context={}
    user = request.user
    data = Course.objects.get(title = code)
    client = razorpay.Client(auth=("rzp_test_tIqAd7OXqu2xWS", "Nt4xEdPZ2llmou7xC55FfCmq"))
    data = { "amount":data.fees*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context["data"]=payment
    context["course"]=code
    # context={'data':payment}
    # context={"course":code}
    return render(request,'pay.html',context)



def enrolled_user(request, title):
    context = {}
    user = request.user
    title = unquote(title)
    

    # Fetch the course instance or return a 404 error if not found
    course_instance = get_object_or_404(Course, title=title)

    # Create a new enrollment record
    enrolled.objects.create(uid=user, course_name=course_instance, paid=True)

    # Send email confirmation
    msg_body = 'Your order has been placed successfully.'
    user_email = user.email

    send_mail(
        'Course Enrollment Confirmation',  # Subject
        msg_body,  # Message body
        "dharmeshhh011@gmail.com",  # From email
        [user_email],  # To email
        fail_silently=False,
    )

    # Add a message to be displayed on the next page
    messages.success(request, 'Course purchase completed successfully! The premium section is now unlocked. Enjoy your new content!')

    # Render the response with context
    return redirect("/")



def course_menu(request):
    course_data = Course.objects.all()
    context={"data":course_data}
    return render(request,'courseMenu.html',context)


@login_required(login_url='login_page')
def premium(request):
    user = request.user
    enrollments = enrolled.objects.filter(uid=user)

    # Check if there's any enrollment where paid is True
    if enrollments.filter(paid=False).exists():
        return redirect('/courseMenu')   


    # courseDetail = Course.objects.filter(title=enrollments)
    course_details = Course.objects.filter(enrolled__in=enrollments).distinct()
    
    context = {"data":course_details,"customer":user}
    return render(request, 'premium.html',context)


def watchpremium(request,title):
    context = {}
    data = Course.objects.get(title = title)
    context['watchp']=data
    return render(request,'watchpremiume.html',context)


def coursefeedbackandrating(request,title):
    user = request.user
    e_learning_instance = Course.objects.get(title=title)
    if request.method == "POST":
        review = request.POST.get('review', 'no feedback given') 
        rating = request.POST.get('rating')

        # if not rating:

        #     messages.error(request, 'Please provide a rating...')
        #     return redirect(f'http://127.0.0.1:8000/watchonline/{e_learning_instance.id}')  # Redirect to an appropriate page

        # Create and save the Feedback object
        data= coursefeedback.objects.create(uid=user,course_title=e_learning_instance,review=review,ratings=rating)
        data.save()

        # Show a success message
        messages.success(request, 'Thank you for your feedback. Explore more content!')
        return redirect('/e-learning')  # Redirect to an appropriate page after saving
    else:
    # Handle non-POST requests
        return redirect('/e-premium')
    
def support(request,title):
    messages.error(request,"Our expert will get in touch with you shortly to schedule a one-on-one doubt-solving session. We’re here to help you with any questions you have!")
    data=Course.objects.get(title = title)
    return redirect(f"http://127.0.0.1:8000/watchpremium/{title}")


def sortrange(request,ord):
    col=''
    if ord == 'asc':
     col='fees'
    else:
        col= '-fees'
    clist = Course.objects.all().order_by(col)
    context={'data':clist}
    return render(request,'courseMenu.html',context)

# def searchttitle(request):
#     query = request.GET.get('query', '')
#     courses = Course.objects.filter(title__icontains=query)  # Filter courses by title
#     return render(request, 'courseMenu.html', {'courses': courses})

def search_courses(request):
    query = request.GET.get('query', '')
    courses = Course.objects.filter(title__icontains=query)  # Filter courses by title
    return render(request, 'courseMenu.html', {'courses': courses, 'query': query})



