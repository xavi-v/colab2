from django.shortcuts import render
from .models import Course, Subscription, Subject, Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
# Create your views here.


def v_index(request):
    context = {
        'course1': Course.objects.get( name = 'Matematica Avanzada'), 
        'course2': Course.objects.get( name = 'Literatura'), 
    }
    return render(request, 'index.html', context)
    #enlaza view con html
    
  
def v_course(request, course_id):
    context = {
        'course': Course.objects.get(id = course_id)
    }
    #traer el ultimo subject del curso
    subject = Subject.objects.filter(course_id = course_id).last()
    if subject is None:        
        return HttpResponseRedirect("/") #redirige a Home
    context['subs'] = subject


    if request.user.is_authenticated:
        if Student.objects.filter(id = request.user.id).exists(): #True si existe
# estoy seguro de que se trata de un estudiante
            verificar = Subscription.objects.filter(subject_id = subject.id, 
                student_id = request.user.id).exists() #retorna True o Flase
            context['subscribed'] = verificar  
            
    return render(request, 'course.html', context)


@login_required(login_url = "/admin/login")
@permission_required('academy.add_subscription', login_url = "/admin/login")

def v_subscribe(request, course_id):
    
    subject = Subject.objects.filter(course_id = course_id).last()
    if subject is None:
        messages.error(request, "No puedes subscribirte en este curso. ")
        return HttpResponseRedirect("/academy/course/%s" % (course_id))


    verificar = Subscription.objects.filter(subject_id = subject.id, student_id = request.user.id)
    if verificar.exists():
        messages.success(request, "Tu subscripcion ya está activa. ")
        return HttpResponseRedirect("/academy/course/%s" % (course_id))
    
    else: 
        subs = Subscription()
        subs.student_id = request.user.id
        subs.subject_id = subject.id
        subs.save()
        messages.success(request, "Finalmente, Ya estás inscrito!!! ")
        return HttpResponseRedirect("/academy/course/%s" % (course_id))

