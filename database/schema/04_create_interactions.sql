-- Create the interactions table to store events and activities
-- associated with a lead after entering the system.
CREATE TABLE interactions (

    -- Unique identifier for each interaction.
    interaction_id SERIAL PRIMARY KEY,

    -- Lead associated with this interaction.
    lead_id INTEGER NOT NULL REFERENCES leads(lead_id),

    -- Type of interaction or event.
    interaction_type VARCHAR(100) NOT NULL,

    -- Channel where the interaction occurred.
    interaction_channel VARCHAR(50),

    -- Additional information about the interaction, if needed.
    interaction_details TEXT,

    -- Timestamp when the interaction occurred.
    interaction_at TIMESTAMP NOT NULL
);