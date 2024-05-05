import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = " "
    month = " "
    day = " "
    answer = " "

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        try:
            city = input("Would you like to see data for Chicago, New York or Washington? \n").lower()
            if city == 'new york':
                city = 'new york city'
        except:
            city = " "     


    # get user input for month (all, january, february, ... , june)
    while answer != 'yes' and answer != 'no':
        try:
            answer = input("Would you like to filter by month? \n").lower()
            if answer == 'no':
                month = 'all'
        except:
            answer = " "    

    while month not in months and month != 'all':  
        try: 
            month = input("Enter the month by which you want to filter (January, February, March, April, May or June): \n").lower()
        except:
            month = " "

    answer = ' '
    while answer != 'yes' and answer != 'no':
        try:
            answer = input("Would you like to filter by weekday? \n").lower()
            if answer == 'no':
                day = 'all'
        except:
            answer = " "  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days and day != 'all':   
        try:
            day = input("Enter the day of the week by which you want to filter: ").lower()
        except:
            day = " "
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day where applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing raw city data 
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['start_hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month].reset_index(drop=True)
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day.lower())
        df = df[df['day_of_week'] == day].reset_index(drop=True)

    
    return df




def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (pandas.DataFrame) df - contains city data filtered by month and day
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        none   
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        common_month = df['month'].mode()[0]
        print('The most popular month was {}'.format(months[common_month - 1].title()))
        print()

    # display the most common day of week
    if day == 'all':    
        common_dow = df['day_of_week'].mode()[0]
        print('The most popular day of the week was {}'.format(days[common_dow - 1].title()))
        print()

    # display the most common start hour
    common_sthour = df['start_hour'].mode()[0]
    print('The most popular start hour was {}'.format(common_sthour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (pandas.DataFrame) df - contains city data filtered by month and day

    Returns:
        none     
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_ststation = df['Start Station'].mode()[0]
    print('The most popular start station was {}'.format(common_ststation))
    #print()

    # display most commonly used end station
    common_endstation = df['End Station'].mode()[0]
    print('\nThe most popular end station was {}'.format(common_endstation))
    #print()

    # display most frequent combination of start station and end station trip
    common_route = df['trip'].mode()[0]
    print('\nThe most frequent trip from start to end was {}'.format(common_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (pandas.DataFrame) df - contains city data filtered by month and day

    Returns:
        none    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum().round(1)
    print('The total travel time was {} seconds.'.format(str(total_time)))
    print()

    # display mean travel time
    mean_time = df['Trip Duration'].mean().round(1)
    print('The average travel time was {} seconds.'.format(str(mean_time)))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        (pandas.DataFrame) df - contains city data filtered by month and day
        (str) city - name of the city to analyze

    Returns:
        none  
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utype_count = df['User Type'].value_counts()
    print('The breakdown of different user types was ')
    print(utype_count)
    print()


    if city != "washington":
    # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('The breakdown of users by gender is ')
        print(gender_count)
        print()


    # Display earliest, most recent, and most common year of birth
        min_birth_year = df['Birth Year'].min()
        print('The oldest subscriber was born in {}'.format(str(int(min_birth_year))))
        print()
        max_birth_year = df['Birth Year'].max()
        print('The youngest subscriber was born in {}'.format(str(int(max_birth_year))))
        print()
        mode_birth_year = df['Birth Year'].mode()[0]
        print('Subscribers were most commonly born in {}'.format(str(int(mode_birth_year))))

    else:
        print("No gender and birth year information is available for {}.".format(city.title())) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    answer = " "
    derived_columns = ['month', 'day_of_week', 'start_hour', 'trip']

    while answer != 'yes' and answer != 'no':
        try:
            answer = input("Would you like to see some raw data? \n").lower()
        except:
            answer = " "   

    if answer == 'yes':
        n = 5
        i = 0

        while True:
            print()
            while i < n and i < len(df):
                for col in df.columns:
                    if col not in derived_columns:
                        print("{}: {}".format(col, str(df[col][i])))
                i += 1
                print()
            if i < len(df):        
                more = input("\nWould you like to see more raw data? Yes or no \n")    
                if more.lower() != 'yes':
                    break
                else:
                    n += 5



def main():
    """
    Main function of the program.

    1. Retrieves user input to determine filters for data
    2. Loads data from file
    3. Calculates statistics from data
    4. Gives the option to display raw data

    Args:
        None

    Returns:
        None

    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        print("\nThe data above is a summary of bikeshare data for {}.".format(city.title()))
        if month != 'all':
            if day != 'all':
                print("\nThe data was filtered by month {} and weekday {}.".format(month.title(), day.title()))
            else:
                print("\nThe data was filtered by month {}.".format(month.title()))
        elif day != 'all':
            print("\nThe data was filtered by weekday {}.".format(day.title()))            

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()