from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class BaseResult:
    request_id: Optional[str] = None

@dataclass
class EditSyncResult(BaseResult):
    url: Optional[str] = None

@dataclass
class EditAsyncResult(BaseResult):
    url: Optional[str] = None

@dataclass
class StatusResult(BaseResult):
    status: Optional[str] = None

@dataclass
class StatusSuccessResult(StatusResult):
    url: Optional[str] = None
    seed: Optional[int] = None
    prompt: Optional[str] = None
    refined_prompt: Optional[str] = None


@dataclass
class StatusErrorResult(StatusResult):
    error: Optional[Dict[str, Any]] = None