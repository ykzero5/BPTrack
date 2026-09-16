class BloodPressureRecord:

    def __init__(
        self,
        record_id,
        person_id,
        systolic,
        diastolic,
        pulse_rate,
        notes,
        date
    ):
        self.record_id = record_id
        self.person_id = person_id

        # Encapsulation
        self._systolic = systolic
        self._diastolic = diastolic
        self._pulse_rate = pulse_rate
        self._notes = notes
        self._date = date

    def get_systolic(self):
        return self._systolic

    def get_diastolic(self):
        return self._diastolic

    def get_pulse_rate(self):
        return self._pulse_rate

    def get_notes(self):
        return self._notes

    def get_date(self):
        return self._date

    def update_record(
        self,
        systolic,
        diastolic,
        pulse_rate,
        notes
    ):
        if systolic <= 0 or diastolic <= 0:
            return False

        self._systolic = systolic
        self._diastolic = diastolic
        self._pulse_rate = pulse_rate
        self._notes = notes

        return True

    def get_summary(self):

        return (
            f"{self._systolic}/"
            f"{self._diastolic} mmHg"
        )

    def get_bp_category(self):

        systolic = self._systolic
        diastolic = self._diastolic

        if systolic > 180 or diastolic > 120:
            return "Hypertensive Crisis"

        elif systolic >= 140 or diastolic >= 90:
            return "Stage 2 Hypertension"

        elif systolic >= 130 or diastolic >= 80:
            return "Stage 1 Hypertension"

        elif systolic >= 120 and diastolic < 80:
            return "Elevated"

        else:
            return "Normal"

    def get_category_color(self):

        category = self.get_bp_category()

        if category == "Normal":
            return "green"

        elif category == "Elevated":
            return "gold"

        elif category == "Stage 1 Hypertension":
            return "orange"

        elif category == "Stage 2 Hypertension":
            return "red"

        else:
            return "darkred"