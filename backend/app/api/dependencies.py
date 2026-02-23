from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings

# Type alias for injecting settings into route handlers
SettingsDependency = Annotated[Settings, Depends(get_settings)]
