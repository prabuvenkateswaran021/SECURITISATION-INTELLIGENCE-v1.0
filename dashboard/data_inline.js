window.DATA = {
  "meta": {
    "pool_id": "ZAAUTO2024-1",
    "pool_name": "Zenith Auto Receivables Trust 2024 Series 1",
    "cutoff_date": "2024-10-30",
    "currency": "INR",
    "generated_at": "2026-05-21T15:29:42.310681+00:00",
    "engine_version": "1.0.0"
  },
  "kpis": {
    "loan_count": 500,
    "borrower_count": 500,
    "original_balance": 545999999.9,
    "current_balance": 317771999.99,
    "pool_factor": 0.5820000000882785,
    "avg_loan_size": 635543.99998,
    "total_ead": 317771999.99,
    "defaulted_count": 27,
    "default_rate_pct": 0.054,
    "total_gross_loss": 6931796.74,
    "total_net_loss": 6931796.74,
    "total_recovery": 8201523.68,
    "total_prepayment": 11332753.51,
    "gross_loss_rate_pct": 0.012695598427233628,
    "recovery_rate_pct": 1.1831742890949222,
    "wac_pct": 11.12416908253226,
    "wam_months": 40.04826594492429,
    "wala_months": 19.980537189021707,
    "weighted_ltv_pct": 70.0236626308046,
    "weighted_dti_pct": 34.174292777196676,
    "weighted_cibil": 745.8566634117184,
    "dpd_30plus_balance": 45374623.300000004,
    "dpd_30plus_pct": 0.14278987230287093,
    "dpd_30plus_count": 71,
    "dpd_60plus_balance": 30406446.32,
    "dpd_60plus_pct": 0.09568636104174333,
    "dpd_60plus_count": 46,
    "dpd_90plus_balance": 19102090.46,
    "dpd_90plus_pct": 0.06011256643316946,
    "dpd_90plus_count": 27,
    "delinquency_rate_pct": 0.142,
    "npa_balance": 19102090.46,
    "npa_pct": 0.06011256643316946,
    "top10_borrower_share_pct": 0.06827475649422461,
    "hhi": 28.73757028632894
  },
  "ecl": {
    "total_ecl": 14148503.476566795,
    "total_ead": 317771999.99,
    "ecl_coverage_pct": 0.044524072218483805,
    "ecl_12month": 4110876.406304175,
    "ecl_lifetime": 10037627.070262617,
    "weighted_pd_pct": 0.12305801729273652,
    "weighted_lgd_pct": 0.3557289885653404,
    "stages": {
      "stage1": {
        "count": 413,
        "balance": 263086875.83999997,
        "ead": 263086875.83999997,
        "ecl": 4110876.406304175,
        "coverage_pct": 0.01562554723864015
      },
      "stage2": {
        "count": 60,
        "balance": 35583033.69,
        "ead": 35583033.69,
        "ecl": 3105830.6156479376,
        "coverage_pct": 0.08728403099932365
      },
      "stage3": {
        "count": 27,
        "balance": 19102090.46,
        "ead": 19102090.46,
        "ecl": 6931796.454614679,
        "coverage_pct": 0.3628815636241458
      }
    }
  },
  "stress": [
    {
      "scenario_id": "BASE",
      "scenario": "Base",
      "pd_multiplier": 1.0,
      "lgd_multiplier": 1.0,
      "ecl": 14148503.476566795,
      "ecl_cr": 1.4148503476566796,
      "uplift_vs_base": 0.0,
      "coverage_pct": 0.044524072218483805,
      "gdp_shock_bps": 0,
      "repo_shock_bps": 0,
      "unemployment_shock_bps": 0
    },
    {
      "scenario_id": "MILD",
      "scenario": "Mild Recession",
      "pd_multiplier": 1.3,
      "lgd_multiplier": 1.1,
      "ecl": 17944867.141467668,
      "ecl_cr": 1.7944867141467669,
      "uplift_vs_base": 0.2683226301063241,
      "coverage_pct": 0.05647088837919129,
      "gdp_shock_bps": -100,
      "repo_shock_bps": 25,
      "unemployment_shock_bps": 50
    },
    {
      "scenario_id": "MODERATE",
      "scenario": "Moderate Slowdown",
      "pd_multiplier": 1.8,
      "lgd_multiplier": 1.25,
      "ecl": 24902336.367660604,
      "ecl_cr": 2.4902336367660602,
      "uplift_vs_base": 0.7600685760797706,
      "coverage_pct": 0.07836542039085967,
      "gdp_shock_bps": -200,
      "repo_shock_bps": 50,
      "unemployment_shock_bps": 120
    },
    {
      "scenario_id": "SEVERE",
      "scenario": "Severe Recession",
      "pd_multiplier": 2.8,
      "lgd_multiplier": 1.45,
      "ecl": 38235728.45823824,
      "ecl_cr": 3.823572845823824,
      "uplift_vs_base": 1.7024574381004658,
      "coverage_pct": 0.12032441014136387,
      "gdp_shock_bps": -350,
      "repo_shock_bps": 100,
      "unemployment_shock_bps": 250
    },
    {
      "scenario_id": "CRISIS",
      "scenario": "Crisis",
      "pd_multiplier": 4.5,
      "lgd_multiplier": 1.75,
      "ecl": 62624100.55251695,
      "ecl_cr": 6.262410055251695,
      "uplift_vs_base": 3.426199608759824,
      "coverage_pct": 0.19707243103384714,
      "gdp_shock_bps": -500,
      "repo_shock_bps": 200,
      "unemployment_shock_bps": 400
    }
  ],
  "tranche_allocation": [
    {
      "tranche_id": "TR-A",
      "tranche": "Class A (Senior)",
      "rank": 1,
      "thickness": 436800000.0,
      "loss_absorbed": 0.0,
      "loss_absorbed_pct": 0.0,
      "written_down": false
    },
    {
      "tranche_id": "TR-B",
      "tranche": "Class B (Mezzanine)",
      "rank": 2,
      "thickness": 65520000.0,
      "loss_absorbed": 18944100.552516952,
      "loss_absorbed_pct": 0.2891346238174138,
      "written_down": false
    },
    {
      "tranche_id": "TR-C",
      "tranche": "Class C (Equity)",
      "rank": 3,
      "thickness": 43680000.0,
      "loss_absorbed": 43680000.0,
      "loss_absorbed_pct": 1.0,
      "written_down": true
    }
  ],
  "waterfall": [
    {
      "ReportingDate": "2023-11-30",
      "Step": "1. Servicer Fee",
      "Amount": 227500.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "2. Trustee Fee",
      "Amount": 22750.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "3. Senior Interest",
      "Amount": 3003000.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "5. Senior Principal",
      "Amount": 14614405.68
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "EOP Senior Balance",
      "Amount": 422185594.32
    },
    {
      "ReportingDate": "2023-11-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "1. Servicer Fee",
      "Amount": 219923.73
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "2. Trustee Fee",
      "Amount": 21992.37
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "3. Senior Interest",
      "Amount": 2902525.96
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "5. Senior Principal",
      "Amount": 15295905.58
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "EOP Senior Balance",
      "Amount": 406889688.74
    },
    {
      "ReportingDate": "2023-12-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "1. Servicer Fee",
      "Amount": 212195.42
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "2. Trustee Fee",
      "Amount": 21219.54
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "3. Senior Interest",
      "Amount": 2797366.61
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "5. Senior Principal",
      "Amount": 13590695.89
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "EOP Senior Balance",
      "Amount": 393298992.85
    },
    {
      "ReportingDate": "2024-01-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "1. Servicer Fee",
      "Amount": 205163.41
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "2. Trustee Fee",
      "Amount": 20516.34
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "3. Senior Interest",
      "Amount": 2703930.58
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "5. Senior Principal",
      "Amount": 11506780.56
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "EOP Senior Balance",
      "Amount": 381792212.29
    },
    {
      "ReportingDate": "2024-02-29",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "1. Servicer Fee",
      "Amount": 199186.0
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "2. Trustee Fee",
      "Amount": 19918.6
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "3. Senior Interest",
      "Amount": 2624821.46
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "5. Senior Principal",
      "Amount": 11242868.63
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "EOP Senior Balance",
      "Amount": 370549343.66
    },
    {
      "ReportingDate": "2024-03-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "1. Servicer Fee",
      "Amount": 193197.64
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "2. Trustee Fee",
      "Amount": 19319.76
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "3. Senior Interest",
      "Amount": 2547526.74
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "5. Senior Principal",
      "Amount": 14256280.88
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "EOP Senior Balance",
      "Amount": 356293062.78
    },
    {
      "ReportingDate": "2024-04-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "1. Servicer Fee",
      "Amount": 185923.81
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "2. Trustee Fee",
      "Amount": 18592.38
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "3. Senior Interest",
      "Amount": 2449514.81
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "5. Senior Principal",
      "Amount": 12613777.0
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "EOP Senior Balance",
      "Amount": 343679285.78
    },
    {
      "ReportingDate": "2024-05-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "1. Servicer Fee",
      "Amount": 179517.44
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "2. Trustee Fee",
      "Amount": 17951.74
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "3. Senior Interest",
      "Amount": 2362795.09
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "5. Senior Principal",
      "Amount": 9931073.93
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "EOP Senior Balance",
      "Amount": 333748211.84
    },
    {
      "ReportingDate": "2024-06-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "1. Servicer Fee",
      "Amount": 174140.53
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "2. Trustee Fee",
      "Amount": 17414.05
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "3. Senior Interest",
      "Amount": 2294518.96
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "5. Senior Principal",
      "Amount": 11320356.26
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "EOP Senior Balance",
      "Amount": 322427855.58
    },
    {
      "ReportingDate": "2024-07-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "1. Servicer Fee",
      "Amount": 168319.03
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "2. Trustee Fee",
      "Amount": 16831.9
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "3. Senior Interest",
      "Amount": 2216691.51
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "5. Senior Principal",
      "Amount": 11304464.38
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "EOP Senior Balance",
      "Amount": 311123391.2
    },
    {
      "ReportingDate": "2024-08-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "1. Servicer Fee",
      "Amount": 162476.08
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "2. Trustee Fee",
      "Amount": 16247.61
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "3. Senior Interest",
      "Amount": 2138973.31
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "5. Senior Principal",
      "Amount": 9824016.63
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "EOP Senior Balance",
      "Amount": 301299374.57
    },
    {
      "ReportingDate": "2024-09-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "1. Servicer Fee",
      "Amount": 157259.95
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "2. Trustee Fee",
      "Amount": 15726.0
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "3. Senior Interest",
      "Amount": 2071433.2
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "4. Mezz Interest",
      "Amount": 573300.0
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "5. Senior Principal",
      "Amount": 11930008.6
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "6. Mezz Principal",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "7. Reserve Top-Up",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "8. Equity Residual",
      "Amount": 0.0
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "EOP Senior Balance",
      "Amount": 289369365.96
    },
    {
      "ReportingDate": "2024-10-30",
      "Step": "EOP Mezz Balance",
      "Amount": 65520000.0
    }
  ],
  "loss_timeseries": [
    {
      "ReportingDate": "2023-11-30",
      "BOP_Balance": 546000000.0,
      "NetLoss_ThisMonth": 398528.37,
      "MonthlyDefaultRate": 0.002085,
      "CPR_Annualised": 0.140861,
      "CollectionEfficiency": 0.963739
    },
    {
      "ReportingDate": "2023-12-30",
      "BOP_Balance": 527816945.96,
      "NetLoss_ThisMonth": 232645.83,
      "MonthlyDefaultRate": 0.001259,
      "CPR_Annualised": 0.162815,
      "CollectionEfficiency": 0.969231
    },
    {
      "ReportingDate": "2024-01-30",
      "BOP_Balance": 509269002.78,
      "NetLoss_ThisMonth": 302182.45,
      "MonthlyDefaultRate": 0.001695,
      "CPR_Annualised": 0.140585,
      "CollectionEfficiency": 0.964441
    },
    {
      "ReportingDate": "2024-02-29",
      "BOP_Balance": 492392184.54,
      "NetLoss_ThisMonth": 171469.19,
      "MonthlyDefaultRate": 0.000995,
      "CPR_Annualised": 0.10049,
      "CollectionEfficiency": 0.986208
    },
    {
      "ReportingDate": "2024-03-30",
      "BOP_Balance": 478046403.0,
      "NetLoss_ThisMonth": 215100.54,
      "MonthlyDefaultRate": 0.001286,
      "CPR_Annualised": 0.109461,
      "CollectionEfficiency": 0.956931
    },
    {
      "ReportingDate": "2024-04-30",
      "BOP_Balance": 463674346.3,
      "NetLoss_ThisMonth": 348624.8,
      "MonthlyDefaultRate": 0.002148,
      "CPR_Annualised": 0.184951,
      "CollectionEfficiency": 0.95625
    },
    {
      "ReportingDate": "2024-05-30",
      "BOP_Balance": 446217155.21,
      "NetLoss_ThisMonth": 288796.79,
      "MonthlyDefaultRate": 0.001849,
      "CPR_Annualised": 0.153692,
      "CollectionEfficiency": 0.98596
    },
    {
      "ReportingDate": "2024-06-30",
      "BOP_Balance": 430841861.61,
      "NetLoss_ThisMonth": 228401.54,
      "MonthlyDefaultRate": 0.001515,
      "CPR_Annualised": 0.107384,
      "CollectionEfficiency": 0.950073
    },
    {
      "ReportingDate": "2024-07-30",
      "BOP_Balance": 417937272.18,
      "NetLoss_ThisMonth": 157275.91,
      "MonthlyDefaultRate": 0.001075,
      "CPR_Annualised": 0.145872,
      "CollectionEfficiency": 0.970583
    },
    {
      "ReportingDate": "2024-08-30",
      "BOP_Balance": 403965665.31,
      "NetLoss_ThisMonth": 295761.52,
      "MonthlyDefaultRate": 0.002092,
      "CPR_Annualised": 0.155458,
      "CollectionEfficiency": 0.971236
    },
    {
      "ReportingDate": "2024-09-30",
      "BOP_Balance": 389942597.94,
      "NetLoss_ThisMonth": 240941.27,
      "MonthlyDefaultRate": 0.001765,
      "CPR_Annualised": 0.129451,
      "CollectionEfficiency": 0.960059
    },
    {
      "ReportingDate": "2024-10-30",
      "BOP_Balance": 377423886.83,
      "NetLoss_ThisMonth": 198117.2,
      "MonthlyDefaultRate": 0.0015,
      "CPR_Annualised": 0.195,
      "CollectionEfficiency": 0.961863
    }
  ],
  "stratification": {
    "by_cibil_band": [
      {
        "CIBILBand_Curr": "Excellent",
        "balance": 147491526.43,
        "loans": 233,
        "ecl": 3089960.52,
        "balance_pct": 0.4641426130516264
      },
      {
        "CIBILBand_Curr": "Super Prime",
        "balance": 97678199.92,
        "loans": 146,
        "ecl": 3438535.21,
        "balance_pct": 0.30738453961668694
      },
      {
        "CIBILBand_Curr": "Prime",
        "balance": 51949125.23,
        "loans": 89,
        "ecl": 5380839.65,
        "balance_pct": 0.16347924056126653
      },
      {
        "CIBILBand_Curr": "Near Prime",
        "balance": 17901451.24,
        "loans": 28,
        "ecl": 1983561.32,
        "balance_pct": 0.056334262428921804
      },
      {
        "CIBILBand_Curr": "Subprime",
        "balance": 2751697.17,
        "loans": 4,
        "ecl": 255608.38,
        "balance_pct": 0.008659344341498286
      }
    ],
    "by_dpd_bucket": [
      {
        "DPD_Bucket": "Current",
        "balance": 250804342.83,
        "loans": 398,
        "ecl": 4914082.19,
        "balance_pct": 0.7892587856635972
      },
      {
        "DPD_Bucket": "1-29 DPD",
        "balance": 21593033.86,
        "loans": 31,
        "ecl": 276602.64,
        "balance_pct": 0.06795134203353194
      },
      {
        "DPD_Bucket": "90+ DPD",
        "balance": 19102090.46,
        "loans": 27,
        "ecl": 6931796.74,
        "balance_pct": 0.06011256643316946
      },
      {
        "DPD_Bucket": "30-59 DPD",
        "balance": 14968176.98,
        "loans": 25,
        "ecl": 930052.92,
        "balance_pct": 0.047103511261127586
      },
      {
        "DPD_Bucket": "60-89 DPD",
        "balance": 11304355.86,
        "loans": 19,
        "ecl": 1095970.59,
        "balance_pct": 0.03557379460857387
      }
    ],
    "by_geography": [
      {
        "State": "Madhya Pradesh",
        "balance": 35764215.15,
        "loans": 48,
        "ecl": 885594.29,
        "balance_pct": 0.11254677929813033
      },
      {
        "State": "Tamil Nadu",
        "balance": 26916112.07,
        "loans": 33,
        "ecl": 1268318.99,
        "balance_pct": 0.08470259201832456
      },
      {
        "State": "Kerala",
        "balance": 23964334.83,
        "loans": 36,
        "ecl": 1305278.27,
        "balance_pct": 0.07541361363101261
      },
      {
        "State": "Telangana",
        "balance": 23933345.37,
        "loans": 34,
        "ecl": 649960.0599999999,
        "balance_pct": 0.07531609257817921
      },
      {
        "State": "Haryana",
        "balance": 23316577.74,
        "loans": 38,
        "ecl": 1232438.19,
        "balance_pct": 0.07337518013145826
      },
      {
        "State": "Rajasthan",
        "balance": 22437691.18,
        "loans": 41,
        "ecl": 723118.22,
        "balance_pct": 0.07060940290744967
      },
      {
        "State": "Maharashtra",
        "balance": 22255161.28,
        "loans": 36,
        "ecl": 950191.9299999999,
        "balance_pct": 0.07003499767349028
      },
      {
        "State": "Karnataka",
        "balance": 20496006.91,
        "loans": 31,
        "ecl": 1278898.31,
        "balance_pct": 0.06449909655553351
      },
      {
        "State": "Odisha",
        "balance": 19255398.67,
        "loans": 32,
        "ecl": 884738.29,
        "balance_pct": 0.06059501362802876
      },
      {
        "State": "Uttar Pradesh",
        "balance": 18870014.9,
        "loans": 32,
        "ecl": 1338968.58,
        "balance_pct": 0.05938224544828941
      },
      {
        "State": "Bihar",
        "balance": 18482016.49,
        "loans": 30,
        "ecl": 1174710.8499999999,
        "balance_pct": 0.05816124923083725
      },
      {
        "State": "Delhi",
        "balance": 17469604.27,
        "loans": 27,
        "ecl": 428510.89999999997,
        "balance_pct": 0.05497527872358092
      },
      {
        "State": "West Bengal",
        "balance": 16970779.62,
        "loans": 33,
        "ecl": 447920.5,
        "balance_pct": 0.05340552226292455
      },
      {
        "State": "Gujarat",
        "balance": 15518562.91,
        "loans": 25,
        "ecl": 1048098.0800000001,
        "balance_pct": 0.04883552644817151
      },
      {
        "State": "Punjab",
        "balance": 12122178.6,
        "loans": 24,
        "ecl": 531759.62,
        "balance_pct": 0.03814740946458931
      }
    ]
  }
};
