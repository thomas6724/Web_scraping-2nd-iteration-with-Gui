from urllib.request import urlopen as url_req
from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import *
import pandas as pd
import constants
import time
import sys
import os
import re


def search():
    run()


def introduction():
    """
    Sends out a line of print statements set at intervals introducing the user to the web-scraper.
    """
    intro = Label(main_window, text="Hello, welcome to the Newegg.com web-scraper! Using this web-scraper you can\n"
                                    "search up your favourite products, getting real time data. For your convenience\n"
                                    "we have gone ahead and created some optional category's for you to try. But\n"
                                    "don't feel hindered. You can search up whatever you want! Some possible\n"
                                    "category's include but are not limited to - Graphics cards, Ram, PC cases and\n"
                                    "storage.", borderwidth=10, bd=3, relief='sunken', justify='left')
    intro.grid(row=0, rowspan=4, column=2, pady=20)


def input_code():
    """
    Takes input from the user, validates input and turns it into something usable for the end of a link.

    Returns
    -------
    user_search : str
        Takes user_input and replaces specific keystrokes with symbols turning the
        return into a form that works with links.
    user_input : str
        Takes input from the user.

    Raises
    ------
    ValueError
        Raises error verifying the user has only entered text.

    Notes
    -----
    os.system('cls') will only work on windows. If using a mac please change this line to os.system('clear')
    """
    while True:
        # clears the console on windows when not using pycharm

        user_input = input_test.get()
        os.system('cls')

        try:
            # checks to see if there is a number in input
            input_nospace = user_input.replace(" ", "")
            print(input_nospace)
            _ = int(input_nospace)

        # checks to see if the user has entered no numbers
        # accepts input
        except ValueError:
            pass
        else:
            print("Please do not enter numbers!")
            break

        # SPELL is a constant
        # changes the user input into something url appropriate
        # checks if there is a spelling mistake in the input
        user_search = user_input.replace(' ', '+')
        misspelled = constants.SPELL.unknown(user_input.split())

        # checks if the user has typed anything
        # does not accept single letters or symbols or simply spaces
        # checks the input for character length
        # does not accept more than 30 characters
        if len(user_input.strip()) <= 1 or len(user_input.strip()) >= 30:
            print("Please put in a valid input!")
            errormessage1 = Label(main_window, text="Please enter a valid message", fg='red')
            errormessage1.grid(row=1, column=0)
            break

        # checks the input for word count
        # does not accept more than 4 words
        elif len(user_input.split()) > 4:
            print("Please type no more than 4 words")
            break

        # checks to see if there is a typo in a word
        # if there isn't it accepts the input
        elif misspelled == set():
            print("Searching newegg.com for " + user_input)

            # returns the input and search from the def
            return [user_search, user_input]

        # picks up all typos/ non english words and symbols
        else:
            print("Please enter a word in the english dictionary. \nThe word '" + user_input + "' is not valid")
            break


def timer(timer_var):
    """
    A countdown per second to 0, whilst printing the seconds.

    parameters
    ----------
    timer_var : int, necessary
        Allows programmer to set different int values to start the countdown.
    """
    while True:
        # wait one second
        # minus one second off
        # repeat unless timer has reached 0
        time.sleep(1)
        timer_var = timer_var - 1
        print(timer_var)
        if timer_var == 0:
            break
        else:
            continue


def remove_letters(test_str):
    """
    Code that takes all values except integers and "." then removes them.
    Used for cleaning the price section of data.

    Returns
    -------
    ret: str
        returns price without additional commenting
    """

    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '(':
            skip2c += 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret


