from rest_framework import serializers
from .models import *


class GridSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grid
        fields = '__all__'
        abstract = True


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'
        abstract = True
        read_only_fields = ['stackable']


class ChessCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessCell
        fields = ['x', 'y', 'grid']
        read_only_fields = ['stackable']


class ChessGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessGrid
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        abstract = True


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        abstract = True
        read_only_fields = ['max_players']


class ChessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chess
        fields = '__all__'
        read_only_fields = ['max_players']


class ChessItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessItem
        fields = '__all__'


class QueenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queen
        fields = '__all__'


class KingSerializer(serializers.ModelSerializer):
    class Meta:
        model = King
        fields = '__all__'


class BishopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bishop
        fields = '__all__'


class KnightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knight
        fields = '__all__'


class RookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rook
        fields = '__all__'


class PawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pawn
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
