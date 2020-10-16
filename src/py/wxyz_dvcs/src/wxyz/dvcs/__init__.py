""" DVCS widgets
"""
from ._version import __version__  # noqa
from .repos.repo_base import Repo
from .tools.tool_commits import Committer
from .tools.tool_heads import HeadPicker, HeadStatus
from .tools.tool_remotes import Remoter
from .tools.tool_timetravel import TimeTraveler
from .trackers.tracker_base import Tracker
from .trackers.tracker_json import JSONDictTracker
from .widget_watch import Watcher

__all__ = [
    "__version__",
    "Committer",
    "HeadPicker",
    "HeadStatus",
    "JSONDictTracker",
    "Remoter",
    "Repo",
    "TimeTraveler",
    "Tracker",
    "Watcher",
]

# conditional imports
try:
    from .trackers.tracker_yaml import YAMLDictTracker

    __all__ += ["YAMLDictTracker"]
except ImportError:
    pass


try:
    from .repos.repo_git import Git

    __all__ += ["Git"]
except ImportError:
    pass