def web_scraper():
    """
    Code that inputs your search into newegg.com search algorithm and then reads the results of said search.
    Further reads and writes the search results to a file.

    Returns
    -------
    file_name: str
        Returns the name of the CSV file that has been written to.

    Raises
    ------
    ValueError
        Input is not compatible.
    IndexError
        Raised when a list doesnt exist. Raised when the web-scraper finds no search results and
        cannot create a list. Prompts user to search something else after a cool-down period.
    KeyError
        Raised when the script cannot find a keyword in the html. excepts to either writing "none"
        in results or prompts you to search again
    AttributeError
        An attribute doesnt exist. Raised when code cant find an attribute in the html. Skips over
        said html and writes "none" in the CSV file. Continues the scraper onto the next item in list.
    PermissionError
        Caused when the CSV file trying to be write is open. Prompts user to close said file and
        restart code

    Notes
    -----
    Script will not work in some external programs where web-scraping is against terms and
    conditions for example, repl.it.
    """
    try:
        while True:
            # running user input loop
            # saving input_code() into a list
            # splitting the user_input into two variables
            user_input = input_code()
            try:
                user_url = user_input[0]
                user_search = user_input[1]
            except TypeError:
                break

            # URl to web scrap from.
            # LINK is a constant
            # Default URL search link + users search input
            url = constants.LINK + user_url + "&PageSize=96"

            # opens the connection and downloads html page from url
            uClient = url_req(url)

            # parses html into a soup data structure to traverse html
            # as if it were a json data type.
            # putting it inside a variable to prevent the whole code crashing
            page_html = uClient.read()
            uClient.close()

            # parses html into a soup data structure to traverse html
            # as if it were a json data type.
            page_soup = soup(page_html, "html.parser")

            # finds all of the containers on neweggs html doc
            # Grabs each product on the page
            containers = page_soup.findAll("div", {"class": "item-container"})

            # creating a loop that detects containers
            try:
                # creating variable container so I can loop through the containers within neweggs html file
                # exiting the list if variable is made
                container = containers[0]
                break

            # If can't find any containers two errors occur as a list cannot be created
            # and then as a specific word cant be found
            # No search results creates said errors
            # Sending the user back to input
            except (ValueError, IndexError):
                print("I'm sorry. There are no search results for '" + user_search + "'. \nPlease wait 10 seconds "
                                                                                     "before "
                                                                                     "searching again to prevent "
                                                                                     "excessive traffic")
                # timer counting down from 10seconds before restarting the input loop
                timer(11)
                continue

        # try/ except function detecting whether or not the CSV file is currently in use
        try:
            # the CSV files name
            # opening the CSV file allowing us to write
            file_name = "products.csv"
            file = open(file_name, "w")

            # if CSV file is open show print statement
        except PermissionError:
            print("Please close the CSV file and then run the program again.")

            # stopping the program
            sys.exit()

        # naming the headers to write to the CSV file
        headers = "Brand,Product name,Price,Original price,Rating,Additional promotions\n"

        # writing the headers to the CSV file
        file.write(headers)

        # creating the loop
        # loop adds to container[] list as it goes through all of the containers on the webpage
        # once all containers in neweggs html file have been recorded the loop will break
        for container in containers:

            # try/ except command used to allow the code to skip over
            # any missing index's (IndexError), or words (KeyError) in neweggs html file
            try:
                rating_container = container.findAll("a", {"class": "item-rating"})
                rating = str(rating_container[0]["title"])
                rating = [int(s) for s in rating.split() if s.isdigit()]
            except (IndexError, KeyError):

                # if there isn't a word in neweggs html file, specifically title under the dictated directory - skips rating
                # if there isn't an index that is in reach or rating on a product, writing 'none' in the ratings place
                # writing 'none' in the ratings place
                rating = "none"

            # try/ except command used to allow the code to skip over any missing index's in neweggs html file
            try:
                # scraping newegg.com for a products original price
                origin_price_container = container.findAll("li", {"class": "price-was"})
                origin_price = origin_price_container[0].text
            except IndexError:

                # if there isn't an index that is in reach or original price on a product,
                # writing 'none' in the original price's place
                origin_price = "none"

            # try/ except command used to allow the code to skip over any missing words in neweggs html file
            try:
                # scraping newegg.com for a products price
                model = container.img["alt"]
            except KeyError:

                # if there isn't a word in neweggs html file, specifically alt under the dictated directory - skips
                # model writing 'none' in the models place
                model = "none"

            # try/ except command used to allow the code to skip over any missing index's in neweggs html file
            try:
                # scraping newegg.com for a products price
                price_container = container.findAll("li", {"class": "price-current"})
                price = price_container[0].text

                # Removing all letters, symbols and spaces allowing Pandas to clean information scraped
                price = remove_letters(price)
                price = re.sub('[^0-9.]', '', price)

            except IndexError:

                # if there isn't an index that is in reach or price on a product, writing 'none' in the price's place
                price = "none"

            # try/ except command used to allow the code to skip over any missing index's in neweggs html file
            try:
                # scraping newegg.com for a products brand name
                brand_container = container.findAll("a", {"class": "item-brand"})
                brand = brand_container[0].img["alt"]
            except IndexError:

                # if there isn't an attribute or rating on a product, writing 'none' in the brands place
                brand = "none"

            # try/ except command used to allow the code to skip over any missing attributes in neweggs html file
            try:
                # scraping newegg.com for a products rating out of 5
                promotion = container.div.p.text
            except AttributeError:

                # if there isn't an attribute or promotion on a product, writing 'none' in the ratings place
                promotion = "none"

            # writing the results of the web-scraper to the CSV file, as it loops around until it reaches the bottom of
            # the list/ last container on the page
            file.write(str(brand) + "," + str(model.replace(",", "|")) + "," + str(price) + "," + str(origin_price) +
                       "$USD," + str(rating) + "/[5]," + str(promotion.replace(",", "-")) + "\n")

        # closing the CSV file to allow user to open it
        file.close()

        # showing data display option button in gui
        save_selection.grid(row=3, column=1)

        # showing dropdown menu allowing user to pick how to view data
        drop.grid(row=3, column=0)

        return [file_name]
    except Exception:
        pass


