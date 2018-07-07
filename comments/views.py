from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views import View
from campgrounds.models import Campground
from . forms import CommentForm
from . models import Comment


@method_decorator(login_required, name='dispatch')
class CreateNewCommentView(View):
    """ Create new comment added by user at route campgrounds/<int:campground_id>/<slug:slug>/comments/add """
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        campground = None
        if form.is_valid():
            comment_form = form.save(commit=False)
            campground = get_object_or_404(Campground, id=kwargs.get('campground_id'), slug=kwargs.get('slug'))
            comment_form.user = request.user
            comment_form.campground = campground
            comment_form.save()
            messages.success(request, 'Comment for {} successfully Added.'.format(campground.name))
            return redirect(reverse('campgrounds:campground_details', kwargs={'campground_id':campground.id, 'slug':campground.slug}))
        return render(request, 'comments/new_comment.html', {'form':form, 'campground':campground, 'title':'Add Comment'})
        
    
    def get(self, request, *args, **kwargs):
        """ Render the form for the user to add a comment """
        """ Render a form for a user to add a comment for a campground at route /campgrounds/<int:campground_id>/<slug:slug>/comments/add """
        campground = get_object_or_404(Campground, id=kwargs.get('campground_id'), slug=kwargs.get('slug'))
        form = CommentForm()
        return render(request, 'comments/new_comment.html', {'form':form, 'campground':campground, 'title':'Add Comment'})

@method_decorator(login_required, name='dispatch')
class UpdateCommentView(UpdateView):
    model = Comment
    fields = ('comment', )
    template_name = 'comments/edit_comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'
    

    def form_valid(self, form):
        self.comment = form.save(commit=False)
        self.comment.save()
        return redirect(reverse('campgrounds:campground_details', kwargs={'campground_id':self.comment.campground.pk, 'slug':self.comment.campground.slug}))
    
    
@login_required           
def delete_comment(request, campground_id, slug, comment_id):
    """ Handles delete operation for a comment at route campgrounds/<int:campground_id>/<slug:slug>/comments/<int:comment_id>/"""
    campground = get_object_or_404(Campground, pk=campground_id, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id, campground=campground)
    comment.delete()
    return redirect(reverse('campgrounds:campground_details', kwargs={'campground_id':campground.id, 'slug':campground.slug}))
    