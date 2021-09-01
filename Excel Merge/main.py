# importing the required modules
import glob
import pandas as pd
import os


def clear(): return os.system('cls')


# check to see if output directory present, if not then create

directory = "output"

if not os.path.exists(directory):
    print("Directory does not exist! Creating directory")
    os.makedirs(directory)


# Fetch .xlsx files in directory of .py script
location = "*.xlsx"
excel_files = glob.glob(location)

# Create empty DataFrame
df1 = pd.DataFrame()

# Concat .xlsx files
clear()
print("Combining .xlsx files")

for excel_file in excel_files:
    df2 = pd.read_excel(excel_file)
    df1 = pd.concat([df1,df2])


# Write to merged.xlsx
clear()
print("Saving merged document to output/merged.xlsx")
df1.to_excel("output\\merged.xlsx", index=False)

# Read newly saved merged.xlsx file and create new column(s)
df = pd.read_excel("output\\merged.xlsx")
df["ValueX50"] = df.Item.value_counts().Pen * 50

# Write newly calculated columns to final .xlsx file on the Desktop
clear()
print("Saving final document")
df.to_excel("output\\Final.xlsx", index=False)
