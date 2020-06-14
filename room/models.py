from django.db import models


class Grid(models.Model):
    class Meta:
        abstract = True


class ChessGrid(Grid):
    pass


class CatanGrid(Grid):
    pass


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

    class Meta:
        abstract = True


class ChessItem(Item):
    cell = models.ForeignKey("ChessCell", on_delete=models.CASCADE, related_name='figure')
    isWhite = models.BooleanField(verbose_name='isWhite', db_index=True)

    def can_move(self, cell):
        pass

    def move(self, cell):
        cell.item.delete()
        cell.item = self
        cell.save()

    # class Meta:
    #     abstract = True


class King(ChessItem):  # король in russian
    def can_move(self, cell):
        return self.cell != cell and \
               abs(cell.x - self.cell.x) < 2 and \
               abs(cell.y - self.cell.y) < 2 and \
               (cell.item.objects.count == 0 or
                cell.item.isWhite != self.isWhite)


class Queen(ChessItem):  # ферзь in russian
    def can_move(self, cell):
        return self.cell != cell and \
               (abs(cell.x - self.cell.x) == abs(cell.y - self.cell.y) or
                abs(cell.x - self.cell.x) == 0 or
                abs(cell.y - self.cell.y) == 0)


class Bishop(ChessItem):  # elephant in russian version
    def can_move(self, cell):
        return self.cell != cell and \
               abs(cell.x - self.cell.x) == abs(cell.y - self.cell.y)


class Knight(ChessItem):  # horse in russian version
    def can_move(self, cell):
        return self.cell != cell


class Rook(ChessItem):  # ладья in russian
    def can_move(self, cell):
        return self.cell != cell and \
               (abs(cell.x - self.cell.x) == 0 or
                abs(cell.y - self.cell.y) == 0)


class Pawn(ChessItem):  # пешка in russian
    def can_move(self, cell):
        # TODO: Check in GUI if we should swap 1 and -1
        return self.cell != cell and \
               cell.y - self.cell.y == 1 if self.isWhite else -1 and \
               (cell.x == self.cell.x or
                (cell.item.isWhite != self.isWhite and abs(cell.x - self.cell.x) == 1)
                )

    # def can_transform(self):
    #     pass
    #
    # def transform(self):
    #     pass


class CatanItem(Item):
    cell = models.ForeignKey("CatanCell", on_delete=models.CASCADE, related_name='item')

    # class Meta:
    #     abstract = True


class Game(models.Model):
    max_players = models.IntegerField(verbose_name='max_players')
    game_name = models.CharField(verbose_name='game_name', db_index=True, max_length=32)

    def have_places(self):
        return self.max_players - Player.objects.count() > 0

    class Meta:
        abstract = True


class Chess(Game):
    max_players = models.IntegerField(verbose_name='max_players', default=2)


class Catan(Game):
    max_players = models.IntegerField(verbose_name='max_players', default=4)


class Player(models.Model):
    nickname = models.CharField(verbose_name='nickname', db_index=True, max_length=32)
    is_host = models.BooleanField(verbose_name='is_host', db_index=True, default=False)

    # TODO: change to the true by default when will be supported
    is_spectator = models.BooleanField(verbose_name='is_spectator', db_index=True, default=False)
