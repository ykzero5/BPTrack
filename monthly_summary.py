# basic monthly statistics; average systolic, average diastolic,
# average pulse and total number of records

class MonthlySummary:

    def __init__(self, records):
        self.records = records

    def calculate_average_systolic(self):

        if not self.records:
            return 0

        total = 0

        for record in self.records:
            total += record.get_systolic()

        return total / len(self.records)

    def calculate_average_diastolic(self):

        if not self.records:
            return 0

        total = 0

        for record in self.records:
            total += record.get_diastolic()

        return total / len(self.records)

    def calculate_average_pulse(self):

        valid_pulses = []

        for record in self.records:

            pulse = record.get_pulse_rate()

            if isinstance(pulse, int):
                valid_pulses.append(pulse)

        if not valid_pulses:
            return 0

        return sum(valid_pulses) / len(valid_pulses)

    def get_total_records(self):

        return len(self.records)