from rest_framework import serializers
from .models import *
import re
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
        fields = ['game', 'cells_type', 'size_x', 'size_y']
        read_only_fields = ['cells_type', 'size_x', 'size_y']


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
        fields = ['id', 'max_players', 'game_name', 'room', 'chess_grid']
        read_only_fields = ['max_players', 'chess_grid']


class ChessItemCoordinatesField(serializers.Field):
    def to_representation(self, value):
        return {'x': value.cell.x,
                'y': value.cell.y
                }

    def to_internal_value(self, data):
        cell = self.parent.instance.cell
        r = re.match(r'\D+(\d+)\D+(\d+)\D+', data)
        cell.x, cell.y = r.group(1), r.group(2)
        cell.save()
        return {'cell.x': cell.x,
                'cell.y': cell.y
                }


class ChessItemsSerializer(serializers.ModelSerializer):
    available_cells = serializers.SerializerMethodField('get_available_cells')
    # x = serializers.SerializerMethodField('get_x')
    # y = serializers.SerializerMethodField('get_y')
    coordinates = ChessItemCoordinatesField(source='*')

    def get_available_cells(self, item):
        return item.available_cells().values('x', 'y')
        # return ChessCell.objects.all().values('x', 'y')

    # def get_x(self, item):
    #     return item.cell.x
    #
    # def get_y(self, item):
    #     return item.cell.y

    class Meta:
        model = ChessItem
        fields = ['id', 'type', 'coordinates', 'isWhite', 'image', 'available_cells']
        read_only_fields = ['available_cells']


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField('player')

    def player(self, room):
        # return serialize('json', room.player.values_list('id'))
        return room.player.values('id', 'nickname')
        # return room.player.all().serializable_value(id)
        # return room.serializable_value(room__player_id)

    class Meta:
        model = Room
        fields = ['id', 'name', 'players', 'chess_game', 'catan_game']
        read_only_fields = ['players']
