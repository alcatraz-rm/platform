from django import forms
from questions.models import Response, Problem, Section


class CommentForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('body',)


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, section):
        return "%s " % section.name


class NewProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('title', 'body', 'topics', 'problem_type', 'is_anonymous')

    topics = CustomMMCF(queryset=Section.objects.all(),
                        widget=forms.CheckboxSelectMultiple
                        )
