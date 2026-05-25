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

FROM insurance.claims c

JOIN insurance.policies p
    ON c.policy_id = p.policy_id

JOIN insurance.customers cu
    ON p.customer_id = cu.customer_id

JOIN insurance.agents a
    ON p.agent_id = a.agent_id

LEFT JOIN insurance.risk_assessments ra
    ON cu.customer_id = ra.customer_id

LIMIT 50;