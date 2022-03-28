import typing

if typing.TYPE_CHECKING:
  from Classes.Schwi import Schwi


class PermissionLevel:
  BLOCKED = "0"
  USER = "1"
  ADMIN = "2"


class PermissionsManager:
  def __init__(self, schwi: "Schwi"):
    self.schwi = schwi

  def get_permissions(self, user_id: int | str):
    user_id = str(user_id)
    permissions = self.schwi.redis.get(f"schwi:permissions:{user_id}")
    if permissions is None:
      self.set_permissions(user_id, PermissionLevel.USER)
      return PermissionLevel.USER
    else:
      return permissions.decode("utf-8")

  def set_permissions(self, user_id: int | str, level: str):
    user_id = str(user_id)
    self.schwi.redis.set(f"schwi:permissions:{user_id}", level)
