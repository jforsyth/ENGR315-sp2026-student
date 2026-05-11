import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# folder where the yob files are saved
folder_path = r"C:\Users\phili\OneDrive\Desktop\CS Project\names (1)"

# Names I want to compare
names_to_analyze = ["Michael", "Jessica", "Ashley", "James", "Emily"]  # can change these names

# this means the code is looking for when a name drops to 50% of its peak
threshold_pct = 0.5

# Load all name data from the files
# data will look like:
# data["Michael"] = {1880: 354, 1881: 298, etc.}
data = {}

# go through every yob file in the folder
for filepath in sorted(glob.glob(os.path.join(folder_path, "yob*.txt"))):
    # get the year from the file name, like yob1995.txt -> 1995
    year = int(os.path.basename(filepath)[3:7])

    # read each line in the file
    with open(filepath, 'r') as f:
        for line in f:
            name, gender, count = line.strip().split(',')
            count = int(count)

            # only keep the names that are in my selected list
            if name in names_to_analyze:
                if name not in data:
                    data[name] = {}

                # add the count for that name in this year
                # this combines male and female counts if the name appears for both genders
                data[name][year] = data[name].get(year, 0) + count


# Print a summary table for the results
print(f"{'Name':<12} {'Peak Year':<12} {'Peak Count':<14} {'50% Decline Year':<20} {'Years to 50% Decline':<22} {'Decline Rate/Year'}")
print("-" * 95)

# create the graph
plt.figure(figsize=(12, 6))

# Analyze each name one at a time
for name in names_to_analyze:
    if name not in data:
        print(f"{name}: no data found")
        continue

    # sort years so the graph and calculations go in order
    years = sorted(data[name].keys())
    counts = [data[name][y] for y in years]

    years = np.array(years)
    counts = np.array(counts)

    # Find the peak year for the name
    # np.argmax gives the index where the count is highest
    peak_idx = np.argmax(counts)
    peak_year = years[peak_idx]
    peak_count = counts[peak_idx]

    # only look at the years after the name hit its peak
    # this lets us measure the "lifespan" after the name was most popular
    post_years = years[peak_idx:]
    post_counts = counts[peak_idx:]

    # Find the first year where the name dropped to 50% of its peak count
    target = peak_count * threshold_pct
    decline_year = None

    for i, c in enumerate(post_counts):
        if c <= target:
            decline_year = post_years[i]
            break

    # if a decline year was found, calculate how many years it took
    if decline_year:
        years_to_decline = decline_year - peak_year
    else:
        years_to_decline = None

    # Calculate the average decline rate after the peak
    # this uses a simple best-fit line for the post-peak years
    if len(post_years) > 1:
        decline_slope, _ = np.polyfit(post_years, post_counts, 1)
    else:
        decline_slope = 0

    # print the results for this name
    print(f"{name:<12} {peak_year:<12} {peak_count:<14} "
          f"{str(decline_year):<20} {str(years_to_decline):<22} {decline_slope:.1f}")

    # Plot the full count history for the name
    plt.plot(years, counts, linewidth=2, label=name)

    # add a vertical line at the peak year
    # this makes it easier to see when the decline starts
    plt.axvline(peak_year, linestyle='--', alpha=0.3)


# basic graph labels
plt.title("Baby Name Popularity Lifespan After Peak")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()

# show the graph
plt.show()
