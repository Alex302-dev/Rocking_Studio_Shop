def user_city_context(request):
    if request.user.is_authenticated:
        return {'user_city': request.user.city}
    return {'user_city': None}