from rest_framework import generics, viewsets
from django.db.models import Q
from .serializers import *


# class GameViewSet(viewsets.ModelViewSet):
#     serializer_class = GameSerializer
#     queryset = Game.objects.all()


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()


# class GridViewSet(viewsets.ModelViewSet):
#     serializer_class = GridSerializer
#     queryset = Grid.objects.all()


# class CellViewSet(viewsets.ModelViewSet):
#     serializer_class = CellSerializer
#     queryset = Cell.objects.all().


class ChessViewSet(viewsets.ModelViewSet):
    serializer_class = ChessSerializer
    queryset = Chess.objects.all()


class ChessCellViewSet(viewsets.ModelViewSet):
    serializer_class = ChessCellSerializer
    queryset = ChessCell.objects.all()


class ChessGridViewSet(viewsets.ModelViewSet):
    serializer_class = ChessGridSerializer
    queryset = ChessGrid.objects.all()


class ChessItemsViewSet(viewsets.ModelViewSet):
    serializer_class = ChessItemsSerializer
    queryset = ChessItem.objects.all()


class QueenViewSet(viewsets.ModelViewSet):
    serializer_class = QueenSerializer
    queryset = Queen.objects.all()


class KingViewSet(viewsets.ModelViewSet):
    serializer_class = KingSerializer
    queryset = King.objects.all()


class BishopViewSet(viewsets.ModelViewSet):
    serializer_class = BishopSerializer
    queryset = Bishop.objects.all()


class KnightViewSet(viewsets.ModelViewSet):
    serializer_class = KnightSerializer
    queryset = Knight.objects.all()


class RookViewSet(viewsets.ModelViewSet):
    serializer_class = RookSerializer
    queryset = Rook.objects.all()


class PawnViewSet(viewsets.ModelViewSet):
    serializer_class = PawnSerializer
    queryset = Pawn.objects.all()

