def animefan_context(request):
    if request.user.is_authenticated:
        return {'animefan': request.user}
    return {'animefan': None}