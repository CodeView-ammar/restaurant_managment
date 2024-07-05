from django.shortcuts import render

# Create your views here.
def pos_index(request):
    content={}
    return render(request,"pos/pos_index.html",content)