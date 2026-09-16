import streamlit as st
from datetime import date

from user import User
from person import Person
from blood_pressure_tracker import BloodPressureTracker
from monthly_summary import MonthlySummary


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="BPTrack",
    page_icon="🫀",
    layout="wide"
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
# HELPER FUNCTIONS
# ==========================================

def get_next_person_id():

    if not st.session_state.people:
        return 1

    return max(
        person.person_id
        for person in st.session_state.people
    ) + 1


def get_next_record_id():

    records = tracker.get_records()

    if not records:
        return 1

    return max(
        record.record_id
        for record in records
    ) + 1


def get_person_name(person_id):

    for person in st.session_state.people:

        if person.person_id == person_id:
            return person.get_name()

    return "Unknown"


def show_bp_card(record):

    color = record.get_category_color()

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            color:white;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
        ">
            <b style="font-size:24px;">
                {record.get_summary()}
            </b>
            <br>
            {record.get_bp_category()}
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# TITLE
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

    if st.button(
        "Login",
        use_container_width=True
    ):

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
# MAIN APPLICATION
# ==========================================

else:

    menu = st.sidebar.radio(
        "BPTrack Menu",
        [
            "Dashboard",
            "Manage People",
            "Add Record",
            "View Records",
            "Monthly Summary"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.user.logout()

        st.session_state.logged_in = False

        st.rerun()


    # ======================================
    # DASHBOARD
    # ======================================

    if menu == "Dashboard":

        st.header("Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "People",
            len(st.session_state.people)
        )

        col2.metric(
            "BP Records",
            len(tracker.get_records())
        )

        if tracker.get_records():

            latest = tracker.get_records()[-1]

            col3.metric(
                "Latest BP",
                latest.get_summary()
            )

            st.divider()

            st.subheader(
                "Latest Reading"
            )

            st.write(
                "**Person:**",
                get_person_name(
                    latest.person_id
                )
            )

            show_bp_card(latest)

        else:

            col3.metric(
                "Latest BP",
                "No Data"
            )

            st.info(
                "No blood pressure records yet."
            )


    # ======================================
    # MANAGE PEOPLE
    # ======================================

    elif menu == "Manage People":

        st.header(
            "Manage People"
        )

        # ADD PERSON
        st.subheader(
            "Add Person"
        )

        name = st.text_input(
            "Name"
        )

        if st.button(
            "Add Person",
            use_container_width=True
        ):

            name = name.strip()

            if name == "":

                st.error(
                    "Please enter a name."
                )

            else:

                duplicate = False

                for person in st.session_state.people:

                    if (
                        person.get_name().lower()
                        ==
                        name.lower()
                    ):

                        duplicate = True

                if duplicate:

                    st.warning(
                        "This person already exists."
                    )

                else:

                    person = Person(
                        get_next_person_id(),
                        name
                    )

                    st.session_state.people.append(
                        person
                    )

                    st.success(
                        "Person added successfully."
                    )

                    st.rerun()


        st.divider()


        # DELETE PERSON
        st.subheader(
            "Current People"
        )

        if not st.session_state.people:

            st.info(
                "No people added yet."
            )

        else:

            for person in st.session_state.people:

                st.write(
                    f"**{person.person_id}. "
                    f"{person.get_name()}**"
                )

            st.divider()

            delete_names = [
                person.get_name()
                for person
                in st.session_state.people
            ]

            person_to_delete = st.selectbox(
                "Select Person to Delete",
                delete_names
            )

            if st.button(
                "Delete Person",
                use_container_width=True
            ):

                selected_person = None

                for person in (
                    st.session_state.people
                ):

                    if (
                        person.get_name()
                        ==
                        person_to_delete
                    ):

                        selected_person = person
                        break

                if selected_person is not None:

                    person_id = (
                        selected_person.person_id
                    )

                    # Delete the person
                    st.session_state.people.remove(
                        selected_person
                    )

                    # Delete their BP records too
                    tracker.records = [
                        record
                        for record
                        in tracker.get_records()
                        if record.person_id
                        != person_id
                    ]

                    st.success(
                        "Person and associated "
                        "records deleted."
                    )

                    st.rerun()


    # ======================================
    # ADD RECORD
    # ======================================

    elif menu == "Add Record":

        st.header(
            "Add Blood Pressure Record"
        )

        if not st.session_state.people:

            st.warning(
                "Please add a person first."
            )

        else:

            people_names = [
                person.get_name()
                for person
                in st.session_state.people
            ]

            selected_name = st.selectbox(
                "Person",
                people_names
            )

            selected_person = None

            for person in (
                st.session_state.people
            ):

                if (
                    person.get_name()
                    ==
                    selected_name
                ):

                    selected_person = person


            col1, col2 = st.columns(2)

            systolic = col1.number_input(
                "Systolic (mmHg)",
                min_value=1,
                max_value=300,
                value=120
            )

            diastolic = col2.number_input(
                "Diastolic (mmHg)",
                min_value=1,
                max_value=200,
                value=80
            )


            pulse_na = st.checkbox(
                "Pulse rate is unavailable"
            )

            if pulse_na:

                pulse = "N/A"

            else:

                pulse = st.number_input(
                    "Pulse Rate (bpm)",
                    min_value=1,
                    max_value=250,
                    value=70
                )


            record_date = st.date_input(
                "Date",
                value=date.today()
            )

            notes = st.text_area(
                "Notes"
            )


            if st.button(
                "Save Record",
                use_container_width=True
            ):

                tracker.add_record(
                    get_next_record_id(),
                    selected_person.person_id,
                    int(systolic),
                    int(diastolic),
                    pulse,
                    notes,
                    record_date
                )

                record = (
                    tracker.get_records()[-1]
                )

                st.success(
                    "Blood pressure record saved."
                )

                show_bp_card(record)


    # ======================================
    # VIEW / EDIT / DELETE RECORDS
    # ======================================

    elif menu == "View Records":

        st.header(
            "Blood Pressure Records"
        )

        records = tracker.get_records()

        if not records:

            st.info(
                "No records available."
            )

        else:

            search = st.text_input(
                "Search by Name"
            )

            for record in records.copy():

                person_name = (
                    get_person_name(
                        record.person_id
                    )
                )

                if (
                    search == ""
                    or
                    search.lower()
                    in person_name.lower()
                ):

                    with st.expander(
                        f"{person_name} | "
                        f"{record.get_summary()} | "
                        f"{record.get_date()}"
                    ):

                        show_bp_card(record)

                        st.write(
                            "**Pulse:**",
                            record.get_pulse_rate()
                        )

                        st.write(
                            "**Date:**",
                            record.get_date()
                        )

                        st.write(
                            "**Notes:**",
                            record.get_notes()
                            or "No notes"
                        )


                        st.divider()

                        st.write(
                            "### Edit Record"
                        )


                        col1, col2 = (
                            st.columns(2)
                        )

                        new_systolic = (
                            col1.number_input(
                                "Systolic",
                                min_value=1,
                                max_value=300,
                                value=record.get_systolic(),
                                key=f"sys_{record.record_id}"
                            )
                        )

                        new_diastolic = (
                            col2.number_input(
                                "Diastolic",
                                min_value=1,
                                max_value=200,
                                value=record.get_diastolic(),
                                key=f"dia_{record.record_id}"
                            )
                        )


                        current_pulse = (
                            record.get_pulse_rate()
                        )

                        pulse_na = st.checkbox(
                            "Pulse unavailable",
                            value=(
                                current_pulse == "N/A"
                            ),
                            key=f"na_{record.record_id}"
                        )

                        if pulse_na:

                            new_pulse = "N/A"

                        else:

                            if isinstance(
                                current_pulse,
                                int
                            ):
                                default_pulse = (
                                    current_pulse
                                )

                            else:
                                default_pulse = 70

                            new_pulse = (
                                st.number_input(
                                    "Pulse Rate",
                                    min_value=1,
                                    max_value=250,
                                    value=default_pulse,
                                    key=f"pulse_{record.record_id}"
                                )
                            )


                        new_notes = st.text_area(
                            "Notes",
                            value=record.get_notes(),
                            key=f"notes_{record.record_id}"
                        )


                        col1, col2 = (
                            st.columns(2)
                        )


                        if col1.button(
                            "Save Changes",
                            key=f"edit_{record.record_id}",
                            use_container_width=True
                        ):

                            tracker.update_record(
                                record.record_id,
                                int(new_systolic),
                                int(new_diastolic),
                                new_pulse,
                                new_notes
                            )

                            st.success(
                                "Record updated."
                            )

                            st.rerun()


                        if col2.button(
                            "Delete Record",
                            key=f"delete_{record.record_id}",
                            use_container_width=True
                        ):

                            tracker.delete_record(
                                record.record_id
                            )

                            st.success(
                                "Record deleted."
                            )

                            st.rerun()


    # ======================================
    # MONTHLY SUMMARY
    # ======================================

    elif menu == "Monthly Summary":

        st.header(
            "Monthly Statistics"
        )

        if not st.session_state.people:

            st.info(
                "No people available."
            )

        elif not tracker.get_records():

            st.info(
                "No records available."
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


            selected_person = None

            for person in (
                st.session_state.people
            ):

                if (
                    person.get_name()
                    ==
                    selected_name
                ):

                    selected_person = person


            col1, col2 = st.columns(2)

            selected_month = col1.selectbox(
                "Month",
                list(range(1, 13)),
                index=date.today().month - 1
            )

            selected_year = col2.number_input(
                "Year",
                min_value=2000,
                max_value=2100,
                value=date.today().year
            )


            person_records = (
                tracker.search_by_person(
                    selected_person.person_id
                )
            )


            monthly_records = []

            for record in person_records:

                record_date = (
                    record.get_date()
                )

                if (
                    record_date.month
                    == selected_month
                    and
                    record_date.year
                    == selected_year
                ):

                    monthly_records.append(
                        record
                    )


            if not monthly_records:

                st.info(
                    "No records found for "
                    "this person during the "
                    "selected month."
                )

            else:

                summary = MonthlySummary(
                    monthly_records
                )

                st.subheader(
                    f"{selected_name}'s Summary"
                )

                col1, col2, col3, col4 = (
                    st.columns(4)
                )

                col1.metric(
                    "Total Records",
                    summary.get_total_records()
                )

                col2.metric(
                    "Average Systolic",
                    f"{summary.calculate_average_systolic():.1f}"
                )

                col3.metric(
                    "Average Diastolic",
                    f"{summary.calculate_average_diastolic():.1f}"
                )

                average_pulse = (
                    summary.calculate_average_pulse()
                )

                if average_pulse == 0:
                    pulse_display = "N/A"

                else:
                    pulse_display = (
                        f"{average_pulse:.1f}"
                    )

                col4.metric(
                    "Average Pulse",
                    pulse_display
                )


                st.divider()

                st.subheader(
                    "Records"
                )

                for record in monthly_records:

                    show_bp_card(record)

                    st.caption(
                        f"{record.get_date()} | "
                        f"Pulse: "
                        f"{record.get_pulse_rate()}"
                    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "BPTrack is for informational tracking "
    "only and is not a medical diagnosis."
)