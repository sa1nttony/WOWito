from .models import Player


def model_contexts(request):
    if request.user.is_authenticated:
        player_context = Player.objects.get(user = request.user)
        return {'player_context': player_context}
    return request