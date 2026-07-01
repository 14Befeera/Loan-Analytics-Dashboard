from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_excel("loan_data.xlsx")

# -----------------------------
# Business KPIs
# -----------------------------
total_applications = len(df)
approved_loans = len(df[df["LoanStatus"] == "Y"])
rejected_loans = len(df[df["LoanStatus"] == "N"])
approval_rate = round((approved_loans / total_applications) * 100, 2)

# -----------------------------
# Chart 1 - Loan Approval
# -----------------------------
loan_chart = px.pie(
    df,
    names="LoanStatus",
    title="Loan Approval Distribution",
    color="LoanStatus",
    color_discrete_map={
        "Y": "#2E86DE",
        "N": "#E74C3C"
    }
)

loan_chart.update_layout(title_x=0.5)

loan_chart_html = loan_chart.to_html(full_html=False)

# -----------------------------
# Chart 2 - Property Area
# -----------------------------
property_chart = px.histogram(
    df,
    x="PropertyArea",
    color="PropertyArea",
    title="Applications by Property Area"
)

property_chart.update_layout(title_x=0.5)

property_chart_html = property_chart.to_html(full_html=False)

# -----------------------------
# Chart 3 - Income vs Loan Amount
# -----------------------------
income_chart = px.scatter(
    df,
    x="ApplicantIncome",
    y="LoanAmount",
    color="LoanStatus",
    title="Applicant Income vs Loan Amount"
)

income_chart.update_layout(title_x=0.5)

income_chart_html = income_chart.to_html(full_html=False)

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():

    return render_template(
        "index.html",

        total=total_applications,
        approved=approved_loans,
        rejected=rejected_loans,
        approval_rate=approval_rate,

        loan_chart=loan_chart_html,
        property_chart=property_chart_html,
        income_chart=income_chart_html
    )

# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)