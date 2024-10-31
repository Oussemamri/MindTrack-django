from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('quiz_app:quiz_list')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_app:quiz_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
