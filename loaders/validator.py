from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class Machine(BaseModel):
    id: str
    # allow None so raw missing values don't break; if provided, must be > 0
    time: Optional[float] = Field(default=None, gt=0, description="Processing time (must be positive if provided)")

class Operation(BaseModel):
    operation_id: str
    machines: List[Machine]

class Job(BaseModel):
    job_id: str
    operations: List[Operation]

class Metadata(BaseModel):
    source: str
    objective: str
    created_by: str

class CaseStudy(BaseModel):
    case_id: str
    jobs: List[Job]
    metadata: Metadata

    @field_validator("jobs")
    @classmethod
    def jobs_not_empty(cls, v):
        if not v:
            raise ValueError("Jobs list cannot be empty")
        return v

def validate_case(data: dict) -> CaseStudy:
    """Validate and return a CaseStudy object."""
    return CaseStudy(**data)
