import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from board.service.board_service_impl import BoardServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class BoardController(viewsets.ViewSet):
    boardService = BoardServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestBoardList(self, request):
        getRequest = request.GET
        page = int(getRequest.get("page", 1))
        perPage = int(getRequest.get("perPage", 8))
        paginatedBoardList, totalItems, totalPages = self.boardService.requestList(page, perPage)

        # JSON 응답 생성
        return JsonResponse({
            "dataList": paginatedBoardList,  # 게시글 정보 목록
            "totalItems": totalItems,  # 전체 게시글 수
            "totalPages": totalPages  # 전체 페이지 수
        }, status=status.HTTP_200_OK)

    def requestBoardCreate(self, request):
        postRequest = request.data
        print(f"postRequest: {postRequest}")

        title = postRequest.get("title")
        content = postRequest.get("content")
        userToken = postRequest.get("userToken")

        accountId = self.redisCacheService.getValueByKey(userToken)

        savedBoard = self.boardService.requestCreate(title, content, accountId)

        return JsonResponse({"data": savedBoard}, status=status.HTTP_200_OK)

    def requestBoardRead(self, request, pk=None):
        try:
            if not pk:
                return JsonResponse({"error": "ID를 제공해야 합니다."}, status=400)

            print(f"requestGameSoftwareRead() -> pk: {pk}")
            readBoard = self.boardService.requestRead(pk)

            return JsonResponse(readBoard, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def requestBoardModify(self, request, pk=None):
        try:
            postRequest = request.data
            print(f"postRequest: {postRequest}")

            title = postRequest.get("title")
            content = postRequest.get("content")

            # 필수 항목 체크
            if not title or not content:
                return JsonResponse({"error": "Title and content are required."}, status=status.HTTP_400_BAD_REQUEST)

            userToken = postRequest.get("userToken")
            accountId = self.redisCacheService.getValueByKey(userToken)

            # 게시글 수정 요청 처리
            updatedBoard = self.boardService.requestModify(pk, title, content, accountId)

            return JsonResponse(updatedBoard, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestBoardDelete(self, request, pk=None):
        try:
            postRequest = request.data
            print(f"postRequest: {postRequest}")

            userToken = postRequest.get("userToken")
            accountId = self.redisCacheService.getValueByKey(userToken)
            if not accountId:
                return JsonResponse({"error": "유저 토큰이 유효하지 않음"}, status=status.HTTP_400_BAD_REQUEST)

            # 게시글 삭제 처리
            success = self.boardService.requestDelete(pk, accountId)

            if success:
                return JsonResponse({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "게시글 삭제 실패"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
