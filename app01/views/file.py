from django.shortcuts import render


def file(request, project_id):
    """
    wiki首页
    :param request:
    :param project_id:
    :return:
    """

    return render(request, 'file.html')
