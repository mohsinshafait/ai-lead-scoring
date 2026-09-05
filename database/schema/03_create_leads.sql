-- Create the leads table to store potential customers
-- who are interested in EduGrowth's educational services.
CREATE TABLE leads (

    -- Unique identifier for each lead.
    lead_id SERIAL PRIMARY KEY,

    -- The learner associated with this lead.
    learner_id INTEGER REFERENCES learners(learner_id),

    -- The course the lead is interested in.
    course_id INTEGER REFERENCES courses(course_id),

    -- First name of the person who contacted EduGrowth.
    contact_first_name VARCHAR(100) NOT NULL,

    -- Last name of the contact person.
    contact_last_name VARCHAR(100) NOT NULL,

    -- Contact person's email address.
    email VARCHAR(255),

    -- Contact person's phone number.
    phone VARCHAR(30),

    -- Indicates who is making the enrollment decision.
    decision_maker_type VARCHAR(50) NOT NULL,

    -- How the lead first discovered EduGrowth.
    lead_source VARCHAR(100) NOT NULL,

    -- Marketing campaign associated with the lead, if available.
    campaign VARCHAR(150),

    -- Type of inquiry.
    lead_type VARCHAR(100) NOT NULL,

    -- Preferred method for contacting the lead.
    preferred_contact_method VARCHAR(50),

    -- Lead's available budget for the educational service.
    budget NUMERIC(10, 2),

    -- Current status of the lead in the business process.
    lead_status VARCHAR(50) DEFAULT 'New',

    -- Timestamp when the lead entered the system.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);