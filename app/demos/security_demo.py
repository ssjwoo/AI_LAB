from app.core.settings import Settings
from app.security.authz import SecurityManager, User, Resource, AuthorizationError, ResourceNotFoundError


async def demo_security(settings: Settings):
    res = Resource(id=101, owner_id=1, content="secret")
    user_owner = User(id=1, role="user")
    user_other = User(id=2, role="user")
    admin = User(id=999, role="admin")

    print("[SECURITY DEMO] owner access -> should pass")
    SecurityManager.check_access(
        user_owner, res,
        hide_existence_on_unauthorized=settings.HIDE_EXISTENCE_ON_UNAUTHORIZED
    )
    print("  OK")

    print("[SECURITY DEMO] admin access -> should pass")
    SecurityManager.check_access(
        admin, res,
        hide_existence_on_unauthorized=settings.HIDE_EXISTENCE_ON_UNAUTHORIZED
    )
    print("  OK")

    print("[SECURITY DEMO] other user access -> should fail")
    try:
        SecurityManager.check_access(
            user_other, res,
            hide_existence_on_unauthorized=settings.HIDE_EXISTENCE_ON_UNAUTHORIZED
        )
    except (AuthorizationError, ResourceNotFoundError) as e:
        print(f"  BLOCKED: {type(e).__name__}: {e}")

    print("[SECURITY DEMO] missing resource -> 404")
    try:
        SecurityManager.check_access(
            user_owner, None,
            hide_existence_on_unauthorized=settings.HIDE_EXISTENCE_ON_UNAUTHORIZED
        )
    except ResourceNotFoundError as e:
        print(f"  NOT_FOUND: {e}")