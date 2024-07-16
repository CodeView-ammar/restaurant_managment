from django.shortcuts import render
from input.models import Items
# Create your views here.
def pos_index(request):
    item_=Items.objects.all()
    content={
        "items":item_
    }
    return render(request,"pos/pos_index.html",content)