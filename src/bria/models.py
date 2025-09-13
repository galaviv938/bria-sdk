from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class BaseResult:
    raw_json: Dict[str, Any]

@dataclass
class RemoveBackgroundResult(BaseResult):
    url: Optional[str]
    request_id: Optional[str]

@dataclass
class StatusResult(BaseResult):
    status: Optional[str]
    request_id: Optional[str]

@dataclass
class StatusSuccessResult(StatusResult):
    url: Optional[str] = None
    seed: Optional[int] = None
    prompt: Optional[str] = None
    refined_prompt: Optional[str] = None


@dataclass
class StatusErrorResult(StatusResult):
    error: Optional[Dict[str, Any]] = None