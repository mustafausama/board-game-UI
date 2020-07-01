from django.db import models
from django.db.models import F


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
            # not implemented
            pass

    class Meta:
        abstract = True


class ChessCell(Cell):
    stackable = models.BooleanField(verbose_name='stackable', db_index=True, default=False)
    grid = models.ForeignKey("ChessGrid", on_delete=models.CASCADE, related_name='cell')


class CatanCell(Cell):
    grid = models.ForeignKey("CatanGrid", on_delete=models.CASCADE, related_name='cell')


class Item(models.Model):
    cell = models.ForeignKey("Cell", on_delete=models.CASCADE, related_name='item')
    type = models.CharField(max_length=64, verbose_name='type', db_index=True)
    image = models.ImageField(upload_to='uploads/')

    def move(self, cell):
        cell.chess_item.add(self)

    def available_cells(self):
        pass

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

    # functional code, but it worked slower
    # queen and rook works without the logic that they can't go through other figures

    # def can_move(self, cell):
    #     if self.type == 'King':
    #         return (cell.chess_item.count() == 0 or
    #                 cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
    #                self.cell != cell and \
    #                abs(cell.x - self.cell.x) < 2 and \
    #                abs(cell.y - self.cell.y) < 2
    #
    #     if self.type == 'Queen':
    #         return (cell.chess_item.count() == 0 or
    #                 cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
    #                self.cell != cell and \
    #                (abs(cell.x - self.cell.x) == abs(cell.y - self.cell.y) or
    #                 abs(cell.x - self.cell.x) == 0 or
    #                 abs(cell.y - self.cell.y) == 0)
    #
    #     if self.type == 'Bishop':
    #         return (cell.chess_item.count() == 0 or
    #                 cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
    #                ChessCell.objects \
    #                    .filter(grid=cell.grid,
    #                            x__range=(cell.x, self.cell.x),
    #                            y__range=(cell.y, self.cell.y),
    #                            x=F('y')) \
    #                    .exclude(id=cell.id) \
    #                    .exclude(id=self.cell_id) \
    #                    .exists() and \
    #                abs(cell.x - self.cell.x) == abs(cell.y - self.cell.y)
    #
    #     if self.type == 'Knight':
    #         return (cell.chess_item.count() == 0 or
    #                 cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
    #                ((abs(cell.x - self.cell.x) == 1 and abs(cell.y - self.cell.y) == 2) or
    #                 (abs(cell.x - self.cell.x) == 2 and abs(cell.y - self.cell.y) == 1)
    #                 )
    #
    #     if self.type == 'Rook':
    #         return (cell.chess_item.count() == 0 or
    #                 cell.chess_item.only('isWhite')[0].isWhite != self.isWhite) and \
    #                self.cell != cell and \
    #                (abs(cell.x - self.cell.x) == 0 or
    #                 abs(cell.y - self.cell.y) == 0)
    #
    #     if self.type == 'Pawn':
    #         right_dir = cell.y - self.cell.y == (1 if self.isWhite else -1)
    #         if cell.chess_item.exists():
    #             return cell.chess_item.only('isWhite')[0].isWhite != self.isWhite and \
    #                    abs(cell.x - self.cell.x) == 1 and \
    #                    right_dir
    #         else:
    #             return cell.x == self.cell.x and right_dir

    def move(self, cell):
        cell.chess_item.delete()
        cell.chess_item = self
        cell.save()

    def available_cells(self):
        cells = ChessCell.objects.filter(grid=self.cell.grid)
        available = []
        x = self.cell.x
        y = self.cell.y

        if self.type == 'King':

            if y > 1:
                temp = cells.get(x=x, y=y - 1).chess_item
                if not temp.exists() or (temp.get().isWhite != self.isWhite):
                    available.append({'x': x, 'y': y - 1})

            if y < 8:
                temp = cells.get(x=x, y=y + 1).chess_item
                if not temp.exists() or (temp.get().isWhite != self.isWhite):
                    available.append({'x': x, 'y': y + 1})

            if x > 1:
                temp = cells.get(x=x - 1, y=y).chess_item
                if not temp.exists() or (temp.get().isWhite != self.isWhite):
                    available.append({'x': x - 1, 'y': y})

                if y < 8:
                    temp = cells.get(x=x - 1, y=y + 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x - 1, 'y': y + 1})

                if y > 1:
                    temp = cells.get(x=x - 1, y=y - 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x - 1, 'y': y - 1})

            if x < 8:
                temp = cells.get(x=x + 1, y=y).chess_item
                if not temp.exists() or (temp.get().isWhite != self.isWhite):
                    available.append({'x': x + 1, 'y': y})

                if y < 8:
                    temp = cells.get(x=x + 1, y=y + 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x + 1, 'y': y + 1})

                if y > 1:
                    temp = cells.get(x=x + 1, y=y - 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x + 1, 'y': y - 1})

        elif self.type == 'Knight':

            if x < 8:
                if y < 7:
                    temp = cells.get(x=x + 1, y=y + 2).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x + 1, 'y': y + 2})

                if y > 2:
                    temp = cells.get(x=x + 1, y=y - 2).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x + 1, 'y': y - 2})

            if x < 7:
                if y < 8:
                    temp = cells.get(x=x + 2, y=y + 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x + 2, 'y': y + 1})

                if y > 1:
                    temp = cells.get(x=x + 2, y=y - 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x + 2, 'y': y - 1})

            if x > 1:
                if y < 7:
                    temp = cells.get(x=x - 1, y=y + 2).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x - 1, 'y': y + 2})

                if y > 2:
                    temp = cells.get(x=x - 1, y=y - 2).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x - 1, 'y': y - 2})

            if x > 2:
                if y < 8:
                    temp = cells.get(x=x - 2, y=y + 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x - 2, 'y': y + 1})

                if y > 1:
                    temp = cells.get(x=x - 2, y=y - 1).chess_item
                    if not temp.exists() or (temp.get().isWhite != self.isWhite):
                        available.append({'x': x - 2, 'y': y - 1})

        elif self.type == 'Pawn':

            if self.isWhite:
                if not cells.get(x=x, y=y + 1).chess_item.exists():
                    available.append({'x': x, 'y': y + 1})

                if x > 1:
                    temp = cells.get(x=x - 1, y=y + 1).chess_item
                    if temp.exists() and not temp.get().isWhite:
                        available.append({'x': x - 1, 'y': y + 1})

                if x < 8:
                    temp = cells.get(x=x + 1, y=y + 1).chess_item
                    if temp.exists() and not temp.get().isWhite:
                        available.append({'x': x + 1, 'y': y + 1})

                if y == 2:
                    if not cells.get(x=x, y=y + 2).chess_item.exists() and \
                            not cells.get(x=x, y=y + 1).chess_item.exists():
                        available.append({'x': x, 'y': y + 2})
            else:
                if not cells.get(x=x, y=y - 1).chess_item.exists():
                    available.append({'x': x, 'y': y - 1})

                if x > 1:
                    temp = cells.get(x=x - 1, y=y - 1).chess_item
                    if temp.exists() and temp.get().isWhite:
                        available.append({'x': x - 1, 'y': y - 1})

                if x < 8:
                    temp = cells.get(x=x + 1, y=y - 1).chess_item
                    if temp.exists() and temp.get().isWhite:
                        available.append({'x': x + 1, 'y': y - 1})

                if y == 7:
                    if not cells.get(x=x, y=y - 2).chess_item.exists() and \
                            not cells.get(x=x, y=y - 1).chess_item.exists():
                        available.append({'x': x, 'y': y - 2})

        elif self.type == 'Rook' or self.type == 'Queen':

            for i in range(x - 1, 0, -1):
                temp = cells.get(x=i, y=y).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': i, 'y': y})
                    break
                available.append({'x': i, 'y': y})

            for i in range(x + 1, 9):
                temp = cells.get(x=i, y=y).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': i, 'y': y})
                    break
                available.append({'x': i, 'y': y})

            for i in range(y - 1, 0, -1):
                temp = cells.get(x=x, y=i).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': x, 'y': i})
                    break
                available.append({'x': x, 'y': i})

            for i in range(y + 1, 9):
                temp = cells.get(x=x, y=i).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': x, 'y': i})
                    break
                available.append({'x': x, 'y': i})

        if self.type == 'Bishop' or self.type == 'Queen':

            for i in range(1, (min(x, y))):
                temp = cells.get(x=x - i, y=y - i).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': x - i, 'y': y - i})
                    break
                available.append({'x': x - i, 'y': y - i})

            for i in range(1, (min(9 - x, y))):
                temp = cells.get(x=x + i, y=y - i).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': x + i, 'y': y - i})
                    break
                available.append({'x': x + i, 'y': y - i})

            for i in range(1, (min(x, 9 - y))):
                temp = cells.get(x=x - i, y=y + i).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': x - i, 'y': y + i})
                    break
                available.append({'x': x - i, 'y': y + i})

            for i in range(1, (min(9 - x, 9 - y))):
                temp = cells.get(x=x + i, y=y + i).chess_item
                if temp.exists():
                    if temp.get().isWhite != self.isWhite:
                        available.append({'x': x + i, 'y': y + i})
                    break
                available.append({'x': x + i, 'y': y + i})

        return available

        # shitty code, uses functional style, but it's a lot slower because of many SQL requests
        # return ChessCell.objects.filter(
        #     id__in=[x.id for x in ChessCell.objects.all().filter(grid=self.cell.grid) if self.can_move(x)])

    def can_transform(self):
        return self.type == 'Pawn' and (
                (self.cell.x == 8 and self.cell.y == 8 and self.isWhite) or
                (self.cell.x == 1 and self.cell.y == 1 and not self.isWhite)
        )

    def transform(self):
        self.type = 'Queen'
        self.image = 'uploads/chess/Queen_White.png' if self.isWhite else 'uploads/chess/Queen_Black.png'
        self.save()


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
