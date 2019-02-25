from urllib.parse import quote_plus
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import post
from .forms import PostForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone
#from django.http import HttpResponse
# Create your views here.

def home(request):      #Function base view
    today = timezone.now()
    queryset_list = post.objects.active()   #.filter(draft = False).filter(publish__lte = timezone.now())  #Double slash lte (less or equal than)    #.all().order_by('-timestamp')
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = post.objects.all()
    paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
        'object': queryset,
        'today': today
    }
    return render(request, 'list.html', context)


def listing(request):
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'list.html', {'contacts': contacts})

def create(request):      #Function base view
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfuly Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Created")
    context = {
        "form": form,
    }
    return render(request, 'create.html', context)

def detail(request, slug):      #Function base view
    instance = get_object_or_404(post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    shared_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "shared_string": shared_string,
    }
    return render(request, 'post_detail.html', context)


def update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    print("pass form")
    if form.is_valid():
        print("is valid")
        instance = form.save(commit=False)
        instance.save()
        print("is up")
        messages.success(request, "Successfuly Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Saved")
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, 'create.html', context)

def delete(request, slug):      #Function base view
    if not request.user.is_staff or not request.user.is_superuser:      #Only staff users or administrator are able to make changes
        raise Http404
    instance = get_object_or_404(post, slug=slug)
    instance.delete()
    messages.success(request, "Successfuly Saved")
    return redirect('quoting:home')
