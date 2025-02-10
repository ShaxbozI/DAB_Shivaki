from django.shortcuts import render

def page_not_found_view(request, exception=None):
    return render(request, 'error_404.html', status=404)

def server_error_view(request):
    return render(request, 'error_500.html', status=500)
