from django.db import IntegrityError

from board.entity.board import Board
from board.repository.board_repository import BoardRepository


class BoardRepositoryImpl(BoardRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self, page, perPage):
        offset = (page - 1) * perPage
        boards = Board.objects.all().order_by('-create_date')[offset:offset + perPage]
        totalItems = Board.objects.count()

        return boards, totalItems

    def save(self, board):
        try:
            # Board 객체를 데이터베이스에 저장
            board.save()  # 새 객체를 저장하거나 기존 객체를 업데이트
            return board  # 저장된 Board 객체를 반환
        except IntegrityError as e:
            # 저장 중에 발생한 예외 처리
            print(f"Error saving board: {e}")
            raise Exception("Board 저장 중 오류가 발생했습니다.")

    def findById(self, boardId):
        try:
            return Board.objects.get(id=boardId)
        except Board.DoesNotExist:
            return None

    def deleteById(self, boardId):
        try:
            # 게시글을 ID로 조회
            board = Board.objects.get(id=boardId)
            board.delete()  # 게시글 삭제
            return True  # 삭제 성공
        except Board.DoesNotExist:
            # 게시글이 존재하지 않으면 None을 반환
            print(f"게시글 ID {boardId}가 존재하지 않습니다.")
            return False  # 삭제 실패
        except IntegrityError as e:
            # 삭제 중에 발생한 예외 처리
            print(f"Error deleting board: {e}")
            return False  # 삭제 실패
