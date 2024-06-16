import feedparser

from datetime import datetime
import time


# convert to integer
def get_last_run():
    try:
        with open("last_run.txt", "r") as fp:
            epoch = fp.read()

        epoch = int(epoch)
        return epoch
    except Exception as e:
        raise e

def get_news_feed():
    try:
        NewsFeed = feedparser.parse("https://jnapolitano.com/index.xml")
        return NewsFeed
    except Exception as e:
        raise e


def convert_to_epoch(given):

    try: 
        # The given date string
        date_str = given

        # Define the format of the date string
        date_format = "%a, %d %b %Y %H:%M:%S %z"

        # Convert the date string to a datetime object
        dt = datetime.strptime(date_str, date_format)

        # Convert the datetime object to a timestamp (epoch time)
        epoch_time = int(dt.timestamp())

        return epoch_time
    except Exception as e:
        raise e

def write_current_dt_to_file(file_name = "last_run.txt"):

    try:
        # Get the current epoch time
        current_epoch_time = int(time.time())

        # Write the current epoch time to the file
        with open(file_name, "w") as file:
            file.write(str(current_epoch_time))
        return True
    except Exception as e:
        raise e



try:
    last_run_epoch = get_last_run()
    NewsFeed = get_news_feed()
   
    for entry in NewsFeed.entries:
        given = entry.published
        # print(given)
        # print(convert_to_epoch(given))
        publish_date_epoch = convert_to_epoch(given)
        if publish_date_epoch > last_run_epoch:
            print(True)
            # in the next pass this will run the social update workflow
    
    # run the write epoch to file function
    result = write_current_dt_to_file()


except Exception as e :
    raise e