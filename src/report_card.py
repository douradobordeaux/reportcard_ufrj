import json
class Subject:
    def __init__(self, name, grade, credits):
        self.name = name
        self.grade = grade
        self.credits = credits
        self.result = grade >= 5

    def subject_to_dictionary(self):
        return {"name": self.name, "grade": self.grade, "credits": self.credits, "result": self.result}
    
    @staticmethod
    def subject_from_dictionary(data):
        subject = Subject(data["name"], data["grade"], data["credits"])
        return subject


class Period:
    def __init__(self, name):
        self.name = name
        self.subjects = []

    def insert_subject(self, subject):
        self.subjects.append(subject)

    def delete_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)

    def calculate_period_average(self):
        subject_grades_weighted_sum = sum(s.grade * s.credits for s in self.subjects)
        subject_credits_sum = sum(s.credits for s in self.subjects)
        return subject_grades_weighted_sum / subject_credits_sum if subject_credits_sum > 0 else 0

    def calculate_period_credits(self):
        return sum(s.credits for s in self.subjects)

    def calculate_period_earned_credits(self):
        return sum(s.credits for s in self.subjects if s.result)

    def calculate_period_fails(self):
        return sum(1 for s in self.subjects if not s.result)
    
    def period_to_dictionary(self):
        return {"name": self.name, "subjects": [s.subject_to_dictionary() for s in self.subjects]}
    
    @staticmethod
    def period_from_dictionary(data):
        period = Period(data["name"])
        period.subjects = [Subject.subject_from_dictionary(s) for s in data["subjects"]]
        return period

class ReportCard:

    def __init__(self):
        self.periods = []
    
    def insert_period(self, period):
        self.periods.append(period)
    
    def delete_period(self, period):
        if period in self.periods:
            self.periods.remove(period)

    def calculate_current_total_average(self, period):
        period_grades_weighted_sum = sum(p.calculate_period_average() * p.calculate_period_credits() for p in self.periods[:period])
        period_credits_sum = sum(p.calculate_period_credits() for p in self.periods[:period])
        return period_grades_weighted_sum / period_credits_sum if period_credits_sum > 0 else 0
    
    def calculate_current_total_credits(self, period):
        return sum(p.calculate_period_credits() for p in self.periods[:period])
    
    def calculate_current_total_earned_credits(self, period):
        return sum(p.calculate_period_earned_credits() for p in self.periods[:period])
    
    def calculate_current_total_fails(self, period):
        return sum(p.calculate_period_fails() for p in self.periods[:period])
    
    def report_card_to_dictionary(self):
        return {"periods": [p.period_to_dictionary() for p in self.periods]}
    
    def read_report_from_dictionary(self, data):
        self.periods = [Period.period_from_dictionary(p) for p in data["periods"]]

    def report_card_to_json(self):
        return json.dumps({"periods": [p.period_to_dictionary() for p in self.periods]}, indent=4)
    
    def report_card_from_json(self, json_string):
        data = json.loads(json_string)
        self.periods = [Period.period_from_dictionary(p) for p in data["periods"]]

    def save_to_file_json(self, filename):
        with open(filename, "w") as f:
            f.write(self.report_card_to_json())

    def load_from_file_json(self, filename):
        try:
            with open(filename, "r") as f:
                json_string = f.read()
                self.report_card_from_json(json_string)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading report card: {e}")

    # def print_report_card(self):
    #     print("\n\n")
    #     for i, p in enumerate(self.periods):
    #         print("\n====================")
    #         print(f"Period: {p.name}\n")
    #         for d in p.subjects:
    #             print(f"Subject: {d.name} / Grade: {d.grade} / Credits: {d.credits} / Result: {'Passed' if d.result else 'Failed'} \n")
    #         period_average = p.calculate_period_average()
    #         period_earned_credits = p.calculate_period_earned_credits()
    #         period_credits = p.calculate_period_credits()
    #         period_fails = p.calculate_period_fails()
    #         total_average = self.calculate_current_total_average(i + 1)
    #         total_earned_credits = self.calculate_current_total_earned_credits(i + 1)
    #         total_credits = self.calculate_current_total_credits(i + 1)
    #         total_fails = self.calculate_current_total_fails(i + 1)
    #         print(f"Period Average: {period_average:.2f} / Period Earned Credits: {period_earned_credits} / Period Credits: {period_credits} / Period Fails: {period_fails}")
    #         print(f"Total Average: {total_average:.2f} / Total Earned Credits: {total_earned_credits} / Total Credits: {total_credits} / Total Fails: {total_fails}")
    #         print("\n====================")