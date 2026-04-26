from core.models.entities.user import User
from core.services.base_manager import BaseManager

manager = BaseManager(User)

manager.save({
    "username": "haggag",
    "password": "123456"
})

print("✔ Saved")