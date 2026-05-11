import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# folder where all the yob files are stored
folder_path = r"C:\Users\phili\OneDrive\Desktop\CS Project\names (1)"

# Names I want to analyze, with the gender that matches the SSA dataset
selected_names = {
    "Michael": "M",
    "Jessica": "F",
    "Ashley": "F",
    "James": "M",
    "Emily": "F"
}

# name of the graph file that gets saved
output_file = "task5_q1_name_popularity_projection.png"

# This dictionary will hold all of the data for each name
# Example:
# data["Michael"] = {"years": [], "counts": [], "popularity_pct": []}
data = {}

# Go through every yob file in the folder
for filepath in sorted(glob.glob(os.path.join(folder_path, "yob*.txt"))):
    filename = os.path.basename(filepath)

    # make sure the file is actually one of the year files
    # like yob1880.txt, yob1999.txt, etc.
    if not filename.startswith("yob") or not filename.endswith(".txt"):
        continue

    # pull the year out of the file name
    year = int(filename[3:7])

    # total number of babies in this specific year
    total_births = 0

    # keep track of the counts for the selected names in this year
    year_counts = {name: 0 for name in selected_names}

    # read the file line by line
    with open(filepath, "r") as f:
        for line in f:
            name, sex, count = line.strip().split(",")
            count = int(count)

            # add every name count so we can calculate total births
            total_births += count

            # only save the count if the name and gender match what I selected
            if name in selected_names and sex == selected_names[name]:
                year_counts[name] += count

    # save this year's info into the main data dictionary
    for name, sex in selected_names.items():
        if name not in data:
            data[name] = {
                "years": [],
                "counts": [],
                "popularity_pct": []
            }

        count = year_counts[name]

        # calculate popularity as a percent of total births for that year
        # this is better than just using raw count, since the number of births changes over time
        if total_births > 0:
            pct = (count / total_births) * 100
        else:
            pct = 0

        data[name]["years"].append(year)
        data[name]["counts"].append(count)
        data[name]["popularity_pct"].append(pct)


# set up the figure before plotting all names
plt.figure(figsize=(13, 7))

# print a small summary table in the terminal
print(f"{'Name':<12} {'Latest Count':<15} {'Latest %':<12} {'Growth %':<12} {'Slope':<12} {'Direction'}")
print("-" * 80)

# Analyze each name one at a time
for name, sex in selected_names.items():
    years = np.array(data[name]["years"])
    counts = np.array(data[name]["counts"])
    popularity_pct = np.array(data[name]["popularity_pct"])

    # most recent year of data
    latest_year = years[-1]
    latest_count = counts[-1]
    latest_pct = popularity_pct[-1]

    # calculate 5 year moving average
    # this smooths out random jumps from year to year
    moving_avg_5 = []
    for i in range(len(popularity_pct)):
        if i < 4:
            # not enough previous years yet to make a 5 year average
            moving_avg_5.append(np.nan)
        else:
            avg = np.mean(popularity_pct[i-4:i+1])
            moving_avg_5.append(avg)

    moving_avg_5 = np.array(moving_avg_5)

    # compare the latest popularity to the popularity from 5 years earlier
    if len(popularity_pct) >= 6 and popularity_pct[-6] != 0:
        old_pct = popularity_pct[-6]
        growth_rate = ((latest_pct - old_pct) / old_pct) * 100
    else:
        growth_rate = 0

    # use the most recent 10 years to get a trend line
    # polyfit gives the slope and intercept of a simple linear trend
    recent_window = min(10, len(years))
    recent_years = years[-recent_window:]
    recent_pct = popularity_pct[-recent_window:]

    slope, intercept = np.polyfit(recent_years, recent_pct, 1)

    # decide whether the name is generally increasing, decreasing, or stable
    if slope > 0.001:
        direction = "increasing"
    elif slope < -0.001:
        direction = "decreasing"
    else:
        direction = "stable"

    # Project the next 5 years using the recent slope
    # this is just a simple estimate, not a perfect prediction
    future_years = []
    projected_pct = []

    for i in range(1, 6):
        future_year = latest_year + i
        future_pct = latest_pct + slope * i

        # popularity percent should not go below 0
        if future_pct < 0:
            future_pct = 0

        future_years.append(future_year)
        projected_pct.append(future_pct)

    future_years = np.array(future_years)
    projected_pct = np.array(projected_pct)

    # print the summary stats for this name
    print(f"{name:<12} {latest_count:<15,} {latest_pct:<12.4f} {growth_rate:<+12.2f} {slope:<+12.6f} {direction}")

    # print out each projected year and popularity percent
    print("  Projection:", end=" ")
    for y, p in zip(future_years, projected_pct):
        print(f"{y}={p:.4f}%", end="  ")
    print("\n")

    # plot the actual popularity over time
    line, = plt.plot(years, popularity_pct, linewidth=2, label=f"{name} actual")
    color = line.get_color()

    # plot the moving average on top of the actual data
    plt.plot(
        years,
        moving_avg_5,
        linestyle="--",
        color=color,
        alpha=0.6,
        label=f"{name} 5-year avg"
    )

    # plot the simple 5 year projection
    plt.plot(
        np.concatenate(([latest_year], future_years)),
        np.concatenate(([latest_pct], projected_pct)),
        linestyle=":",
        marker="o",
        color=color,
        label=f"{name} projected"
    )

# add labels and formatting to the graph
plt.title("Name Popularity Over Time With Projection")
plt.xlabel("Year")
plt.ylabel("Popularity Percentage (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# save the graph into the same folder as the dataset
plt.savefig(os.path.join(folder_path, output_file), dpi=220)

# show the graph on screen
plt.show()
