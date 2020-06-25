from rest_framework import serializers
from .models import *
from django.core.serializers import serialize


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
    available_cells = serializers.SerializerMethodField('get_available_cells')
    x = serializers.SerializerMethodField('get_x')
    y = serializers.SerializerMethodField('get_y')

    def get_available_cells(self, item):
        return item.available_cells().values('x', 'y')
        # return ChessCell.objects.all().values('x', 'y')

    def get_x(self, item):
        return item.cell.x

    def get_y(self, item):
        return item.cell.y

    class Meta:
        model = ChessItem
        fields = ['id', 'type', 'x', 'y', 'isWhite', 'image', 'available_cells']
        read_only_fields = ['available_cells', 'x', 'y']

#
# class QueenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Queen
#         fields = '__all__'
#
#
# class KingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = King
#         fields = '__all__'
#
#
# class BishopSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bishop
#         fields = '__all__'
#
#
# class KnightSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Knight
#         fields = '__all__'
#
#
# class RookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rook
#         fields = '__all__'
# class PawnSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pawn
#         fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField('player')

    def player(self, room):
        # return serialize('json', room.player.values_list('id'))
        return room.player.values('id', 'nickname')
        # return room.player.all().serializable_value(id)
        # return room.serializable_value(room__player_id)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['players']
