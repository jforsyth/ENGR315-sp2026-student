import pandas as pd
import matplotlib.pyplot as plt

#Load NYC Traffic Report dataset & read file w/ pandas
file_path = r"C:\Users\thatt\OneDrive_Personal\OneDrive\Desktop\ENGR315-sp2026-student\Project\Motor_Vehicle_Collisions_-_Crashes.csv"
#My (Josh J) OneDrive gives conflicting errors regarding the file path. To resolve, copy exact file path to .csv and paste as raw string for 'file_path'.
df = pd.read_csv(file_path)

#Seperate data file columns, clean for easier analysis
df.columns = df.columns.str.strip()
# Extract wanted data
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'], errors='coerce')
df['CRASH TIME'] = pd.to_datetime(df['CRASH TIME'], format='%H:%M', errors='coerce')
df['HOUR'] = df['CRASH TIME'].dt.hour

#Q1 - How have crashes trended over the years?
#Convert dates into month-year format
df['MONTH_YEAR'] = df['CRASH DATE'].dt.to_period('M')
monthly_data = df['MONTH_YEAR'].value_counts().sort_index().reset_index()
monthly_data.columns = ['Month-Year', 'Total Crashes']
#Print info
print("Crash Trends Over Time")
print(monthly_data)
print("\n")
#Plot info
plt.figure(figsize=(12, 6))
plt.plot(monthly_data['Month-Year'].dt.to_timestamp(), monthly_data['Total Crashes'], color='tab:blue')
plt.title('Monthly Trend of NYC Crashes', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Number of Accidents')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

#Q4 - What is historically the most dangerous time/place to drive?
#Sort crash reports by borough, if no borough is reported, remove data from set
#Sort each borough's data by time of day
df_filtered = df.dropna(subset=['BOROUGH'])
borough_hour_data = df_filtered.groupby(['BOROUGH', 'HOUR']).size().unstack(level=0).fillna(0)
#Print info
print("Most Dangerous Time and Place to Drive")
print(borough_hour_data)
print("\n")
#Plot info, plot each borough
plt.figure(figsize=(12, 7))
for borough in borough_hour_data.columns:
    plt.plot(borough_hour_data.index, borough_hour_data[borough], marker='.', label=borough)
#Plot titles and labels
plt.title('Accidents by Hour Across NYC Boroughs', fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Number of Accidents')
plt.xticks(range(0, 24))
plt.legend(title='Borough', loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()

#Q5 - What are the most common contributing factors to accidents?
#Compile all contributing factors of crashes into a single list, count total occurances for each factor
factor_cols = ['CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2',
               'CONTRIBUTING FACTOR VEHICLE 3', 'CONTRIBUTING FACTOR VEHICLE 4',
               'CONTRIBUTING FACTOR VEHICLE 5']
all_factors = pd.concat([df[col] for col in factor_cols]).dropna()
factor_data = all_factors[all_factors != 'Unspecified'].value_counts().head(10).reset_index()
factor_data.columns = ['Contributing Factor', 'Occurrence Count']
#Print list of contributing factors by occurance count
print("Contributing Factors")
print(factor_data)
print("\n")
#Plot bar graph of contributing factors
plt.figure(figsize=(10, 6))
plt.bar(factor_data['Contributing Factor'], factor_data['Occurrence Count'], color='tab:green', edgecolor='black')
plt.title('Contributing Factors', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

