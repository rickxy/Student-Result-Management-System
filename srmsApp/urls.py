from django.contrib import admin
from django.urls import path
from srmsApp import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static
context={
    'page':'login',
    'page_title':'Login',
    'system_name': views.context['system_name'],
    'short_name':views.context['short_name'],
    'has_navigation':False,
    'has_sidebar':False,
}
urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True,extra_context = context),name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('userlogin', views.login_user, name="login-user"),
    path('profile', views.profile, name="profile-page"),
    path('update_profile', views.update_profile, name="update-profile"),
    path('update_password', views.update_password, name="update-password"),
    path('', views.home,name="home-page"),
    path('class_mgt', views.class_mgt,name="class-page"),
    path('manage_class', views.manage_class,name="manage-class"),
    path('manage_class/<int:pk>', views.manage_class,name="manage-class-pk"),
    path('save_class', views.save_class,name="save-class"),
    path('delete_class', views.delete_class,name="delete-class"),
    path('subject_mgt', views.subject_mgt,name="subject-page"),
    path('manage_subject', views.manage_subject,name="manage-subject"),
    path('manage_subject/<int:pk>', views.manage_subject,name="manage-subject-pk"),
    path('view_subject/<int:pk>', views.view_subject,name="view-subject-pk"),
    path('save_subject', views.save_subject,name="save-subject"),
    path('delete_subject', views.delete_subject,name="delete-subject"),
    path('student', views.student_mgt,name="student-page"),
    path('manage_student', views.manage_student,name="manage-student"),
    path('manage_student/<int:pk>', views.manage_student,name="manage-student-pk"),
    path('view_student/<int:pk>', views.view_student,name="view-student-pk"),
    path('save_student', views.save_student,name="save-student"),
    path('delete_student', views.delete_student,name="delete-student"),
    path('result', views.result_mgt,name="result-page"),
    path('manage_result', views.manage_result,name="manage-result"),
    path('manage_result/<int:pk>', views.manage_result,name="manage-result-pk"),
    path('view_result/<int:pk>', views.view_result,name="view-result-pk"),
    path('save_result', views.save_result,name="save-result"),
    path('delete_result', views.delete_result,name="delete-result"),
    path('select_student', views.select_student,name="select-student"),
    path('list_result', views.list_student_result,name="list-result"),
    path('list_result/<int:pk>', views.list_student_result),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)