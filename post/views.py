from django.shortcuts import get_object_or_404, redirect
from post.models import Post, Comments
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, StringSerializer, EditPostSerializer

class NewPost(APIView):
    def get(self, request):
        return Response()
    
    def post(self, request):
        temp = EditPostSerializer(data=request.data)
        if temp.is_valid():
            post_title = temp.validated_data['title']
            post_text = temp.validated_data['text']
            new_post = Post.objects.create(title=post_title, text = post_text, bump = 0, author = request.user)
            new_post.save()
        return redirect('feed')


class PostAll(ListAPIView):
    def get_queryset(self):
        return Post.objects.all()
    def get_serializer_class(self):
        return PostSerializer


class PostDetails(APIView):
    def get(self, request, post_id):
        postObj = get_object_or_404(Post, pk=post_id)
        postSerializer = PostSerializer(postObj)
        commentsObjAll = Comments.objects.filter(parent=postObj)
        commentsSerializerAll = CommentSerializer(commentsObjAll, many=True)
        return Response({'post': postSerializer.data, 'comments': commentsSerializerAll.data})
    
    def post(self, request, post_id):
        postObj = get_object_or_404(Post, pk=post_id)
        newCommentSerializer = StringSerializer(data=request.data)
        if newCommentSerializer.is_valid():
            comment_text = newCommentSerializer.validated_data['text']
            new_comment = Comments.objects.create(text=comment_text, bump=0, author=request.user, parent=postObj)
            new_comment.save()
        else:
            print('i dont know what went wrong tbh')
        
        postSerializer = PostSerializer(postObj)
        commentsObjAll = Comments.objects.filter(parent=postObj)
        commentsSerializerAll = CommentSerializer(commentsObjAll, many=True)
        return Response({'post': postSerializer.data, 'comments': commentsSerializerAll.data})
    
    def put(self, request, post_id):
        editPostSerializer = EditPostSerializer(data=request.data)
        if editPostSerializer.is_valid():
            post_title = editPostSerializer.validated_data['title']
            post_text = editPostSerializer.validated_data['text']
            if not post_title or post_title == '':
                Post.objects.filter(pk = post_id).update(text = post_text)
            elif not post_text or post_text == '':
                Post.objects.filter(pk = post_id).update(title = post_title)
            else:
                Post.objects.filter(pk = post_id).update(title=post_title, text = post_text)
        
        postObj = get_object_or_404(Post, pk=post_id)
        postSerializer = PostSerializer(postObj)
        commentsObjAll = Comments.objects.filter(parent=postObj)
        commentsSerializerAll = CommentSerializer(commentsObjAll, many=True)
        return Response({'post': postSerializer.data, 'comments': commentsSerializerAll.data})