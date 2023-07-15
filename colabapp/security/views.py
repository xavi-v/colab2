from django.shortcuts import render
from security.forms import StudentForm
from django.contrib.auth.models import Permission

# Create your views here.

def v_signup(request):
    if request.method =='POST':
        data = request.POST.copy() #toma los datos del front-end
        data['username'] = data['email'] #altera los datos previamente
        form = StudentForm(data) #compara con el backend
        if form.is_valid(): # los valida
            us = form.save() # se guarda en base de datos          

            us.is_staff = True #entrego mas capacidades a ese registro de db
            us.is_active = True #entrego mas capacidades a ese registro de db
            us.set_password(data['password']) #cifra contraseña
            us.save() # se vuelve a guardar en base de datos
            perm = Permission.objects.get(name = "Can add subscription")
            us.user_permissions.add(perm) # asignamos permisos
            
        else:
            print(">>", form.errors)

    context ={}
    return render(request, 'signup.html', context)
