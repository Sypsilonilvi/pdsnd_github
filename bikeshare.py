import datetime, time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to enter a city, month, and day to analyze.

Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city_csv = ['chicago', 'washington', 'new york city']
        city = input('Would you like to look at data from Chicago, Washington or New York City? ').lower()

        if city in city_csv:
           print('Great, I''ll get you the data for {}.'.format(city.title()))
           break

        else:
            print('Please enter chicago, washington or new york city as given here.')


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'All']
        month = input('Which month do you want to see? Jan, Feb, ... , Jun or All? ').title()

        if month in months:
            print('Great, I will get you the data for {}.'.format(month))
            break

        else:
            print('Please only enter the first three letters of the chosen month.')


    # TO DO: get user input for day of week (all, Mondayday, Tuesdaysday, ... Sundayday)
    while True:
        days = ['All', 'Monday', 'Tuesdays', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = input('Which day do you want me to show you? Monday, Tuesday, ... , Sunday or All? ').title()

        if day in days:
            print('Great, I''ll get you the data for {}.'.format(day))
            break
        else:
            print('Please enter the weekday as shown above.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #df = df.sort_values(by = 'Start Time')

    if month != 'All':
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    print('The most common travel month was: ',df['month'].mode()[0])
    print()

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    print('The most common travel day was: ',df['day_of_week'].mode()[0])
    print()

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour was: ',df['hour'].mode()[0])
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mcu_sstation = df['Start Station'].mode()[0]
    print ('The start station most commonly used is: ', mcu_sstation)
    print()

    # TO DO: display most commonly used end station
    mcu_estation = df['End Station'].mode()[0]
    print ('The end station most commonly used is: ', mcu_estation)
    print()

    # TO DO: display most frequent combination of start station and end station trip
    df['mcu_combination'] = df['Start Station']+ " + " + df['End Station']
    print('The most common combination of stations is: ', df['mcu_combination'].mode().values[0])
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['time_dif'] = df['End Time'] - df['Start Time']

    time_tot = str(df['time_dif'].sum())
    print('The total travel time of all trips taken was: ',time_tot)
    print()
    # TO DO: display mean travel time

    time_avg = df['time_dif'].mean()
    print('The average travel time is: ',time_avg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    print(df['User Type'].value_counts())
    print()

    # TO DO: Display counts of gender
    if 'Gender'in df:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print('No data regarding gender available.')
    print()

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The oldest customer was born in: ',int(df['Birth Year'].min()))
        print()
        print('The youngest customer was born in: ',int(df['Birth Year'].max()))
        print()
        print('Most customers were born in: ',int(df['Birth Year'].mode()))
    else:
        print('No data regarding birth years available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    """ Asks user if they want to look at more rows of data. """

    view_data = input ('Would you like to view 5 rows of individual trip data? Enter yes or no. ').lower()
    start_loc = 0
    df = df.drop(columns = df.columns[0])

    while True:
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc+10])
            start_loc += 10
            view_display = input("Do you wish to continue?: ").lower()
            if view_display != 'yes':
                print('Okay, I am not going to display more data.')
                break
        else:
            print('Okay, I am not going to display more data.')
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
