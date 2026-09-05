-- Create the outcomes table to store the final
-- business outcome for each lead.
CREATE TABLE outcomes (

    -- Unique identifier for each outcome record.
    outcome_id SERIAL PRIMARY KEY,

    -- Lead associated with this outcome.
    lead_id INTEGER NOT NULL UNIQUE REFERENCES leads(lead_id),

    -- Indicates whether the lead eventually enrolled.
    converted BOOLEAN NOT NULL,

    -- Date when the enrollment happened, if the lead converted.
    enrollment_date TIMESTAMP,

    -- Revenue generated from the lead, if converted.
    revenue NUMERIC(10, 2),

    -- Final recorded outcome or reason.
    outcome_reason VARCHAR(150),

    -- Timestamp when the outcome was recorded.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);