# Import Streamlit to build the web application interface
import streamlit as st

# Import requests to communicate with the FastAPI backend
import requests

# Define the base URL of the FastAPI backend
API_BASE_URL = "http://127.0.0.1:8000"

# Configure the browser page before creating any Streamlit components
st.set_page_config(
    page_title="AI Lead Scoring",  # Text shown in the browser tab
    page_icon="🎯",                # Icon shown in the browser tab
    layout="wide"                 # Use the full browser width
)


# Display the main title of the application
st.title("🎯 AI Lead Scoring System")


# Display a short description explaining the purpose of the application
st.write(
    "Predict lead conversion probability and prioritize "
    "leads based on their likelihood of conversion."
)

# Check whether the FastAPI backend is running
try:
    # Send a request to the backend
    response = requests.get(API_BASE_URL)

    # Check whether the backend responded successfully
    if response.status_code == 200:

        # Display a success message when the backend is available
        st.success("🟢 Prediction API is connected and ready.")

    else:

        # Display a warning when the backend responds unexpectedly
        st.warning("🟡 Prediction API is running but returned an unexpected response.")

except requests.exceptions.RequestException:

    # Display an error when the backend cannot be reached
    st.error(
        "🔴 Prediction API is not available. "
        "Please start the FastAPI backend."
    )

# Add a horizontal line to visually separate the header from the next section
st.divider()

# Display a heading for the lead information section
st.subheader("📝 Lead Information")


# Create a form so all input values are submitted together
with st.form("lead_form"):

    # Create two columns for a cleaner and more professional layout
    col1, col2 = st.columns(2)

    # Place the first group of inputs in the left column
    with col1:

        # Select the source/origin through which the lead entered the system
        lead_origin = st.selectbox(
            "Lead Origin",
            [
                "Landing Page Submission",
                "API",
                "Lead Add Form",
                "Lead Import",
                "Quick Add Form"
            ]
        )

        # Select the specific source from which the lead was generated
        lead_source = st.text_input(
            "Lead Source",
            value="Google"
        )

        # Enter the country of the lead
        country = st.text_input(
            "Country",
            value="India"
        )

        # Select the lead's area of specialization
        specialization = st.text_input(
            "Specialization",
            value="Business Administration"
        )

        # Enter how the lead discovered the education platform
        heard_about_x_education = st.text_input(
            "How did you hear about X Education?",
            value="Online Search"
        )

        # Select the current occupation of the lead
        current_occupation = st.selectbox(
            "Current Occupation",
            [
                "Working Professional",
                "Unemployed",
                "Student",
                "Other"
            ]
        )

        # Enter the main factor influencing course selection
        course_selection_factor = st.text_input(
            "Course Selection Factor",
            value="Better Career Prospects"
        )


    # Place the second group of inputs in the right column
    with col2:

        # Enter the profile category of the lead
        lead_profile = st.text_input(
            "Lead Profile",
            value="Potential Lead"
        )

        # Enter the city of the lead
        city = st.text_input(
            "City",
            value="Mumbai"
        )

        # Select whether the lead should receive emails
        do_not_email = st.selectbox(
            "Do Not Email",
            ["No", "Yes"]
        )

        # Select whether the lead requested a free interview preparation copy
        free_mastering_interview_copy = st.selectbox(
            "Free Copy of Mastering The Interview",
            ["No", "Yes"]
        )

        # Enter the number of website visits
        total_visits = st.number_input(
            "Total Website Visits",
            min_value=0,
            value=5
        )

        # Enter the total time spent on the website
        total_time_spent_on_website = st.number_input(
            "Total Time Spent on Website",
            min_value=0,
            value=1200
        )

        # Enter the average number of page views per visit
        page_views_per_visit = st.number_input(
            "Page Views Per Visit",
            min_value=0.0,
            value=4.0
        )


    # Create the button that submits all form values
    submitted = st.form_submit_button(
        "🎯 Predict Lead Conversion"
    )
    # Check whether the user clicked the prediction button
if submitted:

    # Create a dictionary using the exact field names
    # expected by the FastAPI /predict endpoint
    lead_data = {
        "lead_origin": lead_origin,
        "lead_source": lead_source,
        "country": country,
        "specialization": specialization,
        "heard_about_x_education": heard_about_x_education,
        "current_occupation": current_occupation,
        "course_selection_factor": course_selection_factor,
        "lead_profile": lead_profile,
        "city": city,
        "do_not_email": do_not_email,
        "free_mastering_interview_copy": free_mastering_interview_copy,
        "total_visits": total_visits,
        "total_time_spent_on_website": total_time_spent_on_website,
        "page_views_per_visit": page_views_per_visit
    }

    # Define the URL of the FastAPI prediction endpoint
    API_URL = "http://127.0.0.1:8000/predict"

    # Display a spinner while waiting for the backend response
    with st.spinner("Analyzing lead..."):

        try:
            # Send the lead data to the FastAPI backend as JSON
            response = requests.post(
                API_URL,
                json=lead_data
            )

            # Raise an error if the API returned an unsuccessful status code
            response.raise_for_status()

            # Convert the JSON response into a Python dictionary
            result = response.json()

            # Display a success message when prediction is completed
            st.success("Lead prediction completed successfully!")

            # Display the complete API response temporarily for testing
            # Extract the prediction values returned by the FastAPI backend
            prediction = result["prediction"]
            probability = result["conversion_probability"]
            priority = result["lead_priority"]


            # Create a visual separator before displaying results
            st.divider()


            # Display the prediction results heading
            st.subheader("📊 Prediction Results")


            # Create three columns to display the main results
            col1, col2, col3 = st.columns(3)


            # Display the conversion prediction
            with col1:

                # Show the prediction label
                st.metric(
                    label="Prediction",
                    value=prediction
                )


            # Display the conversion probability as a percentage
            with col2:

                # Convert the decimal probability into percentage format
                probability_percentage = probability * 100

                # Show the probability
                st.metric(
                    label="Conversion Probability",
                    value=f"{probability_percentage:.2f}%"
                )


            # Display the business priority level
            with col3:

                # Show the assigned priority
                st.metric(
                    label="Lead Priority",
                    value=priority
                )


            # Display an additional business interpretation
            if priority == "High":

                # Show a success message for highly valuable leads
                st.success(
                    "🔥 High-priority lead! This lead should be contacted promptly."
                )

            elif priority == "Medium":

                # Show an informational message for medium-priority leads
                st.info(
                    "⚡ Medium-priority lead. Follow up with targeted communication."
                )

            else:

                # Show a neutral message for low-priority leads
                st.warning(
                    "📌 Low-priority lead. Consider automated or lower-cost follow-up."
                )

        except requests.exceptions.RequestException as error:

            # Display an error if the FastAPI backend cannot be reached
            st.error(
                f"Unable to connect to the prediction API: {error}"
            )
