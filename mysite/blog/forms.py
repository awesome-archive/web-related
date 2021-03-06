from django import forms
from .models import Comment
from haystack.forms import SearchForm


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    # Each field type has a default widget that determines how the fields is displayed in HTML
    # The default widget can be overridden with the widget attribute
    # In the comments field, we use a Textarea widget to display it as a <textarea>
    #  HTML element inside of the default <input> element.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class BlogSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()

