import time
import pandas as pd
import numpy as np
import csv

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york city', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_user_input(message, user_list):
    """
    An utility function to obtain user specific input value
    Args:
        (str) message - an information message for a particular request
    Returns:
        (str) user_data - requested data from user
    """

    while True:
        user_data = input(message).lower()
        if user_data in user_list:
            break
        if user_data == 'all':
            break
    
    return user_data


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city do you want to explore? Chicago, New York City or Washington? \n> ').lower()
        if city in CITIES:
           break

    # get user input for month (all, january, february, ... , june)
    month = get_user_input('Okay, Which month? Or \'all\'? \n> ', MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input('Annnnnd which day in week? \n> ', DAYS)

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]
    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)
    print()
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)
    print()
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station:", most_common_start_station)
    print()
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station:", most_common_end_station)
    print()
    most_frequent_start_end = df.groupby(['Start Station', 'End Station'])['Start Time'].count().sort_values(ascending=False).index[0]
    print("The most frequent combination of start station and end station trip: {}, {}".format(most_frequent_start_end[0], most_frequent_start_end[1]))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)
    print()
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))
    print()

    if 'Gender' in df.columns:
        print("Counts of gender:\n")
        gender_counts = df['Gender'].value_counts()
        for index,gender_count   in enumerate(gender_counts):
            print("  {}: {}".format(gender_counts.index[index], gender_count))
        print()

    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        earliest_year = birth_year.min()
        print("The earliest birth year:", earliest_year)
        most_common_year = birth_year.value_counts().idxmax()
        print("The most common birth year:", most_common_year)
        most_recent = birth_year.max()
        print("The most recent birth year:", most_recent)
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(city):
    """
        Displays five lines of raw data if the user specifies that they would like to.
        After displaying five lines, ask the user if they would like to see five more,
        continuing asking until they say stop.
    """

    with open(CITY_DATA[city]) as f:
        reader = csv.reader(f)
        rows = [r for r in reader]
        index = 1
        while True:
            will_see = input('\nWould you like to see some raw data? Enter yes or no.\n').lower()
            if will_see != 'yes':
                break
            for _ in range(5):
                print(rows[index])
                index += 1

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(city)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