def run():
    """
    Def to run the program.
    """
    filename = web_scraper()
    if filename != None:
        # running function introduction
        # introduction()

        # running function web_scraper
        # retrieving filename
        print(
            "Search finished! Thank you for using the newegg.com web-scraper. \nYour results have been written to a "
            "CSV "
            "file! \nYour CSV file is called " + str(filename) + "! Your file directory is: \n" + os.getcwd() +
            "\\products.csv")
    else:
        pass


def cleaning():
    """
    Def which reads webscraped information. Then sorts said information into a nicer format to read
    interms of ordering information

    Returns
    -------
    df:str
        Csv file information of webscraped information

    Raises
    ------
    Exception(1)
        Cannot find value
    Exception(2)
        Cannot read file
    """
    try:
        # reading file "poducts.csv"
        # preventing Pandas error bad_lines
        # removes bad_lines when opened allowing file to be used if bad
        df = pd.read_csv('products.csv', error_bad_lines=False)

        # cleaning CSV file, organising rows by Brand name (A-Z), then price (Low to high)
        df = df.sort_values(['Brand', 'Price'], ascending=[1, 1])

        # Resetting index allowing data to be pulled and ordered when indexing
        df = df.reset_index()

        # saving dataframe as a new csv file
        df.to_csv('new.csv')

        # creating a counting variable for indexing
        position = 0

        # Creating an empty list ready to collect all brands found in search result
        brandsList = []

        # creating loop to run through index catching all str in column Brand
        # then adding them to brandsList variable so that they can be called
        # and located using pandas
        while True:
            try:
                # using indexing to locate the name of the brand at position
                brandName = df.iloc[position, 1]

                # adding the brand name to the brandsList
                brandsList.append(brandName)

                # increasing the index value by one heading down to the next row
                position = position + 1

            except Exception:
                # once all values in document have been added stop the loop
                break

        # Removing and doubled up brands
        # Showing all of the various brands in the scraping
        brandsList = list(set(brandsList))

        # Creating a new variable with just information about
        # first brand in list separating said brand
        # allowing for closer inspection of data
        new_df = df.loc[(df['Brand'] == brandsList[0])]

        # Creating graph titled "Brand --Name of brand-- price guide"
        plt.title("Brand " + brandsList[0] + "s price guide:")

        # Plotting information on graph and creating a dot plot
        # Creating z-axis Product names, and y axis price under one specific brand
        plt.plot(new_df['Product name'], new_df.Price, 'o')

        # returning str df and new_df
        return [df, new_df]
    except Exception:
        # If file cannot be read whole cleaning stage is skipped to avoid crash
        pass


