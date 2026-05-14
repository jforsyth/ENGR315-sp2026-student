import sys


def parse_nyt_data(file_path='./us-counties.csv'):
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
    print("QUESTION 1:")
    for (date,county, state, fips, cases, deaths) in data:
        if county == 'Rockingham' and state == 'Virginia':
            print("The first positive COVID case in Rockingham County was on " + date)
            break
    for (date,county, state, fips, cases, deaths) in data:
        if county == 'Harrisonburg city' and state == 'Virginia':
            print("The first positive COVID case in Harrisonburg was on " + date)
            break   

    # your code here
    return

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """
    print("QUESTION 2:")
    highestCasesHarrisonburg=0;
    prevCasesHarrisonburg=0;
    highestCasesRockingham=0;
    prevCasesRockingham=0;
    for (date,county, state, fips, cases, deaths) in data:
        if county == 'Harrisonburg city' and state == 'Virginia':
            if (cases - prevCasesHarrisonburg) > highestCasesHarrisonburg:
                highestCasesHarrisonburg = cases - prevCasesHarrisonburg
                dateWithMostCasesHarrisonburg = date
            prevCasesHarrisonburg = cases

            
    print("The day with the greatest number of new daily cases recorded in Harrisonburg was on " + dateWithMostCasesHarrisonburg)
    
    for (date,county, state, fips, cases, deaths) in data:
        if county == 'Rockingham' and state == 'Virginia':
            if (cases - prevCasesRockingham) > highestCasesRockingham:
                highestCasesRockingham = cases - prevCasesRockingham
                dateWithMostCasesRockingham = date
            prevCasesRockingham = cases
    print("The day with the greatest number of new daily cases recorded in Rockingham County was on " + dateWithMostCasesRockingham)
    

    # your code here
    return

def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    print("QUESTION 3:")
    highestCasesHarrisonburg=0;
    prevCasesHarrisonburg=0;

    highestCasesRockingham=0;
    prevCasesRockingham=0;
    prev7=0; prev6=0; prev5=0; prev4=0; prev3=0; prev2=0; prev1=0;
    date6DaysAgo=None; date5DaysAgo=None; date4DaysAgo=None; date3DaysAgo=None; date2DaysAgo=None; date1DayAgo=None;
    for (date,county, state, fips, cases, deaths) in data:
        if county == 'Harrisonburg city' and state == 'Virginia':
            if (cases - prev7) > highestCasesHarrisonburg:
                highestCasesHarrisonburg = int(cases) - int(prev7)
                dateWithMostCasesHarrisonburg = date
                startDateWithMostCasesHarrisonburg = date6DaysAgo;
            prev7 = prev6; prev6= prev5; prev5= prev4; prev4= prev3; prev3= prev2; prev2= prev1; prev1= cases
            date6DaysAgo= date5DaysAgo; date5DaysAgo= date4DaysAgo; date4DaysAgo= date3DaysAgo; date3DaysAgo= date2DaysAgo; date2DaysAgo= date1DayAgo; date1DayAgo= date
        
            
    print("The worst 7-day period in Harrisonburg City for new COVID cases was from "  + startDateWithMostCasesHarrisonburg + " to " + dateWithMostCasesHarrisonburg + " with " + str(highestCasesHarrisonburg) + " cases")
    
    prev7=0; prev6=0; prev5=0; prev4=0; prev3=0; prev2=0; prev1=0;
    date6DaysAgo=None; date5DaysAgo=None; date4DaysAgo=None; date3DaysAgo=None; date2DaysAgo=None; date1DayAgo=None;
    for (date,county, state, fips, cases, deaths) in data:
        if county == 'Rockingham' and state == 'Virginia':
            if (cases - prev7) > highestCasesRockingham:
                highestCasesRockingham = int(cases) - int(prev7)
                dateWithMostCasesRockingham = date
                startDateWithMostCasesRockingham = date6DaysAgo;
            prev7 = prev6; prev6= prev5; prev5= prev4; prev4= prev3; prev3= prev2; prev2= prev1; prev1= cases
            date6DaysAgo= date5DaysAgo; date5DaysAgo= date4DaysAgo; date4DaysAgo= date3DaysAgo; date3DaysAgo= date2DaysAgo; date2DaysAgo= date1DayAgo; date1DayAgo= date
        
    print("The worst 7-day period in Rockingham County for new COVID cases was from "  + startDateWithMostCasesRockingham + " to " + dateWithMostCasesRockingham + " with " + str(highestCasesRockingham) + " cases")    

    return

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

  #  for (date,county, state, fips, cases, deaths) in data:
  #      print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


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
