import time
import pandas as pd

# Dictionary to translate user city choice to respective file name
CITY_DATA = {"chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv"}

# Lists to check validity of user inputs
month_list = ["january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "all"]

day_list = ["monday",
          "tuesday",
          "wednesday",
          "thursday",
          "friday",
          "saturday",
          "sunday",
          "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")
    # Get user input for city (chicago, new york city, washington)
    # Uses a while loop to handle invalid inputs and uses dictionaries/lists for input checks and error handler
    while True:
        try:
            city = input("\nPlease choose Chicago, New York City or Washington for analysis:\n").lower()
            if city in CITY_DATA.keys():
                print("You chose {}!".format(city.title()))
                break
            else:
                print("That is not a valid input. Please choose a city.")
        except:
            print("That is not a valid input. Please choose a city.")

    # Get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("\nPlease choose a month from January to June or all for analysis (full name):\n").lower()
            if month in month_list:
                print("You chose {}!".format(month.title()))
                break
            else:
                print("That is not a valid input. Please choose a month.")
        except:
            print("That is not a valid input. Please choose a month.")

    # Get user input for day of week (all, monday, tuesday, ... , sunday)
    while True:
        try:
            day = input("\nPlease choose a weekday from Monday to Sunday or all for analysis (full name):\n").lower()
            if day in day_list:
                print("You chose {}!".format(day.title()))
                break
            else:
                print("That is not a valid input. Please choose a weekday.")
        except:
            print("That is not a valid input. Please choose a weekday.")

    print("-"*40)
    return city, month, day


def load_data(city, month, day,):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Choose input source based on user input using CITY_DATA dictionary and remove csv index column
    df = pd.read_csv(CITY_DATA.get(city))
    df.drop(df.columns[0],axis=1,inplace=True)

    # Convert Time columns to datetime format for further analysis
    df["Start Time_adj"] = pd.to_datetime(df["Start Time"], format="%Y-%m-%d %H:%M:%S")
    df["End Time_adj"] = pd.to_datetime(df["End Time"], format="%Y-%m-%d %H:%M:%S")

    #Create column with month (month_name is called method and not attribute, therefore () needed)
    df["Start Time_month"] = df["Start Time_adj"].dt.month_name()

    # Create column with weekday
    df["Start Time_weekday"] = df["Start Time_adj"].dt.weekday_name

    # Create column with start hour
    df["Start Time_hour"] = df["Start Time_adj"].dt.hour

    # Create columns with travel time as it is nicer to use than the existing trip duration column
    df["Travel Time"] = df["End Time_adj"] - df["Start Time_adj"]

    # Create columns with start/end station combo and use a series with a string as filler between the stations
    df["Insert"] = " to "
    df["Start/End Stations"] = df["Start Station"] + df["Insert"] + df["End Station"]

    # Filter dataframe based on user inputs
    if month != "all":
        df = df[df["Start Time_month"] == month.title()]
    if day !="all":
        df = df[df["Start Time_weekday"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Display the most common month
    print("\nMost common month:\n", df["Start Time_month"].mode()[0])

    # Display the most common day of week
    print("\nMost common weekday:\n", df["Start Time_weekday"].mode()[0])

    # Display the most common start hour
    print("\nMost common start hour:\n", df["Start Time_hour"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    print("\nMost commonly used start station:\n", df["Start Station"].mode()[0])

    # Display most commonly used end station
    print("\nMost commonly used end station:\n", df["End Station"].mode()[0])

    # Display most frequent combination of start station and end station trip
    print("\nMost frequent trips:\n", df["Start/End Stations"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    print("\nTotal travel time:\n", df["Travel Time"].sum())

    # Display mean travel time
    print("\nMean travel time:\n", df["Travel Time"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    print("\nUsers by type:\n", df["User Type"].value_counts())

    # Display counts of gender --> BEWARE: MISSING SOMETIMES
    try:
        print("\nUsers by gender:\n", df["Gender"].value_counts())
    except:
        print("\nNo data available in this city\n")

    # Display earliest, most recent, and most common year of birth --> BEWARE: MISSING SOMETIMES
    try:
        print("\nOldest customers born in:\n", df["Birth Year"].min().astype('int64'))
        print("\nYoungest customers born in:\n", df["Birth Year"].max().astype('int64'))
        print("\nMost common year of birth:\n", df["Birth Year"].mode()[0].astype('int64'))
    except:
        print("\nNo data available in this city\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Raw data is displayed upon request by the user in this manner: Script should prompt the user if they want
        # to see 5 lines of raw data, display that data if the answer is 'yes', and continue these prompts and displays
        # until the user says 'no'.
        add_info = input("\nWould you like to see descriptive statistics and data example? Enter yes or no.\n")
        if add_info.lower() == "yes":
            print(df.describe())
            print()
            print(df.head())

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
	main()
