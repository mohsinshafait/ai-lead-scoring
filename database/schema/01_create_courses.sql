-- Create the courses table to store EduGrowth's educational products.
CREATE TABLE courses (

    -- Unique identifier for each course.
    course_id SERIAL PRIMARY KEY,

    -- Name of the course offered to learners.
    course_name VARCHAR(150) NOT NULL,

    -- Main subject taught in the course.
    subject VARCHAR(100) NOT NULL,

    -- Educational level of the learner.
    student_level VARCHAR(50) NOT NULL,

    -- Delivery method of the course.
    learning_mode VARCHAR(50) NOT NULL,

    -- Duration of the course measured in weeks.
    duration_weeks INTEGER NOT NULL,

    -- Course fee or price.
    price NUMERIC(10, 2) NOT NULL,

    -- Indicates whether the course is currently available.
    is_active BOOLEAN DEFAULT TRUE,

    -- Timestamp when the course record was created.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);