-- Create the sales_actions table to store actions
-- taken by the business for a specific lead.
CREATE TABLE sales_actions (

    -- Unique identifier for each sales action.
    action_id SERIAL PRIMARY KEY,

    -- Lead associated with this sales action.
    lead_id INTEGER NOT NULL REFERENCES leads(lead_id),

    -- Type of action taken or recommended.
    action_type VARCHAR(100) NOT NULL,

    -- Priority level of the action.
    priority VARCHAR(20),

    -- Current status of the action.
    action_status VARCHAR(50) DEFAULT 'Pending',

    -- Optional notes or details about the action.
    action_details TEXT,

    -- Timestamp when the action was created.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Timestamp when the action was completed.
    completed_at TIMESTAMP
);