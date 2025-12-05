# Mount /a2a will be implemented here.

def mount_a2a(app):
    try:
        from agent.a2a_adapter import a2a_app
        app.mount("/a2a", a2a_app)
        return True
    except Exception:
        return False
