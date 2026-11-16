
import math


def parse_vitals_summary(vitals_csv):
    if not isinstance(vitals_csv, str):
        return "Invalid vitals input"

    parts = vitals_csv.split(',')

    if len(parts) != 3:
        return "Invalid vitals input"

    try:
        hr, spo2, temp = (
            float(part.strip()) for part in parts
        )
    except (ValueError, OverflowError):
        return "Invalid vitals input"

    if not all(
        math.isfinite(value)
        for value in (hr, spo2, temp)
    ):
        return "Invalid vitals input"

    if hr <= 0 or not (0 <= spo2 <= 100) or temp <= 0:
        return "Invalid vitals input"

    critical = (
        hr > 120
        or spo2 < 90
        or temp > 39.0
    )

    return (
        f"Vitals: HR={hr}, SpO2={spo2}% - "
        f"{'CRITICAL' if critical else 'STABLE'}"
    )


def compute_patient_bmi(bmi_string):
    if not isinstance(bmi_string, str):
        return None

    parts = bmi_string.split('/')

    if len(parts) != 2:
        return None

    try:
        weight, height = (
            float(part.strip()) for part in parts
        )

        if not (
            math.isfinite(weight)
            and math.isfinite(height)
        ):
            return None

        if weight <= 0 or height <= 0:
            return None

        bmi = weight / (height ** 2)

        if not math.isfinite(bmi):
            return None

        return round(bmi, 2)

    except (ValueError, OverflowError, ZeroDivisionError):
        return None


def assign_ward_bed(allocation_code):
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }

    if not isinstance(allocation_code, str):
        return "Invalid allocation code"

    parts = allocation_code.strip().split('-')

    if len(parts) != 2:
        return "Invalid allocation code"

    ward = parts[0].strip().upper()
    bed_str = parts[1].strip()

    if ward not in ward_names or not bed_str.isdecimal():
        return "Invalid allocation code"

    try:
        bed_num = int(bed_str)
    except ValueError:
        return "Invalid allocation code"

    if bed_num <= 0:
        return "Invalid allocation code"

    return f"{ward_names[ward]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()
