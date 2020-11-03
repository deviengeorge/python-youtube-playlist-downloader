# Selenium Library
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Downloader Library
import wget

# Regex Support
import re

# Global Variables
links = []
titles = []


def Playlist(end=-1):
    try:
        # Make Chrome Headless Browser ( Mean That Chrome Will NOT Show )
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")

        # Setup Selenium Driver
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)

        # GO to keepVid Page
        driver.get("https://keepvid.pro/youtube-playlist-downloader")

        # GET Playlist Link
        playlist_url = input("Please Enter Playlist Link: ")

        # Locate Input, Download Button
        driver.find_element_by_xpath(
            "//*[@id='videourl']").send_keys(playlist_url)
        driver.find_element_by_xpath("//*[@id='downloadbtn']").click()

        # Function To GET Titles Of YouTube Videos
        def getTitles():
            titlesElements = parentElement.find_elements_by_css_selector(
                "tr td:nth-child(3)")
            titles = [title.text for title in titlesElements]
            print("\nSuccessfully: GET Video Titles\n")
            return titles

        # Function To GET Download Links Of YouTube Videos
        def getLinks():
            childElements = parentElement.find_elements_by_tag_name("a")
            links = [link.get_attribute('href') for link in childElements]
            return links

        # Check If There A PopUp Has Shown, Back Us To The Main Page
        if (len(driver.window_handles) > 1):
            driver.switch_to.window(driver.window_handles[0])

        parentElement = driver.find_element_by_id("playlist-row")

        # Wait For Loading The Playlist Links
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "#playlist-row a"))
        )

        # Make Variables Global To Use Them Outside The Function
        global titles
        global links

        # Initialize getTitles, getLinks Functions
        titles = getTitles()
        links = getLinks()

        # Closing All Pages
        print("\nClosing The Browser...\n")
        driver.quit()
    except:
        print("\nError: Closing The Browser\n")


Playlist()

titles = [re.sub("(/|:)", "", title) for title in titles]


def downloadVideos(sorting=True):
    question = input("Download The Whole Playlist ( yes | no ):").lower()
    
    if (question == "yes" or question == "y"):
        start = 0
        end = len(links) - 1
        print(f"\nVideos Count {len(links)}")
    else:
        start = int(input("Please Enter The Start Point: ")) - 1
        end = int(input("Please Enter The End Point: ")) - 1
        print("\nVideos Count:", end - start)

    # I Used enumerate(zip()) To Add Index To The Loop
    for index, (link, title) in enumerate(zip(links, titles)):
        if (index <= end and index >= start):
            if (sorting == True):
                newName = f'{str(index)}. {title.replace("+", "Plus").replace("?", "").replace("#", "")}.mp4'
            else:
                newName = f'{title.replace("+", "Plus").replace("?", "").replace("#", "")}.mp4'
            print("\n" + newName)
            fileName = wget.download(link, newName)
            fileName


def createTxt():
    txtFile = open("links.txt", "w+")
    for index, (link, title) in enumerate(zip(links, titles)):
        newName = f'\n{str(index + 1).zfill(2)}. {title.replace("+", "Plus").replace("?", "").replace("#", "")}.mp4'
        print(f'{newName} Link is:\n{link}')
        txtFile.write(f'{newName} Link is:\n{link}\n')
    txtFile.close


# Initialize Download Videos Function
if (input("Would You Like To Download The Playlist ( yes | no ) : ").lower() == "yes"):
    if (input("Would You Like To Download The Videos With ( Indexs ) In The First For Sorting ( yes | no ): ").lower() == "yes"):
        downloadVideos()
    else:
        downloadVideos(sorting=False)
elif (input("Would You Like To Append Videos Links To Txt File ( yes | no ): ").lower()):
    createTxt()

print("\n\nThanks for Using Our Script\nCoded By Devien George\n")


