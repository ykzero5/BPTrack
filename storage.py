from person import Person
from blood_pressure_record import BloodPressureRecord


PEOPLE_FILE = "people.txt"
RECORDS_FILE = "records.txt"


# ==========================================
# PEOPLE
# ==========================================

def save_people(people):

    with open(
        PEOPLE_FILE,
        "w"
    ) as file:

        for person in people:

            file.write(
                f"Person ID: {person.person_id}\n"
            )

            file.write(
                f"Name: {person.get_name()}\n\n"
            )


def load_people():

    people = []

    try:

        with open(
            PEOPLE_FILE,
            "r"
        ) as file:

            lines = file.readlines()

    except FileNotFoundError:

        return people


    current = {}

    for line in lines:

        line = line.strip()

        if not line:
            continue


        if line.startswith(
            "Person ID:"
        ):

            current["person_id"] = int(
                line.replace(
                    "Person ID:",
                    ""
                ).strip()
            )


        elif line.startswith(
            "Name:"
        ):

            current["name"] = (
                line.replace(
                    "Name:",
                    ""
                ).strip()
            )


            if (
                "person_id" in current
                and
                "name" in current
            ):

                person = Person(
                    current["person_id"],
                    current["name"]
                )

                people.append(
                    person
                )

                current = {}


    return people


# ==========================================
# RECORDS
# ==========================================

def save_records(records):

    with open(
        RECORDS_FILE,
        "w"
    ) as file:

        for record in records:

            file.write(
                f"Record ID: "
                f"{record.record_id}\n"
            )

            file.write(
                f"Person ID: "
                f"{record.person_id}\n"
            )

            file.write(
                f"Systolic: "
                f"{record.get_systolic()}\n"
            )

            file.write(
                f"Diastolic: "
                f"{record.get_diastolic()}\n"
            )

            file.write(
                f"Pulse Rate: "
                f"{record.get_pulse_rate()}\n"
            )

            file.write(
                f"Date: "
                f"{record.get_date()}\n"
            )

            file.write(
                f"Time: "
                f"{record.get_time().strftime('%H:%M:%S')}\n"
            )

            file.write(
                f"Notes: "
                f"{record.get_notes()}\n\n"
            )


def load_records():

    records = []

    try:

        with open(
            RECORDS_FILE,
            "r"
        ) as file:

            lines = file.readlines()

    except FileNotFoundError:

        return records


    current = {}


    for line in lines:

        line = line.strip()

        if not line:
            continue


        if line.startswith(
            "Record ID:"
        ):

            current["record_id"] = int(
                line.replace(
                    "Record ID:",
                    ""
                ).strip()
            )


        elif line.startswith(
            "Person ID:"
        ):

            current["person_id"] = int(
                line.replace(
                    "Person ID:",
                    ""
                ).strip()
            )


        elif line.startswith(
            "Systolic:"
        ):

            current["systolic"] = int(
                line.replace(
                    "Systolic:",
                    ""
                ).strip()
            )


        elif line.startswith(
            "Diastolic:"
        ):

            current["diastolic"] = int(
                line.replace(
                    "Diastolic:",
                    ""
                ).strip()
            )


        elif line.startswith(
            "Pulse Rate:"
        ):

            pulse = (
                line.replace(
                    "Pulse Rate:",
                    ""
                ).strip()
            )

            if pulse == "N/A":

                current["pulse_rate"] = "N/A"

            else:

                current["pulse_rate"] = int(
                    pulse
                )


        elif line.startswith(
            "Date:"
        ):

            from datetime import datetime

            date_text = (
                line.replace(
                    "Date:",
                    ""
                ).strip()
            )

            current["date"] = (
                datetime.strptime(
                    date_text,
                    "%Y-%m-%d"
                ).date()
            )


        elif line.startswith(
            "Time:"
        ):

            from datetime import datetime

            time_text = (
                line.replace(
                    "Time:",
                    ""
                ).strip()
            )

            current["time"] = (
                datetime.strptime(
                    time_text,
                    "%H:%M:%S"
                ).time()
            )


        elif line.startswith(
            "Notes:"
        ):

            current["notes"] = (
                line.replace(
                    "Notes:",
                    ""
                ).strip()
            )


            if (
                "record_id" in current
                and
                "person_id" in current
                and
                "systolic" in current
                and
                "diastolic" in current
                and
                "pulse_rate" in current
                and
                "date" in current
                and
                "time" in current
            ):

                record = BloodPressureRecord(
                    current["record_id"],
                    current["person_id"],
                    current["systolic"],
                    current["diastolic"],
                    current["pulse_rate"],
                    current.get(
                        "notes",
                        ""
                    ),
                    current["date"],
                    current["time"]
                )

                records.append(
                    record
                )

                current = {}


    return records