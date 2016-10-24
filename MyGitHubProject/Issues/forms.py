from django.forms import Form, CharField, ChoiceField
from MyGitHubProject.Issues.defines import ISSUE_PRIORITY_CHOICES, ISSUE_CATEGORY_CHOICES


class AddIssueForm(Form):
    name = ChoiceField(label='Client Name', required=False)
    action = CharField(label='Action (Item/Request)', required=True, help_text='Enter your problem')
    description = CharField(label='Description', required=False, help_text='Enter a description for your problem')
    priority = ChoiceField(label='Priority', required=False)
    category = ChoiceField(label='Category', required=False)

    def __init__(self, *args, **kwargs):
        list_names = kwargs.get('list_names', None)
        list_priority = kwargs.get('list_priority', None)
        list_category = kwargs.get('list_category', None)
        del kwargs['list_names']
        del kwargs['list_priority']
        del kwargs['list_category']

        super(AddIssueForm, self).__init__(*args, **kwargs)
        self.fields['name'].choices = list_names
        self.fields['priority'].choices = list_priority
        self.fields['category'].choices = list_category

