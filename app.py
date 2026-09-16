import streamlit as st
import pandas as pd

from datetime import date, datetime
from zoneinfo import ZoneInfo

from person import Person
from blood_pressure_tracker import BloodPressureTracker
from monthly_summary import MonthlySummary

import storage


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="BPTrack",
    page_icon="❤️",
    layout="wide"
)


# ==========================================
# LOAD SAVED DATA
# ==========================================

if "people" not in st.session_state:
    st.session_state.people = storage.load_people()


if "tracker" not in st.session_state:

    tracker = BloodPressureTracker()

    tracker.records = storage.load_records()

    st.session_state.tracker = tracker


tracker = st.session_state.tracker


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_person_name(person_id):

    for person in st.session_state.people:

        if person.person_id == person_id:
            return person.get_name()

    return "Unknown"


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


def get_or_create_person(name):

    name = name.strip()

    for person in st.session_state.people:

        if (
            person.get_name().lower()
            == name.lower()
        ):
            return person

    person = Person(
        get_next_person_id(),
        name
    )

    st.session_state.people.append(
        person
    )

    storage.save_people(
        st.session_state.people
    )

    return person


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
            <b style="font-size:25px;">
                {record.get_summary()}
            </b>
            <br>
            {record.get_bp_category()}
        </div>
        """,
        unsafe_allow_html=True
    )


def show_alert(record):

    category = record.get_bp_category()

    if category == "Elevated":

        st.warning(
            "⚠️ Elevated blood pressure "
            "reading detected."
        )

    elif category == "Stage 1 Hypertension":

        st.warning(
            "⚠️ Stage 1 hypertension "
            "range detected."
        )

    elif category == "Stage 2 Hypertension":

        st.error(
            "⚠️ Stage 2 hypertension "
            "range detected."
        )

    elif category == "Hypertensive Crisis":

        st.error(
            "🚨 Hypertensive crisis range "
            "detected. This reading may "
            "require prompt medical attention."
        )


# ==========================================
# HEADER
# ==========================================

st.title("❤️ BPTrack")

st.caption(
    "Blood Pressure Tracking System"
)


# ==========================================
# NAVIGATION
# ==========================================

menu = st.sidebar.radio(
    "BPTrack Menu",
    [
        "Dashboard",
        "Add Record",
        "History",
        "Monthly Summary"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Close the browser tab to exit BPTrack."
)


# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.header(
        "Dashboard"
    )

    records = tracker.get_records()

    col1, col2 = st.columns(2)

    col1.metric(
        "People Tracked",
        len(st.session_state.people)
    )

    col2.metric(
        "Total BP Records",
        len(records)
    )

    st.divider()

    st.subheader(
        "Recent Blood Pressure Readings"
    )

    if not records:

        st.info(
            "No records yet. Select Add Record "
            "from the menu to begin."
        )

    else:

        recent_records = list(
            reversed(records[-5:])
        )

        for record in recent_records:

            person_name = get_person_name(
                record.person_id
            )

            st.write(
                f"### {person_name}"
            )

            show_bp_card(record)

            st.caption(
                f"{record.get_date()} "
                f"at "
                f"{record.get_time().strftime('%I:%M %p')} "
                f"| Pulse: "
                f"{record.get_pulse_rate()}"
            )

            st.divider()


# ==========================================
# ADD RECORD
# ==========================================

elif menu == "Add Record":

    st.header(
        "Add Blood Pressure Record"
    )

    person_name = st.text_input(
        "Person's Name"
    )

    col1, col2 = st.columns(2)

    systolic = col1.number_input(
        "Systolic Pressure (mmHg)",
        min_value=1,
        max_value=300,
        value=120
    )

    diastolic = col2.number_input(
        "Diastolic Pressure (mmHg)",
        min_value=1,
        max_value=200,
        value=80
    )

    pulse_unavailable = st.checkbox(
        "Pulse rate is unavailable"
    )

    if pulse_unavailable:

        pulse_rate = "N/A"

    else:

        pulse_rate = st.number_input(
            "Pulse Rate (bpm)",
            min_value=1,
            max_value=250,
            value=70
        )

    record_date = st.date_input(
        "Date",
        value=date.today()
    )

    record_time = st.time_input(
    "Time",
    value=datetime.now(
        ZoneInfo("Asia/Manila")
    ).time()
)

    notes = st.text_area(
        "Notes (Optional)"
    )

    if st.button(
        "Save Blood Pressure Record",
        use_container_width=True
    ):

        if person_name.strip() == "":

            st.error(
                "Please enter the person's name."
            )

        else:

            person = get_or_create_person(
                person_name
            )

            tracker.add_record(
                get_next_record_id(),
                person.person_id,
                int(systolic),
                int(diastolic),
                pulse_rate,
                notes,
                record_date,
                record_time
            )

            storage.save_records(
                tracker.get_records()
            )

            record = tracker.get_records()[-1]

            st.success(
                "Blood pressure record "
                "saved successfully."
            )

            show_bp_card(record)

            show_alert(record)

            st.caption(
                "Blood pressure categories are "
                "for informational tracking only."
            )


# ==========================================
# HISTORY
# ==========================================

elif menu == "History":

    st.header(
        "Blood Pressure History"
    )

    records = tracker.get_records()

    if not records:

        st.info(
            "No blood pressure records available."
        )

    else:

        search = st.text_input(
            "Search or Filter by Person's Name"
        )

        matching_records = []

        for record in records:

            name = get_person_name(
                record.person_id
            )

            if (
                search.strip() == ""
                or
                search.lower() in name.lower()
            ):

                matching_records.append(
                    record
                )

        if not matching_records:

            st.warning(
                "No matching records found."
            )

        for record in matching_records:

            person_name = get_person_name(
                record.person_id
            )

            title = (
                f"{person_name} | "
                f"{record.get_summary()} | "
                f"{record.get_date()}"
            )

            with st.expander(title):

                show_bp_card(record)

                st.write(
                    "**Pulse Rate:**",
                    record.get_pulse_rate()
                )

                st.write(
                    "**Date:**",
                    record.get_date()
                )

                st.write(
                    "**Time:**",
                    record.get_time().strftime(
                        "%I:%M %p"
                    )
                )

                st.write(
                    "**Notes:**",
                    record.get_notes()
                    or "No notes"
                )

                st.divider()

                st.subheader(
                    "Edit Record"
                )

                col1, col2 = st.columns(2)

                new_systolic = col1.number_input(
                    "Systolic",
                    min_value=1,
                    max_value=300,
                    value=record.get_systolic(),
                    key=(
                        f"systolic_"
                        f"{record.record_id}"
                    )
                )

                new_diastolic = col2.number_input(
                    "Diastolic",
                    min_value=1,
                    max_value=200,
                    value=record.get_diastolic(),
                    key=(
                        f"diastolic_"
                        f"{record.record_id}"
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
                    key=(
                        f"pulse_na_"
                        f"{record.record_id}"
                    )
                )

                if pulse_na:

                    new_pulse = "N/A"

                else:

                    if isinstance(
                        current_pulse,
                        int
                    ):

                        pulse_default = (
                            current_pulse
                        )

                    else:

                        pulse_default = 70

                    new_pulse = st.number_input(
                        "Pulse Rate",
                        min_value=1,
                        max_value=250,
                        value=pulse_default,
                        key=(
                            f"pulse_"
                            f"{record.record_id}"
                        )
                    )

                new_date = st.date_input(
                    "Date",
                    value=record.get_date(),
                    key=(
                        f"date_"
                        f"{record.record_id}"
                    )
                )

                new_time = st.time_input(
                    "Time",
                    value=record.get_time(),
                    key=(
                        f"time_"
                        f"{record.record_id}"
                    )
                )

                new_notes = st.text_area(
                    "Notes",
                    value=record.get_notes(),
                    key=(
                        f"notes_"
                        f"{record.record_id}"
                    )
                )

                col1, col2 = st.columns(2)

                if col1.button(
                    "Save Changes",
                    key=(
                        f"edit_"
                        f"{record.record_id}"
                    ),
                    use_container_width=True
                ):

                    success = tracker.update_record(
                        record.record_id,
                        int(new_systolic),
                        int(new_diastolic),
                        new_pulse,
                        new_notes,
                        new_date,
                        new_time
                    )

                    if success:

                        storage.save_records(
                            tracker.get_records()
                        )

                        st.success(
                            "Record updated successfully."
                        )

                        st.rerun()

                if col2.button(
                    "Delete Record",
                    key=(
                        f"delete_"
                        f"{record.record_id}"
                    ),
                    use_container_width=True
                ):

                    success = tracker.delete_record(
                        record.record_id
                    )

                    if success:

                        storage.save_records(
                            tracker.get_records()
                        )

                        st.success(
                            "Record deleted."
                        )

                        st.rerun()


# ==========================================
# MONTHLY SUMMARY
# ==========================================

elif menu == "Monthly Summary":

    st.header(
        "Monthly Summary and Trends"
    )

    if not st.session_state.people:

        st.info(
            "No people have been recorded yet."
        )

    elif not tracker.get_records():

        st.info(
            "No blood pressure records available."
        )

    else:

        names = [
            person.get_name()
            for person in st.session_state.people
        ]

        selected_name = st.selectbox(
            "Person",
            names
        )

        selected_person = None

        for person in st.session_state.people:

            if (
                person.get_name()
                == selected_name
            ):

                selected_person = person
                break

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
            value=date.today().year,
            step=1
        )

        person_records = (
            tracker.search_by_person(
                selected_person.person_id
            )
        )

        monthly_records = []

        for record in person_records:

            if (
                record.get_date().month
                == selected_month
                and
                record.get_date().year
                == selected_year
            ):

                monthly_records.append(
                    record
                )

        monthly_records.sort(
            key=lambda record: (
                record.get_date(),
                record.get_time()
            )
        )

        if not monthly_records:

            st.info(
                "No records found for this "
                "person during the selected month."
            )

        else:

            summary = MonthlySummary(
                monthly_records
            )

            st.subheader(
                f"{selected_name}'s Monthly Summary"
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
                (
                    f"{summary.calculate_average_systolic():.1f} "
                    f"mmHg"
                )
            )

            col3.metric(
                "Average Diastolic",
                (
                    f"{summary.calculate_average_diastolic():.1f} "
                    f"mmHg"
                )
            )

            average_pulse = (
                summary.calculate_average_pulse()
            )

            if average_pulse == 0:

                pulse_text = "N/A"

            else:

                pulse_text = (
                    f"{average_pulse:.1f} bpm"
                )

            col4.metric(
                "Average Pulse",
                pulse_text
            )


            # ==================================
            # TREND CHART
            # ==========================================

            st.divider()

            st.subheader(
                "Blood Pressure Trend"
            )

            chart_data = []

            for record in monthly_records:

                reading_datetime = (
                    datetime.combine(
                        record.get_date(),
                        record.get_time()
                    )
                )

                chart_data.append(
                    {
                        "Date and Time":
                            reading_datetime,

                        "Systolic":
                            record.get_systolic(),

                        "Diastolic":
                            record.get_diastolic()
                    }
                )

            chart_df = pd.DataFrame(
                chart_data
            )

            chart_df = chart_df.set_index(
                "Date and Time"
            )

            st.line_chart(
                chart_df
            )


            # ==================================
            # LATEST TREND
            # ==========================================

            if len(monthly_records) >= 2:

                previous = monthly_records[-2]
                latest = monthly_records[-1]

                difference = (
                    latest.get_systolic()
                    -
                    previous.get_systolic()
                )

                if difference > 0:

                    st.info(
                        f"↑ Latest systolic reading "
                        f"increased by {difference} mmHg "
                        f"from the previous reading."
                    )

                elif difference < 0:

                    st.info(
                        f"↓ Latest systolic reading "
                        f"decreased by "
                        f"{abs(difference)} mmHg "
                        f"from the previous reading."
                    )

                else:

                    st.info(
                        "→ Latest systolic reading "
                        "has not changed from the "
                        "previous reading."
                    )


            # ==================================
            # MONTHLY RECORDS
            # ==========================================

            st.divider()

            st.subheader(
                "Readings This Month"
            )

            for record in monthly_records:

                show_bp_card(record)

                st.caption(
                    f"{record.get_date()} "
                    f"at "
                    f"{record.get_time().strftime('%I:%M %p')} "
                    f"| Pulse: "
                    f"{record.get_pulse_rate()}"
                )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "BPTrack is a prototype for informational "
    "blood pressure tracking and is not intended "
    "to provide a medical diagnosis."
)