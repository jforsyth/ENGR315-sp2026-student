import sys


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information
    """
    # data point list
    data=[]
    file_name='us-counties.csv'
    file_folder = r'C:\Users\thatt\OneDrive_Personal\OneDrive\Desktop\ENGR315-sp2026-student\Exams\Assignment 1 - COVID Data\\'
    file_path = file_folder + file_name
    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # your code here
    harrisonburg = []
    rockingham = []
    for (date,county, state, fips, cases, deaths) in data:
        if state == 'Virginia' and county == 'Rockingham':
            if cases != 0:
                rockingham.append(date)
        if state == 'Virginia' and county == 'Harrisonburg city':
            if cases != 0:
                harrisonburg.append(date)
    print('First Rockingham COVID case occured:', rockingham[0])
    print('First Harrisonburg COVID case occured:', harrisonburg[0])

    return
    
        

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """
    harrisonburg = []
    rockingham = []

    for (date,county, state, fips, cases, deaths) in data:
        if state == 'Virginia' and county == 'Rockingham':
            rockingham.append((date, cases))
        if state == 'Virginia' and county == 'Harrisonburg city':
            harrisonburg.append((date, cases))

    rockingham_largest_new_cases = 0
    rockingham_largest_date = 0
    rockingham_yesterday_cases = None

    harrisonburg_largest_new_cases = 0
    harrisonburg_largest_date = 0
    harrisonburg_yesterday_cases = None

    for date, cases in rockingham:
        if rockingham_yesterday_cases is not None:
            new_cases = cases - rockingham_yesterday_cases
            if new_cases > rockingham_largest_new_cases:
                rockingham_largest_new_cases = new_cases
                rockingham_largest_date = date
        rockingham_yesterday_cases = cases
    print('The most cases in one day in Rockingham was', rockingham_largest_new_cases, 'which occured on', rockingham_largest_date)
    
    for date, cases in harrisonburg:
        if harrisonburg_yesterday_cases is not None:
            new_cases = cases - harrisonburg_yesterday_cases
            if new_cases > harrisonburg_largest_new_cases:
                harrisonburg_largest_new_cases = new_cases
                harrisonburg_largest_date = date
        harrisonburg_yesterday_cases = cases
    print('The most cases in one day in Harrisonburg was', harrisonburg_largest_new_cases, 'which occured on', harrisonburg_largest_date)

    return



def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    harrisonburg = []
    rockingham = []

    for (date,county, state, fips, cases, deaths) in data:
        if state == 'Virginia' and county == 'Rockingham':
            rockingham.append((date, cases))
        if state == 'Virginia' and county == 'Harrisonburg city':
            harrisonburg.append((date, cases))

    rockingham_new_cases_dated = []
    rockingham_yesterday_cases = None
    harrisonburg_new_cases_dated = []
    harrisonburg_yesterday_cases = None

    for date, cases in rockingham:
        if rockingham_yesterday_cases is not None:
            new_cases = cases - rockingham_yesterday_cases
            rockingham_new_cases_dated.append((date, new_cases))
        rockingham_yesterday_cases = cases
    
    for date, cases in harrisonburg:
        if harrisonburg_yesterday_cases is not None:
            new_cases = cases - harrisonburg_yesterday_cases
            harrisonburg_new_cases_dated.append((date, new_cases))
        harrisonburg_yesterday_cases = cases
    
    rockingham_largest_seven_span = 0
    rockingham_seven_span_start = None
    rockingham_seven_span_end = None
    harrisonburg_largest_seven_span = 0
    harrisonburg_seven_span_start = None
    harrisonburg_seven_span_end = None

    for i in range(len(rockingham_new_cases_dated)-6):
        rockingham_seven_day_span = 0
        for j in range(7):
            rockingham_seven_day_span += rockingham_new_cases_dated[i + j][1]
        if rockingham_seven_day_span > rockingham_largest_seven_span:
            rockingham_largest_seven_span = rockingham_seven_day_span
            rockingham_seven_span_start = rockingham_new_cases_dated[i][0]
            rockingham_seven_span_end = rockingham_new_cases_dated[i+6][0]
    print("The worst 7-day period of COVID cases in Rockingham County occured from",rockingham_seven_span_start," to ",rockingham_seven_span_end,", when ",rockingham_largest_seven_span," cases were recorded.")

    for i in range(len(harrisonburg_new_cases_dated)-6):
        harrisonburg_seven_day_span = 0
        for j in range(7):
            harrisonburg_seven_day_span += harrisonburg_new_cases_dated[i + j][1]
        if harrisonburg_seven_day_span > harrisonburg_largest_seven_span:
            harrisonburg_largest_seven_span = harrisonburg_seven_day_span
            harrisonburg_seven_span_start = harrisonburg_new_cases_dated[i][0]
            harrisonburg_seven_span_end = harrisonburg_new_cases_dated[i+6][0]
    print("The worst 7-day period of COVID cases in Harrisonburg occured from",harrisonburg_seven_span_start," to ",harrisonburg_seven_span_end,", when ",harrisonburg_largest_seven_span," cases were recorded.")

    return



if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

    #for (date,county, state, fips, cases, deaths) in data:
        #print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)


