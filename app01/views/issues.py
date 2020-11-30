from django.shortcuts import render


def issues(request, project_id):
    """
    wiki首页
    :param request:
    :param project_id:
    :return:
    """

    return render(request, 'issues.html')
