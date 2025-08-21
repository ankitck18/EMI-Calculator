from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pyloan import pyloan
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://localhost:3000"] for Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    principal: int
    rate: float
    term: int
    start_date: str
    payment_amount: int
    annual_payments: int
    interest_only_period: int
    compounding_method: str

@app.post("/calculate-loan")
def calculate_loan(req: LoanRequest):
    loan = pyloan.Loan(
        loan_amount=req.principal,
        interest_rate=req.rate,
        loan_term=req.term,
        start_date=req.start_date,
        payment_end_of_month=False,
        annual_payments=req.annual_payments,
        interest_only_period=req.interest_only_period,
        compounding_method=req.compounding_method
    )
    df = pd.DataFrame.from_records(
        loan.get_payment_schedule(),
        columns=pyloan.Payment._fields
    )
    return {"schedule": df.to_dict(orient="records")}
