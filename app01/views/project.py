# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from app01.forms.project import ProjectModelForm

def project_list(request):

    form = ProjectModelForm(request)

    return render(request, 'project_list.html', {'form': form})
