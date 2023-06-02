from django.shortcuts import render
from .models import BankBranch
from django.core.paginator import Paginator


# Create your views here.
def branches(request):
    branches_lists = BankBranch.objects.all()
    paginator = Paginator(branches_lists, 4)
    page = request.GET.get('page')
    branches_list = paginator.get_page(page)
    context = {'branches': branches_list}
    return render(request, 'branches/branches.html', context)
