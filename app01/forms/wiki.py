from django import forms

from app01 import models
from app01.forms.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth']

    def __init__(self, request, wiki_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        total_data_list = [("", "请选择"), ]
        data_list = models.Wiki.objects.filter(project=request.tracer.project, parent=None).values_list('id', 'title')
        data_list = [data_set for data_set in data_list if str(data_set[0]) != wiki_id]
        total_data_list.extend(data_list)
        self.fields['parent'].choices = total_data_list
