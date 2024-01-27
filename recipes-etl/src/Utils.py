import re


class Utils:
    def extract_time_in_minutes(time_string):
        time_pattern = re.compile(r'(\d+)([HM])')

        total_minutes = 0

        matches = time_pattern.findall(time_string)

        for value, unit in matches:
            value = int(value)
            if unit == 'H':
                total_minutes += value * 60
            elif unit == 'M':
                total_minutes += value

        return total_minutes
