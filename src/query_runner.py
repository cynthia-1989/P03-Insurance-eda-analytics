# ================================================================
# src/query_runner.py
# P02 Insurance SQL — Query Runner
# ================================================================

import sys
import pathlib
import time
import pandas as pd

_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import engine, DB_AVAILABLE, SQL_DIR, INDUSTRY, logger


class SQLQueryRunner:
    """
    Executes SQL queries against the insurance PostgreSQL database.
    Returns SQL results as pandas DataFrames.
    """

    def __init__(self):
        self.industry = INDUSTRY
        self.history = []
        logger.info(f"SQLQueryRunner ready — schema: {self.industry}, db_available: {DB_AVAILABLE}")

    def run(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Execute a SQL query and return the result as a DataFrame.
        """
        if not DB_AVAILABLE or engine is None:
            logger.error("[SQL] Database not available. Check DB_URL in .env.")
            return pd.DataFrame()

        sql = sql.replace("{industry}", self.industry)
        start_time = time.time()

        try:
            df = pd.read_sql(sql, engine, params=params)

            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:100].strip(),
                "rows": len(df),
                "cols": len(df.columns),
                "duration_ms": duration_ms,
                "status": "success",
            })

            logger.info(
                f"[SQL] Query complete — {len(df):,} rows × {len(df.columns)} columns | {duration_ms} ms"
            )

            return df

        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:100].strip(),
                "rows": 0,
                "cols": 0,
                "duration_ms": duration_ms,
                "status": f"error: {str(e)[:100]}",
            })

            logger.error(f"[SQL] Query failed: {e}")
            return pd.DataFrame()

    def run_file(self, filename: str) -> pd.DataFrame:
        """
        Load a SQL file from the sql/ folder and execute it.
        """
        sql_path = SQL_DIR / filename

        if not sql_path.exists():
            logger.error(f"[SQL] File not found: {sql_path}")
            return pd.DataFrame()

        logger.info(f"[SQL] Loading SQL file: {filename}")

        sql_text = sql_path.read_text(encoding="utf-8")
        return self.run(sql_text)

    def demo_basics(self) -> None:
        """
        Run basic insurance table checks.
        """
        demos = [
            (
                "Sample claims",
                f"""
                SELECT
                    claim_id,
                    claim_date,
                    incident_date,
                    claim_type,
                    amount_claimed,
                    amount_approved,
                    status,
                    is_fraudulent
                FROM {self.industry}.claims
                LIMIT 10;
                """
            ),
            (
                "Sample policies",
                f"""
                SELECT
                    policy_id,
                    policy_type,
                    policy_number,
                    coverage_amount,
                    premium_monthly,
                    deductible,
                    start_date,
                    end_date
                FROM {self.industry}.policies
                LIMIT 10;
                """
            ),
           (
                "Sample customers",
                f"""
                SELECT
                    customer_id,
                    first_name,
                    last_name,
                    gender,
                    city,
                    occupation,
                    annual_income,
                    risk_score
                FROM {self.industry}.customers
                LIMIT 10;
                """
            ),
        ]

        for title, sql in demos:
            print(f"\n── {title}:")
            df = self.run(sql)
            if not df.empty:
                print(df.to_string(index=False))

    def demo_aggregation(self) -> None:
        """
        Run insurance claims aggregation.
        """
        sql = f"""
        SELECT
            p.policy_type,
            c.claim_type,
            COUNT(c.claim_id) AS total_claims,
            SUM(c.amount_claimed) AS total_claim_amount,
            SUM(c.amount_approved) AS total_approved_amount,
            AVG(c.amount_claimed) AS average_claim_amount,
            AVG(c.amount_approved) AS average_approved_amount
        FROM {self.industry}.claims c
        JOIN {self.industry}.policies p
            ON c.policy_id = p.policy_id
        GROUP BY
            p.policy_type,
            c.claim_type
        ORDER BY total_claim_amount DESC;
        """

        print("\n── Insurance Claims Aggregation by Policy Type and Claim Type:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def demo_joins(self) -> None:
        """
        Run joined insurance extract preview.
        """
        sql = f"""
        SELECT
            c.claim_id,
            c.claim_date,
            c.incident_date,
            c.claim_type,
            c.description,
            c.amount_claimed,
            c.amount_approved,
            c.status AS claim_status,
            c.processed_date,
            c.is_fraudulent,

            p.policy_id,
            p.policy_type,
            p.policy_number,
            p.coverage_amount,
            p.premium_monthly,
            p.deductible,
            p.start_date,
            p.end_date,
            p.status AS policy_status,
            p.risk_grade,

            cu.customer_id,
            cu.first_name,
            cu.last_name,
            cu.email,
            cu.phone,
            cu.date_of_birth,
            cu.gender,
            cu.city,
            cu.occupation,
            cu.annual_income,
            cu.credit_score,
            cu.risk_score,
            cu.customer_since,

            a.agent_id,
            a.first_name AS agent_first_name,
            a.last_name AS agent_last_name,
            a.email AS agent_email,
            a.phone AS agent_phone,
            a.license_number,
            a.specialization,
            a.years_exp,
            a.commission_rate,
            a.region,
            a.is_active,

            ra.assessment_id,
            ra.assessment_date,
            ra.risk_category,
            ra.risk_score AS assessment_risk_score,
            ra.factors,
            ra.recommended_premium

        FROM {self.industry}.claims c

        JOIN {self.industry}.policies p
            ON c.policy_id = p.policy_id

        JOIN {self.industry}.customers cu
            ON p.customer_id = cu.customer_id

        JOIN {self.industry}.agents a
            ON p.agent_id = a.agent_id

        LEFT JOIN {self.industry}.risk_assessments ra
            ON cu.customer_id = ra.customer_id

        LIMIT 10;
        """

        print("\n── Insurance Joined Extract Preview:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def __str__(self) -> str:
        return f"SQLQueryRunner(industry={self.industry!r}, queries_run={len(self.history)})"

    def __repr__(self) -> str:
        return f"SQLQueryRunner(industry={self.industry!r})"