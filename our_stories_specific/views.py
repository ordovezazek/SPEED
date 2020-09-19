# from .models import *
# from .forms import CommentForm
# from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404

# def post_detail(request, slug):
#     template_name = "ourstoriesspecific/our_stories_specific.html"
#     post = get_object_or_404(OurStoriesSpecific, slug=slug)
#     comments = post.comments.filter(active=True, Parent__isnull=True)
#     # new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             Parent_obj = None
#             try:
#                 Parent_id = int(request.POST.get('Parent_id'))
#             except:
#                 Parent_id = None
#             if Parent_id:
#                 Parent_obj = Comment.objects.get(id=Parent_id)
#                 if Parent_obj:
#                     reply_comment = comment_form.save(commit=False)
#                     reply_comment.Parent = Parent_obj
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.save()
#            #return redirect('OurStoriesSpecific:detail', slug)
#     else:
#         comment_form = CommentForm()

#             # Create Comment object but don't save to database yet
#             # new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             # Save the comment to the database



#     return render(request, template_name, {'post': post,
#                                            'comments': comments,
#                                            # 'new_comment': new_comment,
#                                            'comment_form': comment_form})
