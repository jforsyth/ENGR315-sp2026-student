# Baby Name Project

## Project Description

This project analyzes baby name data from the Social Security Administration. The goal is to look at how baby names change over time using Python graphs and basic calculations.

The project focuses on name popularity, name decline after peak popularity, name diversity, and simple future trend estimates.

## Dataset

**Dataset Name:** Baby Names from Social Security Card Applications - National Data  
**Source:** Social Security Administration

The dataset is split into yearly text files.

Example file names:

```text
yob1880.txt
yob1881.txt
yob1882.txt
```

Each file contains:

```text
Name, Sex, Count
```

Example row:

```text
Mary,F,7065
```

## Research Questions

1. How do individual baby names rise, peak, and decline over time?
2. How has baby name diversity changed over time?
3. What does past trend data suggest about a name’s future popularity?

## Tools Used

```text
Python
os
glob
numpy
pandas
matplotlib
```



## Source Code Files

### patterns.py

This script analyzes selected names and finds:

```text
Peak year
Peak count
50% decline year
Years to 50% decline
Decline rate per year
```

It also creates a line graph of each name’s popularity over time.

### diversity.py

This script measures name diversity by calculating the percentage of births made up by the top 10 names each year.

It finds:

```text
Least diverse year
Most diverse year
Overall change
Average top 10 share by decade
```

It also creates a graph showing the top 10 name share over time.

### prediction.py

This script uses recent name popularity trends to estimate future popularity.

It finds:

```text
Latest count
Latest popularity percentage
Growth rate
Trend slope
Direction
5 year projection
```

It also creates a graph with actual popularity, moving average, and projected popularity.

## How to Run

1. Download the baby name dataset.
2. Put the `yobYYYY.txt` files in one folder.
3. Open each Python file.
4. Update the `folder_path` variable.

```python
folder_path = r"C:\Users\phili\OneDrive\Desktop\CS Project\names (1)"
```

5. Run the scripts.


## Output

The scripts print results in the terminal and create graphs using Matplotlib.


## Main Results

The analysis showed that baby names have become more diverse over time. The top 10 names made up a much larger share of births in the past than they do today.

The analysis also showed that different names decline at different speeds. Some names stayed popular for many years after their peak, while others declined much faster.

The future projection script showed that the selected names were mostly trending downward based on recent data.

## Notes

The projection is a basic estimate. It uses recent trends and does not account for outside events like celebrities, movies, social media, or cultural changes.
