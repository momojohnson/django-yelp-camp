from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views import View
import geocoder
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url
from . forms import CampgroundForm, CampgroundEditForm
from . models import Campground
from comments.models import Comment

@method_decorator(login_required, name='dispatch')
class CreateNewCampgroundView(View):
    """ A view for adding campgrounds at route campgrounds/add"""
    def post(self, request):
        """ Handles post request of form data at route campgrounds/add"""
        form = CampgroundForm(request.POST, request.FILES)
        if form.is_valid():
            campground_form = form.save(commit=False)
            g = geocoder.google(campground_form.location)
            if g.json is None:
                messages.error(request, 'The location address you enter is invalid. Please enter a valid address.')
                return redirect(reverse('campgrounds:add_campground'))
            campground_form.location = g.json.get('raw').get('formatted_address')
            campground_form.lat = g.json.get('raw').get('geometry').get('location').get('lat')
            campground_form.lng = g.json.get('raw').get('geometry').get('location').get('lng')
            campground_form.user = request.user
            file_to_upload = request.FILES['image']
            if file_to_upload:
                upload_result = upload(file_to_upload, width=900, height = 500,  use_filename =True)
                campground_form.image_url = upload_result.get('secure_url')
                campground_form.image_id  = upload_result.get('public_id')
                campground_form.save()
            messages.success(request, '{} was added successfully'.format(campground_form.name) )
            return redirect('campgrounds:list_campgrounds')
        return render(request, 'campgrounds/new_campground.html', {'form':form, 'title':'Add Campground'})
    
    def get(self, request):
        """ Handles get request for form at route campgrounds/add """
        form = CampgroundForm()
        return render(request, 'campgrounds/new_campground.html', {'form':form, 'title':'Add Campground'})
        

class ListAllCampgroundsView(ListView):
    """ Handles the displaying of campgrounds at route /campgrounds """
    model = Campground
    context_object_name = 'campgrounds'
    template_name = 'campgrounds/list_all_campgrounds.html'
    paginate_by = 6
    
           
    def get_queryset(self):
        queryset = Campground.objects.all().order_by('-created_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ListAllCampgroundsView, self).get_context_data(**kwargs)
        context['title'] = 'List Campgrounds'
        return context

class CampgroundDetailView(ListView):
    model = Campground
    ontext_object_name = 'campground'
    pk_url_kwarg = "campground_id"
    slug_url_kwarg = 'slug'
    context_object_name = "comments"
    template_name = 'campgrounds/campground_details.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        kwargs['campground'] = self.campground
        kwargs['total_comments'] = Comment.objects.count()
        return super().get_context_data(**kwargs)
 
    
    def get_queryset(self):
        self.campground = get_object_or_404(Campground, pk=self.kwargs.get('campground_id'))
        queryset = self.campground.comments.order_by("-created_at")
        return queryset
    

@method_decorator(login_required, name='dispatch')
class EditCampgroundView(UpdateView):
    """ Handles editing of campgrounds at route /campgrounds/<int:campground_id>/<slug:slug>/"""
    model = Campground
    form_class = CampgroundEditForm
    template_name = 'campgrounds/edit_campground.html'
    pk_url_kwarg = 'campground_id'
    slug_url_kwarg = 'slug'
    context_object_name = 'campground'
    def form_valid(self, form):
        campground = form.save(commit=False)
        g = geocoder.google(campground.location)
        if g.json is None:
            messages.error(self.request, 'The location address you enter is invalid. Please enter a valid address.')
            return redirect(reverse('campgrounds:add_campground'))
        campground.location = g.json.get('raw').get('formatted_address')
        campground.lat = g.json.get('raw').get('geometry').get('location').get('lat')
        campground.lng = g.json.get('raw').get('geometry').get('location').get('lng')
        if self.request.FILES.get('image'):
            destroy(campground.image_id)
            upload_result = upload(self.request.FILES['image'],width=900, height = 500,  use_filename =True)
            campground.image_url = upload_result.get('secure_url')
            campground.image_id  = upload_result.get('public_id')
        campground.save()
        messages.success(self.request, '{} was edited successfully'.format(campground.name))
        return redirect('campgrounds:campground_details', campground_id=campground.pk, slug=campground.slug)
    
@login_required
def delete_campground(request, campground_id, slug):
    campground = get_object_or_404(Campground, id=campground_id, slug=slug)
    name = campground.name
    destroy(campground.image_id)
    campground.delete()
    messages.success(request, '{} was deleted successfully'.format(name))
    return redirect(reverse('campgrounds:list_campgrounds'))
    
    
