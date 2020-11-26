# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect


def project_list(request):
    return render(request, 'project_list.html')
