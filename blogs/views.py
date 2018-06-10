from django.shortcuts import render
from .models import Banner,Post,Comment,BlogCategory,FriendlyLink,Tags
from django.views.generic.base import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

#搜索框
class search(View):

    def post(self,request):
        # 获取搜索框输入的内容
        kw=request.POST.get('keyword')
        # 匹配博客的标题或者内容
        post_list=Post.objects.filter(Q(title__contains=kw) | Q(content__contains=kw))


        ctx={
            'post_list':post_list,

        }

        return render(request,'list.html',ctx)

def index(request):
    # 轮播图
    banner_list = Banner.objects.all()
    # 推介博客
    recomment_list=Post.objects.filter(is_recomment=True)
    for recomment in recomment_list:
        recomment.content=recomment.content[:70]+'....'
    # 最新发布
    post_list=Post.objects.all().order_by('-pub_date')
    for count in post_list:
        count.content=count.content[:100]+'......'
    #博客分类
    BlogCategory_list=BlogCategory.objects.all()

    #最新评论
    comment_list = Comment.objects.order_by('-pub_date')
    new_commit_list = []
    for commit in comment_list:
        if commit.post not in new_commit_list:
            new_commit_list.append(commit.post)

    #友情链接
    FriendlyLink_list=FriendlyLink.objects.all()

    #分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(post_list, per_page=1, request=request)
    post_list = p.page(page)

    ctx = {
        'banner_list':banner_list,
        'recomment_list':recomment_list,
        'post_list':post_list,
        'BlogCategory_list':BlogCategory_list,
        'new_commit_list':new_commit_list,
        'FriendlyLink_list':FriendlyLink_list,
    }
    return render(request, 'index.html', ctx)



def list(request,tid=-1,cid=-1):
    #点击标签获取博客
    if tid!=-1:
        cat=Tags.objects.get(id=tid)
        post_list = cat.post_set.all()
    #用分类查询博客
    elif cid != -1:
        cat = BlogCategory.objects.get(id=cid)
        post_list = cat.post_set.all()
    else:
        post_list=Post.objects.order_by('-pub_date')

    #标签云----------------------------------
    tags = Tags.objects.all()
    #取出所有标签放入一个列表中
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tag_message_list.append({'name':t.name,'id':t.id,'count':count})


    ctx={
            'post_list': post_list,
            'tag_message_list': tag_message_list,
        }

    return render(request,'list.html',ctx)

def base(request):
    return render(request, 'base.html')

#详情页
def show(request,sh=-1):
    cht = int(sh)
    if cht != -1:
        post_list = Post.objects.get(id=cht)
    else:
        post_list = Post.objects.filter(is_recomment=True).order_by('-views')
        post_list = post_list[0]
    #最新评论 去重
    comment_list = Comment.objects.order_by('-pub_date')
    new_comment_list = []
    for test in comment_list:
        if test.post not in new_comment_list:
            new_comment_list.append(test.post)
    #标签
    tag_list = post_list.tags.all()

    #相关推介
    tuijie=post_list.category
    tuijie_list=Post.objects.filter(category=tuijie)

    ctx = {
        'post': post_list,
        'new_comment_list':new_comment_list,
        'tuijie_list':tuijie_list,
        'tag_list': tag_list,

    }

    return render(request, 'show.html', ctx)
