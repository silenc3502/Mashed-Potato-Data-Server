from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from board.entity.board import Board
from board.repository.board_repository_impl import BoardRepositoryImpl
from board.service.board_service import BoardService


class BoardServiceImpl(BoardService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__boardRepository = BoardRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__accountProfileRepository = AccountProfileRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestList(self, page, perPage):
        paginatedBoardList, totalItems = self.__boardRepository.list(page, perPage)

        totalPages = (totalItems + perPage - 1) // perPage

        paginatedFilteringBoardList = [
            {
                "boardId": board.id,
                "title": board.title,
                "nickname": board.writer.nickname,  # writer 객체의 nickname 가져오기
                "createDate": board.create_date.strftime("%Y-%m-%d %H:%M"),
            }
            for board in paginatedBoardList
        ]

        return paginatedFilteringBoardList, totalItems, totalPages

    def requestCreate(self, title, content, accountId):
        if not title or not content:
            raise ValueError("Title and content are required fields.")
        if not accountId:
            raise ValueError("Account ID is required.")

            # 2. Account 조회
        account = self.__accountRepository.findById(accountId)
        if not account:
            raise ValueError(f"Account with ID {accountId} does not exist.")

        # 3. AccountProfile 조회
        accountProfile = self.__accountProfileRepository.findByAccount(account)
        if not accountProfile:
            raise ValueError(f"AccountProfile for account ID {accountId} does not exist.")

        # 4. Board 객체 생성 및 저장
        board = Board(
            title=title,
            content=content,
            writer=accountProfile)  # ForeignKey로 연결된 account_profile)
        savedBoard = self.__boardRepository.save(board)

        # 5. 응답 데이터 구조화
        return {
            "boardId": savedBoard.id,
            "title": savedBoard.title,
            "writerNickname": savedBoard.writer.nickname,
            "createDate": savedBoard.create_date.strftime("%Y-%m-%d %H:%M"),
        }

    def requestRead(self, boardId):
        board = self.__boardRepository.findById(boardId)
        if board:
            return {
                "boardId": board.id,
                "title": board.title,
                "content": board.content,
                "createDate": board.create_date.strftime("%Y-%m-%d %H:%M"),
                "nickname": board.writer.nickname
            }
        return None

    def requestModify(self, boardId, title, content, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            accountProfile = self.__accountProfileRepository.findByAccount(account)
            # 게시글 조회
            board = self.__boardRepository.findById(boardId)

            # 게시글 작성자와 요청한 사용자가 동일한지 확인
            if board.writer.id != accountProfile.id:
                raise ValueError("You are not authorized to modify this board.")

            # 제목과 내용 업데이트
            board.title = title
            board.content = content

            # 게시글 저장 (수정)
            updatedBoard = self.__boardRepository.save(board)

            # 수정된 게시글 반환
            return {
                "boardId": updatedBoard.id,
                "title": updatedBoard.title,
                "content": updatedBoard.content,
                "writerNickname": updatedBoard.writer.nickname,  # 작성자의 닉네임
                "createDate": updatedBoard.create_date.strftime("%Y-%m-%d %H:%M"),
            }

        except Board.DoesNotExist:
            raise ValueError(f"Board with ID {boardId} does not exist.")
        except Exception as e:
            raise Exception(f"Error while modifying the board: {str(e)}")

    def requestDelete(self, boardId, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            accountProfile = self.__accountProfileRepository.findByAccount(account)

            board = self.__boardRepository.findById(boardId)
            if not board:
                raise ValueError(f"Board with ID {boardId} does not exist.")

            if board.writer.id != accountProfile.id:
                raise ValueError("You are not authorized to modify this board.")

            # 게시글 삭제 요청
            success = self.__boardRepository.deleteById(boardId)
            return success
        except Exception as e:
            raise Exception(f"게시글 삭제 중 오류 발생: {str(e)}")
