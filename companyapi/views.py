from django.http import HttpResponse,JsonResponse 
def home_page(request):
    print("home page requested")
    friends=[
        'Faisal',
        'Owais',
        'Adeeb'
    ]
    return JsonResponse(friends,safe=False)