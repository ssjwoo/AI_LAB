import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("app.security")


class AuthorizationError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


@dataclass
class User:
    id: int
    role: str  # "admin" | "analyst" | "user"


@dataclass
class Resource:
    id: int
    owner_id: int
    content: str


class SecurityManager:
    @staticmethod
    def check_access(
        user: User,
        resource: Optional[Resource],
        *,
        hide_existence_on_unauthorized: bool = False,
    ) -> bool:
        if resource is None:
            raise ResourceNotFoundError("존재하지 않는 리소스입니다.")

        if user.role == "admin":
            return True

        if resource.owner_id != user.id:
            logger.warning("unauthorized_access user_id=%s resource_id=%s", user.id, resource.id)
            if hide_existence_on_unauthorized:
                raise ResourceNotFoundError("존재하지 않는 리소스입니다.")
            raise AuthorizationError("해당 리소스에 대한 권한이 없습니다.")

        return True
