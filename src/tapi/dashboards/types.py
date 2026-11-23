from typing import Literal

DashboardOrder = Literal[
    "NAME", "RECENTLY_EDITED", "LEAST_RECENTLY_EDITED", "CREATED_DESC", "CREATED_ASC"
]

ImportMode = Literal["new", "replace"]
