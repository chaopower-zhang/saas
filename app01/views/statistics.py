from django.shortcuts import render


def statistics(request, project_id):
    """
    wiki首页
    :param request:
    :param project_id:
    :return:
    """

    return render(request, 'statistics.html')
