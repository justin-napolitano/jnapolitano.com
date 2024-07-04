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

def get_news_feed(feed_url):
    try:
        NewsFeed = feedparser.parse(feed_url)
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
    # keys_i_want = ['author_name','author_email', 'author_id','postid','id','published','title']
    
    out_struct = {
        "author_name": None,
        "author_email": None,
        "author_id": None,
        "postid": None,
        "published": None,
        "title": None
    }

    last_run_epoch = get_last_run()
    NewsFeed = get_news_feed("https://jnapolitano.com/en/posts/index.xml")
   
    for post in NewsFeed.entries:

        try: 
            out_struct['author_name'] = post['author_name']
            out_struct['author_email'] = post['author_email']
            out_struct['author_id'] = post['author_id']
            out_struct['postid'] = post['postid']
            out_struct['published'] = convert_to_epoch(post['published'])
            out_struct['title'] = post['title']
        except Exception as e:
            raise e
        
        print(out_struct)

        ## Write a script to select the given post id
        ## if exists do nothing? Or update. IDK 
        ## if not exists then insert record
        # or drop into an if null.. 
        #somethin glike
        #SELECT IFNULL( (SELECT field1 FROM table WHERE id = 123 LIMIT 1) ,'not found');
        # I'll have to experiment to figure it ou
    # run the write epoch to file function
    result = write_current_dt_to_file()


except Exception as e :
    raise e