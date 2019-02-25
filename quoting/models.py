from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

from markdown_deux import markdown    #Use django Markdown library insted of jquery.
from django.utils.safestring import mark_safe   #Allows to Markdown html tags and show content.

# Create your models here.
#These are model managers
#post.objects.all()
#post.objects.create()
#We can modified these query rules in these case post.objects.all()
class postManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(postManager, self).filter(draft = False).filter(publish__lte = timezone.now()) #It is taking the original one and appending filter

class post(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    updated = models.DateField(auto_now=True, auto_now_add=False)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete='CASCADE')
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)

    objects = postManager()     #This is the link for the postManager class. Now we can return the query on views as the origina form
                                #objects is the convention but you can use something else but dont forgeth to change it: post.objects.all()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("quoting:detail", kwargs={'slug': self.slug})
        #return "detail/%s" %(self.id)

    #Use django Markdown library insted of jquery.
    def get_markdown_django(self):
        content = self.content
        marked = markdown(content)
        return mark_safe(marked)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    #slug = slugify(instance.title)
    #exists = post.objects.filter(slug=slug).exists()
    #if exists:
    #    slug = "%s-%s" %(slug, instance.id)
    #instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=post)
