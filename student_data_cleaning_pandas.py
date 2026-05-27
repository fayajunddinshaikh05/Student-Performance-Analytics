import pandas as pd

# Load Excel File
df = pd.read_excel(
    r"C:\Project_Learning\project_1\Student_Performance_Analytics.xlsx"
)

# Convert into DataFrame
df = pd.DataFrame(df)


# Basic Data Inspection


print(df.head())

print(df.info())

print(df.describe())

print(df.isnull().sum())



# Clean Column Names


df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("%", "pct")
)

# Fill Missing Values
df = df.fillna(0)



# Risk Level Classification


def risk_label(score):

    if score < 40:
        return "High Risk"

    elif score < 65:
        return "Moderate Risk"

    elif score < 80:
        return "Needs Monitoring"

    else:
        return "On Track"


df["Risk_Tier"] = df["Risk_Score"].apply(risk_label)

print("\nRisk Tier Counts:")
print(df["Risk_Tier"].value_counts())

print("\nStudent Risk Classification:")
print(df[["Student_Name", "Risk_Score", "Risk_Tier"]])


# Dual Risk Students


df["Dual_Risk_Flag"] = (
    (df["Avg_Grade"] < 50) &
    (df["Attendance_pct"] < 70)
)

print("\nDual Risk Students:")

print(
    df[
        df["Dual_Risk_Flag"] == True
    ][
        [
            "Student_Name",
            "Avg_Grade",
            "Attendance_pct",
            "Dual_Risk_Flag"
        ]
    ]
)
