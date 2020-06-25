from django.urls import include, path
from .views import *

crud = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

list_create = {
    'get': 'list',
    'post': 'create'
}

urlpatterns = [
    path('player', PlayerViewSet.as_view(list_create)),
    path('player/<int:pk>', PlayerViewSet.as_view(crud)),
    path('room', RoomViewSet.as_view(list_create)),
    path('room/<int:pk>', RoomViewSet.as_view(crud)),

    path('chess/game', ChessViewSet.as_view(list_create)),
    path('chess/game/<int:pk>', ChessViewSet.as_view(crud)),
    # path('chess/item', ChessItemsViewSet.as_view({'get': 'list'})),
    path('chess/item', ChessItemsViewSet.as_view(list_create)),
    path('chess/item/<int:pk>', ChessItemsViewSet.as_view(crud)),
    path('chess/cell', ChessCellViewSet.as_view(list_create)),
    path('chess/cell/<int:pk>', ChessCellViewSet.as_view(crud)),
    path('chess/grid', ChessGridViewSet.as_view(list_create)),
    path('chess/grid/<int:pk>', ChessGridViewSet.as_view(crud)),
]
