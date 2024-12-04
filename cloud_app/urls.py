from django.urls import path
from .user_account import (
    delete_user,
    update_user,
    log_out,
    upload_file,
    get_all_files,
    get_file_by_id,
    get_file_by_link,
    get_file_link,
    delete_file,
    update_file,
    )
from .admin_account import (
    admin_delete_user,
    admin_create_user,
    admin_upload_file,
    admin_get_file_by_id,
    admin_get_all_user_files,
    admin_get_file_link,
    admin_delete_file,
    admin_update_file,
    admin_get_all_users,
    admin_change_permissions
    )

urlpatterns = [
    path("delete_user/<int:user_id>",delete_user),
    path("update_user/<int:user_id>",update_user),
    path("log_out/<int:user_id>",log_out),
    path("upload_file/<int:user_id>",upload_file),
    path('get_all/<int:user_id>',get_all_files),
    path("get_file/<int:user_id>/<int:file_id>",get_file_by_id),
    path("get_by_link/<str:link>",get_file_by_link),
    path("get_link/<int:user_id>/<int:file_id>",get_file_link),
    path("delete_file/<int:user_id>/<int:file_id>",delete_file),
    path("update_file/<int:user_id>/<int:file_id>",update_file),
    
    path("admin/change_permissions/<int:user_id>",admin_change_permissions),
    path("admin/create_user",admin_create_user),
    path("admin/delete_user/<int:user_id>",admin_delete_user),
    path("admin/get_all_users",admin_get_all_users),
    path("admin/upload_file/<int:user_id>",admin_upload_file),
    path('admin/get_all_user_files/<int:user_id>',admin_get_all_user_files),
    path("admin/get_file/<int:user_id>/<int:file_id>",admin_get_file_by_id),
    path("admin/get_link/<int:user_id>/<int:file_id>",admin_get_file_link),
    path("admin/delete_file/<int:user_id>/<int:file_id>",admin_delete_file),
    path("admin/update_file/<int:user_id>/<int:file_id>",admin_update_file),
]
