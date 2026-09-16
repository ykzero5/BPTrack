# this handles: adding records, viewwing all records, finding a record,
# updating a record, deleting a record, and filtering by person

from blood_pressure_record import BloodPressureRecord


class BloodPressureTracker:

    def __init__(self):
        self.records = []

    def add_record(
        self,
        record_id,
        person_id,
        systolic,
        diastolic,
        pulse_rate,
        notes,
        date
    ):
        record = BloodPressureRecord(
            record_id,
            person_id,
            systolic,
            diastolic,
            pulse_rate,
            notes,
            date
        )

        self.records.append(record)

        return True

    def get_records(self):
        return self.records

    def find_record(self, record_id):

        for record in self.records:

            if record.record_id == record_id:
                return record

        return None

    def update_record(
        self,
        record_id,
        systolic,
        diastolic,
        pulse_rate,
        notes
    ):
        record = self.find_record(record_id)

        if record is None:
            return False

        return record.update_record(
            systolic,
            diastolic,
            pulse_rate,
            notes
        )

    def delete_record(self, record_id):

        record = self.find_record(record_id)

        if record is None:
            return False

        self.records.remove(record)

        return True

    def search_by_person(self, person_id):

        results = []

        for record in self.records:

            if record.person_id == person_id:
                results.append(record)

        return results