import streamlit as st
from datetime import date

from user import User
from person import Person
from blood_pressure_tracker import BloodPressureTracker
from monthly_summary import MonthlySummary


st.set_page_config(
    page_title="BPTrack",
    page_icon="🫀"
)


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = User(
        1,
        "admin",
        "1234"
    )

if "people" not in st.session_state:
    st.session_state.people = []

if "tracker" not in st.session_state:
    st.session_state.tracker = BloodPressureTracker()


tracker = st.session_state.tracker


# ==========================================
# HELPER
# ==========================================

def get_person_name(person_id):

    for person in st.session_state.people:

        if person.person_id == person_id:
            return person.get_name()

    return "Unknown"


# ==========================================
# HEADER
# ==========================================

st.title("🫀 BPTrack")

st.caption(
    "Blood Pressure Tracking System"
)


# ==========================================
# LOGIN
# ==========================================

if not st.session_state.logged_in:

    st.subheader("Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if st.session_state.user.login(
            username,
            password
        ):

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    st.info(
        "Prototype Login: admin / 1234"
    )


# ==========================================
# MAIN APP
# ==========================================

else:

    menu = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Add Person",
            "Add Record",
            "View Records",
            "Monthly Summary"
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.user.logout()
        st.session_state.logged_in = False

        st.rerun()


    # ======================================
    # DASHBOARD
    # ======================================

    if menu == "Dashboard":

        st.header("Dashboard")

        col1, col2 = st.columns(2)

        col1.metric(
            "People",
            len(st.session_state.people)
        )

        col2.metric(
            "BP Records",
            len(tracker.get_records())
        )

        st.info(
            "Use the menu to manage "
            "blood pressure records."
        )


    # ======================================
    # ADD PERSON
    # ======================================

    elif menu == "Add Person":

        st.header("Add Person")

        name = st.text_input(
            "Name"
        )

        if st.button("Save Person"):

            if name.strip() == "":

                st.error(
                    "Please enter a name."
                )

            else:

                person = Person(
                    len(
                        st.session_state.people
                    ) + 1,
                    name.strip()
                )

                st.session_state.people.append(
                    person
                )

                st.success(
                    "Person added successfully."
                )


    # ======================================
    # ADD RECORD
    # ======================================

    elif menu == "Add Record":

        st.header(
            "Add Blood Pressure Record"
        )

        if not st.session_state.people:

            st.warning(
                "Add a person first."
            )

        else:

            names = [
                person.get_name()
                for person
                in st.session_state.people
            ]

            selected_name = st.selectbox(
                "Person",
                names
            )

            selected_person = (
                st.session_state.people[
                    names.index(
                        selected_name
                    )
                ]
            )

            systolic = st.number_input(
                "Systolic",
                min_value=1,
                value=120
            )

            diastolic = st.number_input(
                "Diastolic",
                min_value=1,
                value=80
            )

            pulse = st.number_input(
                "Pulse Rate",
                min_value=1,
                value=70
            )

            notes = st.text_input(
                "Notes"
            )

            record_date = st.date_input(
                "Date",
                date.today()
            )

            if st.button("Save Record"):

                tracker.add_record(
                    len(
                        tracker.get_records()
                    ) + 1,
                    selected_person.person_id,
                    int(systolic),
                    int(diastolic),
                    int(pulse),
                    notes,
                    record_date
                )

                record = (
                    tracker.get_records()[-1]
                )

                st.success(
                    "Record saved."
                )

                color = (
                    record.get_category_color()
                )

                st.markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        color:white;
                        padding:15px;
                        border-radius:10px;
                    ">
                    <b>
                    {record.get_summary()}
                    </b><br>
                    {record.get_bp_category()}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ======================================
    # VIEW RECORDS
    # ======================================

    elif menu == "View Records":

        st.header("BP Records")

        search = st.text_input(
            "Search by Name"
        )

        for record in tracker.get_records():

            name = get_person_name(
                record.person_id
            )

            if (
                search == ""
                or
                search.lower()
                in name.lower()
            ):

                st.subheader(name)

                color = (
                    record.get_category_color()
                )

                st.markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        color:white;
                        padding:12px;
                        border-radius:10px;
                    ">
                    <b>
                    {record.get_summary()}
                    </b><br>
                    {record.get_bp_category()}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write(
                    "Pulse:",
                    record.get_pulse_rate()
                )

                st.write(
                    "Date:",
                    record.get_date()
                )

                st.write(
                    "Notes:",
                    record.get_notes()
                )

                st.divider()


    # ======================================
    # MONTHLY SUMMARY
    # ======================================

    elif menu == "Monthly Summary":

        st.header(
            "Monthly Statistics"
        )

        if not tracker.get_records():

            st.info(
                "No records available."
            )

        else:

            summary = MonthlySummary(
                tracker.get_records()
            )

            col1, col2, col3 = (
                st.columns(3)
            )

            col1.metric(
                "Average Systolic",
                f"{summary.calculate_average_systolic():.1f}"
            )

            col2.metric(
                "Average Diastolic",
                f"{summary.calculate_average_diastolic():.1f}"
            )

            col3.metric(
                "Total Records",
                summary.get_total_records()
            )


st.caption(
    "BPTrack is for informational "
    "tracking only and is not a medical diagnosis."
)