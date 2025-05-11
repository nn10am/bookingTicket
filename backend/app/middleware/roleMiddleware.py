from fastapi import Depends
from app.utils.authUtil import get_current_user
from app.models.userModel import User
from app.utils.errorHandleUtil import admin_only_error

def admin_required(user: User=Depends(get_current_user)):
    """Middleware to enfore admin-only API access."""
    if user.is_admin == False:
        admin_only_error()

    return user