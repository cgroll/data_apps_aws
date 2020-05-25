from pathlib import Path

class ProjectPaths:

    home_path = Path.home()
    
    # ---- Folders ----
    # Passwords
    secret_path = home_path / '.secrets'
    passwords_path = secret_path / 'passwords'
    passphrase_path = secret_path
    pass_manager_path = home_path / '.password-store'