def work():
    """
    When button in Gui is pressed, it takes the drop down menu input and expresses the data in
    spread sheet form or graph form (Visualised)
    """

    # If drop down menu is on Visualise data do the following
    if clicked.get() == "Visualise Data":

        print("Do something")

    # If dropdown menu displays show all
    elif clicked.get() == "Show all":

        # run function cleaning
        cleaning()

        # Display spread sheet data at the following location
        my_frame.grid(row=5, column=0, columnspan=3)

        '''
        txt = Text(main_window, width=120)
        txt.grid(row=5, column=0, columnspan=3)
        txt.insert(0.0, datafile[0])
        '''

        # Open CSV file
        file_open()
    else:
        # If nothing is selected do nothing (pass)
        pass


def file_open():
    """
    Gets file name of CSV file and then reads file, attaches it to gui and displays it in
    spreadsheet form.

    Raises
    ------
    FileNotFoundError
        Cannot find file under file path
    """

    # Creating a variable containing CSV file name
    filename = 'new.csv'

    # If file name can be read, read file
    if filename[0]:
        try:

            # putting all information on CSV file under variable df (Dataframe)
            df = pd.read_csv(filename)

        # if file cannot be read display File cannot be found
        except FileNotFoundError:
            my_label.config(text="File could not be found.")

    # if file is changed, clear previous file information
    cleartree()

    # The spreadsheet columns are...
    my_tree["column"] = list(df.columns)

    # Shows headings
    my_tree["show"] = "headings"

    # For each column, create heading
    for column in my_tree['column']:
        my_tree.heading(column, text=column)

    # converting rows in Dataframe to a list
    # storing listed rows in df_rows
    df_rows = df.to_numpy().tolist()

    # For each row in listed Dataframe list them under one another
    for row in df_rows:
        my_tree.insert("", "end", values=row)

    # Display Spreadsheet
    my_tree.grid(row=8, column=0)


def cleartree():
    """
    Deletes all information in variable allowing document to be changed
    """
    my_tree.delete(*my_tree.get_children())


# opens gui
main_window = Tk()  

# Creates text input bar
input_test = Entry(main_window, width=50, borderwidth=5)

# Places input bar into correct row and column
input_test.grid(row=0, column=0)

# Displays (Type something to search) in input bar
input_test.insert(0, "Type something to search...")

# Frame for CSV file
my_frame = Frame(main_window)

# Creates tree within frame
my_tree = ttk.Treeview(my_frame)

# Displays Label for Tree
my_label = Label(main_window, text='')

# Putting returned values in clicked (DDM)
clicked = StringVar()

# Making drop down menu display (Select) as defult
clicked.set("Select")

# Creating display options for drop down menu
drop = OptionMenu(main_window, clicked, "Select", "Visualise Data", "Show all")

#
save_selection = Button(main_window, text="Save selection", command=work)


def gui():
    main_window.title("NewEgg webscraper")
    searchbutton = Button(main_window, text="Search", command=search)
    searchbutton.grid(row=0, column=1, padx=10, pady=10)


gui()
introduction()
main_window.mainloop()
