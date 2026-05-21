"""Pydantic schemas validated at the data boundary (loan-level grain).

Only the loan tape is schema-validated on load; it is the single source of
truth from which pool KPIs and ECL are derived. The other feeds (DPD
snapshots, monthly loss, vintage) are validated structurally by the loaders.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

DPD_BUCKETS = ["Current", "1-29 DPD", "30-59 DPD", "60-89 DPD", "90+ DPD"]
SMA_CLASSES = ["Standard", "SMA-0", "SMA-1", "SMA-2", "NPA"]


class LoanRecord(BaseModel):
    """One row of the auto-loan tape (``fact_loan`` grain)."""

    LoanID: str
    PoolID: str
    BorrowerID: str
    VehicleKey: int
    GeoKey: int
    ServicerID: str
    OriginationDateKey: int
    OriginalLoanAmount: float = Field(gt=0)
    CurrentBalance: float = Field(ge=0)
    InterestRate: float = Field(ge=0, le=40)
    OriginalTerm: int = Field(gt=0)
    RemainingTerm: int = Field(ge=0)
    MonthsOnBook: int = Field(ge=0)
    LTV_Current: float = Field(ge=0)
    DTI_Ratio: float = Field(ge=0)
    CIBIL_Score_Current: int = Field(ge=300, le=900)
    DelinquencyDays: int = Field(ge=0)
    IFRS9_Stage: int = Field(ge=1, le=3)
    PD_Estimate: float = Field(ge=0, le=1)
    LGD_Estimate: float = Field(ge=0, le=1)
    EAD: float = Field(ge=0)
    ECL_Provision: float = Field(ge=0)
    IsDefaulted: bool
    LossAmount: float = Field(ge=0)
    RecoveryAmount: float = Field(ge=0)
    NetLoss: float = Field(ge=0)
    PrepaymentAmount: float = Field(ge=0)

    @field_validator("CurrentBalance")
    @classmethod
    def _balance_not_above_original(cls, v: float, info):
        orig = info.data.get("OriginalLoanAmount")
        if orig is not None and v > orig * 1.0001:
            raise ValueError("CurrentBalance exceeds OriginalLoanAmount")
        return v
