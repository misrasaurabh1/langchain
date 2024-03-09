import platform

from langchain import __version__ as lang_ver
import platform
from functools import lru_cache


@lru_cache(maxsize=1)
def get_runtime_environment() -> dict:
    """Get information about the LangChain runtime environment."""

    return {
        "library_version": lang_ver,
        "library": "langchain",
        "platform": platform.platform(),
        "runtime": "python",
        "runtime_version": platform.python_version(),
    }
