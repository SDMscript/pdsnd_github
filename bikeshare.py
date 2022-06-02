import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("enter the name of the city: ").lower()
        if not city in CITY_DATA:
            print('Sorry no data for that city.')
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all','january','february', 'march', 'april', 'may','june','july','august','september','october','november','december']
    while True:
        month = input("enter the month to explore. Enter 'all' for all months: ").lower()
        if not month in months:
            print('Please enter a valid month.')
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ('all','monday', 'tuesday','wednesday','thursday','friday','saturday','sunday')
    while True:
         day = input("enter the day of the week to explore. Enter 'all' for all days: ").lower()
         if not day in days:
            print('Please enter a valid day of the week.')
         else:
            break
    

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
    months = ['all','january','february', 'march', 'april', 'may','june','july','august','september','october','november','december']
    month_number=months.index(month)
    open_df = pd.read_csv(CITY_DATA[city])
    open_df['Start Time'] = pd.to_datetime(open_df['Start Time'])
    open_df['month']=open_df['Start Time'].dt.month
          
    open_df['day_of_week']=open_df['Start Time'].dt.day_name()
    
    if month != 'all':
        try:
            month_df = open_df.loc[open_df['month']==month_number]
        except KeyError:
            print('\nNo information for this month.')
    elif month == 'all':
        month_df=open_df    
    if day != 'all':
        try:
            df = month_df.loc[month_df['day_of_week']==day.title()]
        except KeyError:
             print('\nNo information for this month {} and day of the week {}.'.format(month,day))
    elif day == 'all':
        df = month_df

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\n The most common month is: ', df['month'].mode()[0])

    # TO DO: display the most common day of week
    print('\n The most common day of the week is: ',df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    print('\n The most common start hour is: ',df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nThe most commonly used start station is:',  df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('\nThe most commonly used end station is:',  df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('\nThe most common combination of start and end station trips are:',df.groupby(['Start Station', 'End Station']).size().idxmax()[0], 'and', df.groupby(['Start Station', 'End Station']).size().idxmax()[1])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('\nTotal travel time is:', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('\nMean travel time is:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_users = df.groupby('User Type').size()
    user_groups =counts_users.keys()
    
    print('\nCounts for user types are:')
    for users in user_groups:
        print(users, counts_users[users])

    # TO DO: Display counts of gender
   
    if 'Gender' in df:
            counts_genders = df.groupby('Gender').size()
            user_gender =counts_genders.keys()
            print('\nCounts for user genders are:')
            for gender in user_gender:
                print(gender, counts_genders[gender])
    else:
        print('\nNo Gender information available for bikeshare users in this city.')


    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
            print('\nOldest year of birth is:', int(df['Birth Year'].min()), 'The youngest birth year is:', int(df['Birth Year'].max()), 'and most common year of birth is:', int(df['Birth Year'].mode()[0]))
        
    except KeyError:
        print('\nNo birth year information available for bikeshare users in this city.')
        
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data != 'yes':
            break
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.shape[0] != 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)
            
        else:
            print('\nNo information for this combination of month and day of the week: {}, {}.'.format(month.title(), day.title()))
            break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
