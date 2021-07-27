# yp-review-grabber
A scrapping tool to help mining data for nlp summer class

# Dependencies
- Pandas
- bs4 (BeautifulSoup)

# Parameters
- -s (required) specify the starting index. <b>Note: I use index starts from 0</b>
- -e (optional) specify the starting index. if not specified, it will run all the way to the end
- -n (optional) specify the number of businesses in a batch. default is 5, the program will output each batch as a csv, and keep going until the end_index is reached
- -t (optional) specify the time interval between requests to avoid band (default=60)
- -w (optional) specify the wait time between each batch, you can set this just to be safe (defult=0)
- -f (optional) the file path to read the business list file (need to be converted to csv), by default, it reads the SBRC_Doctor_Reviews.csv from the same folder as the program
- -p (optional) if using proxy, specify the proxy and port, e.g 1.1.1.1🈵

# Example
python yelp_review_grabber.py -s 100 -e 200 -n 10 -t 40 -p 192.168.1.100:80  
- above code will scrap the busniess from index 100 to 200, and generate csv as 100-109.csv, 110-119.csv, 120-129.csv, .... , 190-200.csv
- the interaval is set to 40 +/- 5 seconds between requests
- each csv contains 10 business (-n 10)
- proxy 192.168.1.100:80 will be used, if you dont use proxy, just don't set -p
- when finish, an error log will be also generated and list all the businesses which didn't scrapped properly so we can deal with later case by case

# Options to be add..
scrap specific buinsess  
