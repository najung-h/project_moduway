# backend/apps/mypage/urls.py

from django.urls import path
from . import views

app_name = 'mypage'


# 아키텍쳐 구조
"""
/api/v1/mypage/
├── dashboard/
│   └── stats/                          # GET: 학습 현황 요약
├── courses/
│   ├── recent/                         # GET: 최근 학습 강좌
│   ├── /                               # GET: 수강 강좌 목록 (?status=enrolled|completed)
│   └── {course_id}/
│       ├── status/                     # GET: 강좌 수강 상세 정보
│       └── rating/                     # POST: 수강평 등록/수정
│                                       # DELETE: 수강평 삭제
├── wishlist/
│   ├── /                               # GET: 관심 강좌 목록
│   └── {course_id}/                    # POST: 관심 강좌 추가
│                                       # DELETE: 관심 강좌 삭제
├── community/
│   ├── stats/                          # GET: 커뮤니티 활동 통계
│   ├── posts/                          # GET: 내가 쓴 글 목록
│   └── comments/                       # GET: 내가 쓴 댓글 목록
├── scraps/                             # GET: 스크랩한 게시글 목록
└── profile/
    ├── /                               # GET: 내 정보 조회
    │                                   # PUT: 내 정보 수정
    └── password/change/                # POST: 비밀번호 변경 (이미 구현됨)
"""

urlpatterns = [
    # ==================================================
    # Dashboard (대시보드)
    # ==================================================

    # [GET]
    # /mypage/dashboard/stats/
    # - 기능: 학습 현황 요약 통계
    path(
        'dashboard/stats/',
        views.DashboardStatsView.as_view(),
        name='dashboard-stats'
    ),

    # ==================================================
    # Courses (강좌 관리)
    # ==================================================

    # [GET]
    # /mypage/courses/recent/
    # - 기능: 최근 학습 강좌 (이어듣기)
    path(
        'courses/recent/',
        views.RecentCourseView.as_view(),
        name='course-recent'
    ),

    # [GET]
    # /mypage/courses/?status=enrolled|completed
    # - 기능: 수강 강좌 목록
    path(
        'courses/',
        views.EnrollmentListView.as_view(),
        name='enrollment-list'
    ),

    # [GET]
    # /mypage/courses/{course_id}/status/
    # - 기능: 강좌 수강 상세 정보
    path(
        'courses/<int:course_id>/status/',
        views.EnrollmentStatusView.as_view(),
        name='enrollment-status'
    ),

    # [POST, DELETE]
    # /mypage/courses/{course_id}/rating/
    # - POST: 수강평 등록/수정
    # - DELETE: 수강평 삭제
    path(
        'courses/<int:course_id>/rating/',
        views.CourseReviewView.as_view(),
        name='course-review'
    ),

    # ==================================================
    # Wishlist (관심 강좌)
    # ==================================================

    # [GET]
    # /mypage/wishlist/
    # - 기능: 찜한 강좌 목록
    path(
        'wishlist/',
        views.WishlistListView.as_view(),
        name='wishlist-list'
    ),

    # [POST, DELETE]
    # /mypage/wishlist/{course_id}/
    # - POST: 위시리스트 추가
    # - DELETE: 위시리스트 삭제
    path(
        'wishlist/<int:course_id>/',
        views.WishlistToggleView.as_view(),
        name='wishlist-toggle'
    ),

    # ==================================================
    # Community (커뮤니티 활동)
    # ==================================================

    # [GET]
    # /mypage/community/stats/
    # - 기능: 커뮤니티 활동 통계
    path(
        'community/stats/',
        views.CommunityStatsView.as_view(),
        name='community-stats'
    ),

    # [GET]
    # /mypage/community/posts/
    # - 기능: 내가 쓴 글 목록
    path(
        'community/posts/',
        views.MyPostListView.as_view(),
        name='my-posts'
    ),

    # [GET]
    # /mypage/community/comments/
    # - 기능: 내가 쓴 댓글 목록
    path(
        'community/comments/',
        views.MyCommentListView.as_view(),
        name='my-comments'
    ),

    # ==================================================
    # Scraps (스크랩)
    # ==================================================

    # [GET]
    # /mypage/scraps/
    # - 기능: 스크랩한 게시글 목록
    path(
        'scraps/',
        views.MyScrapListView.as_view(),
        name='my-scraps'
    ),

    # ==================================================
    # Profile (내 계정)
    # ==================================================

    # [GET, PUT]
    # /mypage/profile/
    # - GET: 내 정보 조회
    # - PUT: 내 정보 수정
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile'
    ),

    # 비밀번호 변경은 accounts.urls에 이미 구현됨
    # /api/v1/accounts/mypage/profile/password/change/
]