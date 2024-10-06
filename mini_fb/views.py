from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'mini_fb/base.html')