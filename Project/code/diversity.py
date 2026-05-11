import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# folder where the baby name files are stored
folder_path = r"C:\Users\phili\OneDrive\Desktop\CS Project\names (1)"

# these lists will store each year and the top 10 name share for that year
years = []
top10_proportions = []

# go through every yob file in the folder
for filepath in sorted(glob.glob(os.path.join(folder_path, "yob*.txt"))):
    # get the year from the file name
    year = int(os.path.basename(filepath)[3:7])
    
    records = []

    # read all the name counts from this year
    with open(filepath, 'r') as f:
        for line in f:
            name, gender, count = line.strip().split(',')

            # only the count is needed for this question
            records.append(int(count))
    
    # total number of births recorded in this year
    total = sum(records)

    # add up the 10 most common name counts
    top10 = sum(sorted(records, reverse=True)[:10])
    
    # save the year and the share of births from the top 10 names
    years.append(year)
    top10_proportions.append(top10 / total)

# Find the year with highest and lowest diversity
# A higher top 10 proportion means less diversity, since fewer names make up more births
max_prop_year = years[top10_proportions.index(max(top10_proportions))]

# A lower top 10 proportion means more diversity, since names are more spread out
min_prop_year = years[top10_proportions.index(min(top10_proportions))]

print(f"Least diverse year: {max_prop_year} — top 10 names accounted for {max(top10_proportions)*100:.1f}% of births")
print(f"Most diverse year:  {min_prop_year} — top 10 names accounted for {min(top10_proportions)*100:.1f}% of births")

# Overall change from the first year in the dataset to the last year
print(f"\nProportion in {years[0]}: {top10_proportions[0]*100:.1f}%")
print(f"Proportion in {years[-1]}: {top10_proportions[-1]*100:.1f}%")
print(f"Overall change: {(top10_proportions[-1] - top10_proportions[0])*100:.1f} percentage points")

# Calculate average top 10 share by decade
# this helps show the trend in a cleaner way than looking at every single year
print("\nAverage top 10 share by decade:")
for decade_start in range(1880, 2030, 10):
    decade_vals = [
        top10_proportions[i]
        for i, y in enumerate(years)
        if decade_start <= y < decade_start + 10
    ]

    # only print the decade if there is data for it
    if decade_vals:
        print(f"  {decade_start}s: {sum(decade_vals)/len(decade_vals)*100:.1f}%")

# Plot the top 10 name share over time
plt.figure(figsize=(10, 6))

plt.plot(years, top10_proportions, color='steelblue', linewidth=2)

# If the line goes down, that means names are becoming more diverse
plt.title('Name Diversity Over Time\n(Proportion of Births in Top 10 Names)')
plt.xlabel('Year')
plt.ylabel('Proportion of Births in Top 10 Names')

plt.tight_layout()
plt.show()
