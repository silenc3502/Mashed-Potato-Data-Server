from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.controller.board_controller import BoardController

router = DefaultRouter()
router.register(r"board", BoardController, basename='board')

urlpatterns = [
    path('', include(router.urls)),
    path('list',
         BoardController.as_view({ 'get': 'requestBoardList' }),
         name='게시판 항목 요청'),
    path('create',
         BoardController.as_view({ 'post': 'requestBoardCreate' }),
         name='게시물 등록 요청'),
    path('read/<int:pk>',
         BoardController.as_view({ 'get': 'requestBoardRead' }),
         name='게시물 읽기 요청'),
    path('modify/<int:pk>',
         BoardController.as_view({ 'put': 'requestBoardModify' }),
         name='게시물 수정 요청'),
    path('delete/<int:pk>',
         BoardController.as_view({'delete': 'requestBoardDelete'}), 
         name='게시물 삭제 요청'),
]