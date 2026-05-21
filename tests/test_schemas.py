"""Schema validation at the data boundary."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrisk.data import loaders
from matrisk.data.schemas import LoanRecord


def test_all_loans_validate(loans):
    assert loaders.validate_loans(loans) == len(loans)


def test_rejects_balance_above_original():
    base = dict(
        LoanID="L1", PoolID="P", BorrowerID="B1", VehicleKey=0, GeoKey=0,
        ServicerID="S", OriginationDateKey=20230101, OriginalLoanAmount=100.0,
        CurrentBalance=200.0, InterestRate=11.0, OriginalTerm=60, RemainingTerm=40,
        MonthsOnBook=20, LTV_Current=70.0, DTI_Ratio=30.0, CIBIL_Score_Current=740,
        DelinquencyDays=0, IFRS9_Stage=1, PD_Estimate=0.01, LGD_Estimate=0.35,
        EAD=200.0, ECL_Provision=0.7, IsDefaulted=False, LossAmount=0.0,
        RecoveryAmount=0.0, NetLoss=0.0, PrepaymentAmount=0.0,
    )
    with pytest.raises(ValidationError):
        LoanRecord.model_validate(base)


def test_rejects_pd_out_of_range():
    with pytest.raises(ValidationError):
        LoanRecord.model_validate(dict(
            LoanID="L1", PoolID="P", BorrowerID="B1", VehicleKey=0, GeoKey=0,
            ServicerID="S", OriginationDateKey=20230101, OriginalLoanAmount=100.0,
            CurrentBalance=50.0, InterestRate=11.0, OriginalTerm=60, RemainingTerm=40,
            MonthsOnBook=20, LTV_Current=70.0, DTI_Ratio=30.0, CIBIL_Score_Current=740,
            DelinquencyDays=0, IFRS9_Stage=1, PD_Estimate=1.5, LGD_Estimate=0.35,
            EAD=50.0, ECL_Provision=0.7, IsDefaulted=False, LossAmount=0.0,
            RecoveryAmount=0.0, NetLoss=0.0, PrepaymentAmount=0.0,
        ))
