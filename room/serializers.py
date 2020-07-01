from rest_framework import serializers
from .models import *
import re


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
        figure = self.parent.instance
        # fails the POST (figure is none, so it has no cell)
        if isinstance(data, dict):
            figure.cell = ChessCell.objects.get(grid=figure.cell.grid, x=data['x'], y=data['y'])
        else:
            r = re.match(r'\D*(\d+)\D*(\d+)\D*', data)
            figure.cell = ChessCell.objects.get(grid=figure.cell.grid, x=r.group(1), y=r.group(2))
        figure.save()
        return {'cell.x': figure.cell.x,
                'cell.y': figure.cell.y,
                }


class ChessItemsSerializer(serializers.ModelSerializer):
    available_cells = serializers.SerializerMethodField('get_available_cells')
    # x = serializers.SerializerMethodField('get_x')
    # y = serializers.SerializerMethodField('get_y')
    coordinates = ChessItemCoordinatesField(source='*')

    def get_available_cells(self, item):
        # TODO: Check why tf this method called 4 times in PATCH request
        return item.available_cells()

    # def get_x(self, item):
    #     return item.cell.x
    #
    # def get_y(self, item):
    #     return item.cell.y

    class Meta:
        model = ChessItem
        fields = ['id', 'type', 'coordinates', 'isWhite', 'image', 'available_cells']
        read_only_fields = ['id', 'available_cells', 'image', 'isWhite', 'type']


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
