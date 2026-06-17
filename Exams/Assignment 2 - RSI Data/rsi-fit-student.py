import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
path_to_datafile = r'C:\Users\thatt\OneDrive_Personal\OneDrive\Desktop\ENGR315-sp2026-student\data\drop-jump\all_participant_data_rsi.csv'

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

#1.1 load data
df = pd.read_csv(path_to_datafile)

#1.2 get RSI data (Acceleration, Force Plate)
accel_rsi = df['accelerometer_rsi'].dropna()
fp_rsi = df['force_plate_rsi'].dropna()

#1.3 apply normal dist. fit
accel_mu, accel_std = norm.fit(accel_rsi)
fp_mu, fp_std = norm.fit(fp_rsi)

#1.4 report the dist. parameters
print(f'Acceleration: mu: {accel_mu:.4f}, std: {accel_std:.4f}')
print(f'Force Plate: mu: {fp_mu:.4f}, std: {fp_std:.4f}')

#1.5 make x-range (for graph)
x = np.linspace(
    min(accel_rsi.min(), fp_rsi.min()),
    max(accel_rsi.max(), fp_rsi.max()),
    1000
)

#1.6 create prob. dist. func., 
# plots y-values of the normal curve for each X value (from x range)
accel_pdf = norm.pdf(x, accel_mu, accel_std)
fp_pdf = norm.pdf(x, fp_mu, fp_std)

#1.7 make the plot using the x-range and y values established
plt.figure()
plt.plot(x, accel_pdf, label='Acceleration RSI', linestyle='--')
plt.plot(x, fp_pdf, label='Force Plate RSI')

plt.title('Normal Distribution Fit of RSI Data')
plt.xlabel('RSI')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()

#1.8 display plots/graphs
plt.show()

"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

#2.0 make bins, establish alpha as global var
alpha = 0.05

bins_inner = np.linspace(0, 2, 10)
bins = np.concatenate(([-np.inf], bins_inner, [np.inf]))

"""
Acceleration
"""
#2.1a determine how many data pieces are assigned to each bin
accel_observed, _ = np.histogram(accel_rsi, bins=bins)

#2.2a determine how many data pieces SHOULD be in each bin based upon normal dist.
# difference (np.diff) determines probability for data falling between 2 bin edges (2 edges form a bin)
accel_expected_probs = np.diff(norm.cdf(bins, loc=accel_mu, scale=accel_std))
#expected count of a bin = probability of the bin * length data set
accel_expected = len(accel_rsi) * accel_expected_probs

#2.3a chi-square goodness of fit test, compare bin counts to bin predictions
accel_chi2, accel_p = chisquare(f_obs=accel_observed, f_exp=accel_expected)

print('Acceleration:')
print(f'Chi2 Statistic: {accel_chi2:.4f}')
print(f'p-value: {accel_p:.4f}')
#2.4a compare P value to alpha to determine if good fit or not
if accel_p < alpha:
    print('Not a good fit')
else:
    print('Good fit')


"""
Force Plate
"""
#2.1b determine how many data pieces are assigned to each bin
fp_observed, _ = np.histogram(fp_rsi, bins=bins)

#2.2b determine how many data pieces SHOULD be in each bin based upon normal dist.
# difference (np.diff) determines probability for data falling between 2 bin edges (2 edges form a bin)
fp_expected_probs = np.diff(norm.cdf(bins, loc=fp_mu, scale=fp_std))
#expected count of a bin = probability of the bin * length data set
fp_expected = len(fp_rsi) * fp_expected_probs

#2.3b chi-square goodness of fit test, compare bin counts to bin predictions
fp_chi2, fp_p = chisquare(f_obs=fp_observed, f_exp=fp_expected)

print('\nForce Plate:')
print(f'Chi2 Statistic: {fp_chi2:.4f}')
print(f'p-value: {fp_p:.4f}')
#2.4b compare P value to alpha to determine if good fit or not
if fp_p < alpha:
    print('Not a good fit')
else:
    print('Good fit')

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

#3.1 compare the acceleration vs force plate means using two sample t-test
t_stat, p_value = ttest_ind(accel_rsi, fp_rsi)

#3.2 Report p-value for the t-test
print('Two-Sample t-Test Results')
print(f't-statistic: {t_stat:.4f}')
print(f'p-value: {p_value:.4f}')

#3.3 determine whether means are equal or not by comparing p-value to 0.05 (alpha)
#if p < 0.05, then it is assumed the predicted result occurs less than 5% of the time under the null hypothesis, indicating significant difference in means
if p_value < alpha:
    print('Means are significantly different, we cannot say they are equal.')
else:   
    print('Means are not significantly different, we can say they are equal.')

"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

print('\n\n-----Question 4-----')

#4.1 calculate error & fit normal distribution to error data
rsi_error = fp_rsi - accel_rsi
error_mu, error_std = norm.fit(rsi_error)

#4.2 report parameters for clarity
print(f'Error Mean (mu): {error_mu:.4f}')
print(f'Error Std Dev (std): {error_std:.4f}')

#4.3 make x-values for fitted curve
x_error = np.linspace(rsi_error.min(), rsi_error.max(), 1000)

#4.4 make fitted prob. dist. function
error_pdf = norm.pdf(x_error, error_mu, error_std)

#4.5 plot histogram 
#note: (density=True scales histogram more appropriately)
plt.figure()
plt.hist(rsi_error, bins=16, density=True, alpha=0.6, label='RSI Error Histogram')

#4.6 plot fitted normal curve
plt.plot(x_error, error_pdf, linewidth=2, label='Fitted Normal Curve')

#4.7 labels and formatting for plot
plt.title('RSI Error Distribution')
plt.xlabel('Force Plate RSI - Accelerometer RSI')
plt.ylabel('Density')
plt.legend()
plt.grid()

plt.show()