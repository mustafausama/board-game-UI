from django.core.management.base import BaseCommand
from room.models import Room, Player, Chess, ChessGrid, ChessCell, ChessItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        room = Room.objects.create(name='TestRoom')
        game = Chess.objects.create(room=room)
        grid = ChessGrid.objects.create(game=game)

        xy = {1, 2, 3, 4, 5, 6, 7, 8}
        cells = [ChessCell(x=i, y=k, grid=grid) for k in xy for i in xy]
        ChessCell.objects.bulk_create(cells)
        cells = ChessCell.objects.filter(grid=grid)

        white_pawns = [ChessItem(type='Pawn', cell=cells[i + 7], isWhite=True, image='uploads/chess/Pawn_White.png') for
                       i in xy]
        black_pawns = [ChessItem(type='Pawn', cell=cells[i + 47], isWhite=False, image='uploads/chess/Pawn_Black.png')
                       for i in xy]

        figures = [
            ChessItem(type='Queen', cell=cells[3], isWhite=True, image='uploads/chess/Queen_White.png'),
            ChessItem(type='Queen', cell=cells[63 - 4], isWhite=False, image='uploads/chess/Queen_Black.png'),
            ChessItem(type='King', cell=cells[4], isWhite=True, image='uploads/chess/King_White.png'),
            ChessItem(type='King', cell=cells[63 - 3], isWhite=False, image='uploads/chess/King_Black.png'),
            ChessItem(type='Bishop', cell=cells[2], isWhite=True, image='uploads/chess/Bishop_White.png'),
            ChessItem(type='Bishop', cell=cells[5], isWhite=True, image='uploads/chess/Bishop_White.png'),
            ChessItem(type='Bishop', cell=cells[63 - 2], isWhite=False, image='uploads/chess/Bishop_Black.png'),
            ChessItem(type='Bishop', cell=cells[63 - 5], isWhite=False, image='uploads/chess/Bishop_Black.png'),
            ChessItem(type='Knight', cell=cells[1], isWhite=True, image='uploads/chess/Knight_White.png'),
            ChessItem(type='Knight', cell=cells[6], isWhite=True, image='uploads/chess/Knight_White.png'),
            ChessItem(type='Knight', cell=cells[63 - 1], isWhite=False, image='uploads/chess/Knight_Black.png'),
            ChessItem(type='Knight', cell=cells[63 - 6], isWhite=False, image='uploads/chess/Knight_Black.png'),
            ChessItem(type='Rook', cell=cells[0], isWhite=True, image='uploads/chess/Rook_White.png'),
            ChessItem(type='Rook', cell=cells[7], isWhite=True, image='uploads/chess/Rook_White.png'),
            ChessItem(type='Rook', cell=cells[63], isWhite=False, image='uploads/chess/Rook_Black.png'),
            ChessItem(type='Rook', cell=cells[63 - 7], isWhite=False, image='uploads/chess/Rook_Black.png'),
        ]

        figures += white_pawns + black_pawns

        ChessItem.objects.bulk_create(figures)
        self.stdout.write(self.style.SUCCESS('Successfully initiated chess game with id "%s"' % game.id))
