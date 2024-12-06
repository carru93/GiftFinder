from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Layout, Submit
from django import forms

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {
            "title": "Post Title",
            "content": "Content",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter post title"}),
            "content": forms.Textarea(attrs={"placeholder": "Write your post here..."}),
        }

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("title", css_class="form-input mb-4"),
            Field("content", css_class="form-textarea mb-4", rows=10),
            Div(
                Button(
                    "cancel",
                    "Cancel",
                    css_class="ng-btn-secondary",
                    onclick="window.history.back()",
                ),
                Submit("submit", "Create Post", css_class="ng-btn"),
                css_class="flex justify-end space-x-2",
            ),
        )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": "Your Comment",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Write your comment here..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("content", css_class="form-textarea mb-4", rows=5),
            Div(
                Button(
                    "cancel",
                    "Cancel",
                    css_class="ng-btn-secondary",
                    onclick="window.history.back()",
                ),
                Submit("submit", "Comment", css_class="ng-btn"),
                css_class="flex justify-end space-x-2",
            ),
        )
