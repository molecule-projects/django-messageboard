# messageboard/views.py

from django.shortcuts import redirect, render, get_object_or_404

from .forms import MessageboardForm, CommentForm
from .models import Message


def messageboard_list_view(request):
    """
    一覧を表示するview
    """
    form = MessageboardForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.message = f"{form.cleaned_data.get('message')} - by.{form.cleaned_data.get('nickname')}"
        obj.save()
        form = MessageboardForm()

    queryset = Message.objects.all()  # 全てのデータを取得する
    context = {
        'object_list': queryset,
        'form': form,
    }
    template_name = 'messageboard/list.html'
    return render(request, template_name, context)


def messageboard_detail_view(request, pk):
    """
    詳細を表示するview
    """
    obj = get_object_or_404(Message, id=pk)
    form = CommentForm()
    comments = obj.comments.all()
    context = {
        'object': obj,
        'form': form,
        'comments': comments,
    }
    template_name = 'messageboard/detail.html'
    return render(request, template_name, context)


def messageboard_comment_to_message_view(request, pk):
    comment_form = CommentForm(request.POST, None)
    if comment_form.is_valid():
        message_obj = get_object_or_404(Message, pk=pk)
        # 情報を追加するために保存を一時停止
        comment_obj = comment_form.save(commit=False)
        # コメントをしているメッセージを紐付ける
        comment_obj.message = message_obj
        # コメントを保存
        comment_obj.save()
        # コメントの保存が終わったらメッセージ画面へリダイレクト。
        # しかし、これはGET、POST処理に構わず行われるのでここで別途リダイレクトしなくてもif文の外でリダイレクトしてくれる
        # return redirect('messageboard:detail', pk=pk)
    # このviewにgetで直接アクセスされた場合、もしくはFormが不正の場合はメッセージに直接戻る
    return redirect('messageboard:detail', pk=pk)
