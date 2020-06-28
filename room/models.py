from django.db import models
from django.db.models import F
import json


class Grid(models.Model):
    game = models.OneToOneField('Game', models.CASCADE, related_name='grid')
    cells_type = models.CharField(max_length=16, verbose_name='cells_type', db_index=True)
    size_x = models.IntegerField(verbose_name='size_x', db_index=True)
    size_y = models.IntegerField(verbose_name='size_y', db_index=True)

    class Meta:
        abstract = True


class ChessGrid(Grid):
    game = models.OneToOneField('Chess', models.CASCADE, related_name='chess_grid')
    cells_type = models.CharField(max_length=16, verbose_name='cells_type', db_index=True, default='tetragonal',
                                  blank=True)
    size_x = models.IntegerField(verbose_name='size_x', db_index=True, default=8, blank=True)
    size_y = models.IntegerField(verbose_name='size_y', db_index=True, default=8, blank=True)


class CatanGrid(Grid):
    game = models.OneToOneField('Catan', models.CASCADE, related_name='catan_grid')
    cells_type = models.CharField(max_length=16, verbose_name='cells_type', db_index=True, default='hexagonal',
                                  blank=True)


class Cell(models.Model):
    x = models.IntegerField(verbose_name='x', db_index=True)
    y = models.IntegerField(verbose_name='y', db_index=True)
    stackable = models.BooleanField(verbose_name='stackable', db_index=True, default=True)
    grid = models.ForeignKey("Grid", on_delete=models.CASCADE, related_name='cell')

    def add_item(self):
        if self.stackable or self.item.count() == 0:
            pass

    class Meta:
        abstract = True


class ChessCell(Cell):
    stackable = models.BooleanField(verbose_name='stackable', db_index=True, default=False)
    # grid = models.ForeignKey("Grid", on_delete=models.CASCADE, related_name='chess_cell')
    grid = models.ForeignKey("ChessGrid", on_delete=models.CASCADE, related_name='cell')


class CatanCell(Cell):
    # grid = models.ForeignKey("Grid", on_delete=models.CASCADE, related_name='catan_cell')
    grid = models.ForeignKey("CatanGrid", on_delete=models.CASCADE, related_name='cell')


class Item(models.Model):
    cell = models.ForeignKey("Cell", on_delete=models.CASCADE, related_name='item')
    type = models.CharField(max_length=64, verbose_name='type', db_index=True)
    image = models.ImageField(upload_to='uploads/')

    class Meta:
        abstract = True


class ChessItem(Item):
    """
    Possible types:
    King
    Queen
    Bishop
    Knight
    Rook
    """
    cell = models.ForeignKey("ChessCell", on_delete=models.CASCADE, related_name='chess_item')
    isWhite = models.BooleanField(verbose_name='isWhite', db_index=True)
    image = models.ImageField(upload_to='uploads/chess/%d/%m/%Y', blank=True, null=True)

    def can_move(self, cell):
        if self.type == 'King':
            return (cell.chess_item.count() == 0 or
                    cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
                   self.cell != cell and \
                   abs(cell.x - self.cell.x) < 2 and \
                   abs(cell.y - self.cell.y) < 2

        if self.type == 'Queen':
            return True
            return (cell.chess_item.count() == 0 or
                    cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
                   self.cell != cell and \
                   (abs(cell.x - self.cell.x) == abs(cell.y - self.cell.y) or
                    abs(cell.x - self.cell.x) == 0 or
                    abs(cell.y - self.cell.y) == 0)

        if self.type == 'Bishop':
            return True
            return (cell.chess_item.count() == 0 or
                    cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
                   ChessCell.objects.filter(grid=cell.grid, x__range=(cell.x, self.cell.x), y__range=(cell.y, self.cell.y), x=F('y')).exclude(id=cell.id).exists() and \
                   abs(cell.x - self.cell.x) == abs(cell.y - self.cell.y)

        if self.type == 'Knight':
            return True
            return (cell.chess_item.count() == 0 or
                    cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
                   (abs(cell.x - self.cell.x) == 1 and abs(cell.y - self.cell.y) == 2) or \
                   (abs(cell.x - self.cell.x) == 2 and abs(cell.y - self.cell.y) == 1)

        if self.type == 'Rook':
            return True
            return (cell.chess_item.count() == 0 or
                    cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
                   self.cell != cell and \
                   (abs(cell.x - self.cell.x) == 0 or
                    abs(cell.y - self.cell.y) == 0)

        if self.type == 'Pawn':
            right_dir = cell.y - self.cell.y == (1 if self.isWhite else -1)
            if cell.chess_item.exists():
                return cell.chess_item.only('isWhite')[0].isWhite != self.isWhite and \
                       abs(cell.x - self.cell.x) == 1 and \
                       right_dir
            else:
                return cell.x == self.cell.x and right_dir

    def move(self, cell):
        cell.chess_item.delete()
        cell.chess_item = self
        cell.save()

    def available_cells(self):
        return ChessCell.objects.filter(
            id__in=[x.id for x in ChessCell.objects.all().filter(grid=self.cell.grid) if self.can_move(x)])
        # return ChessCell.objects.filter(grid=self.cell.grid).filter(self.can_move(F()))

    def can_transform(self):
        pass

    def transform(self):
        pass


class CatanItem(Item):
    cell = models.ForeignKey("CatanCell", on_delete=models.CASCADE, related_name='catan_item')
    image = models.ImageField(upload_to='uploads/catan/', blank=True, null=True)


class Player(models.Model):
    nickname = models.CharField(verbose_name='nickname', db_index=True, max_length=32)
    is_host = models.BooleanField(verbose_name='is_host', db_index=True, default=False)
    room = models.ForeignKey("Room", on_delete=models.DO_NOTHING, related_name='player')
    # is_spectator = models.BooleanField(verbose_name='is_spectator', db_index=True, default=False)


class Game(models.Model):
    max_players = models.IntegerField(verbose_name='max_players')
    game_name = models.CharField(verbose_name='game_name', db_index=True, max_length=32)
    room = models.OneToOneField('Room', on_delete=models.CASCADE, related_name='game')

    def have_places(self):
        return self.max_players - Player.objects.count() > 0

    class Meta:
        abstract = True


class Chess(Game):
    max_players = models.IntegerField(verbose_name='max_players', default=2)
    game_name = models.CharField(verbose_name='game_name', db_index=True, max_length=32, default='Chess')
    room = models.OneToOneField('Room', on_delete=models.CASCADE, related_name='chess_game')


class Catan(Game):
    max_players = models.IntegerField(verbose_name='max_players', default=4)
    game_name = models.CharField(verbose_name='game_name', db_index=True, max_length=32, default='Catan')
    room = models.OneToOneField('Room', on_delete=models.CASCADE, related_name='catan_game')


class Room(models.Model):
    name = models.CharField(verbose_name='name', db_index=True, max_length=32)
