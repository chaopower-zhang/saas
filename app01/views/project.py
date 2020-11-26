# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from app01.forms.project import ProjectModelForm
from django.http import JsonResponse


def project_list(request):
    if request.method == 'GET':

        form = ProjectModelForm(request)

        return render(request, 'project_list.html', {'form': form})

    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.creator = request.trace.user

    return JsonResponse({'status':False, 'error':form.errors})
