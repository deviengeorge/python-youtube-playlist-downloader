
# Selenium Library
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# OS Library
import os

# Downloader Library
import wget

# User Agent
from fake_useragent import UserAgent

# csv writer
import csv

# Global Variables
spaces = 60
character = "#"


def printHash(*texts):
    print()
    print(character * spaces)
    for text in texts:
        print(f" {text} ".center(spaces, character))
    print(character * spaces)
    print()


def printSparetor():
    print()
    print(character * spaces)
    print()


def questionInput(text=""):
    if (text != ""):
        print(text)
    return input("=> ").lower()


class Playlist():
    titles = []
    links = []
    playlistLink = ""
    browser = True
    options = [
        # "download" for download the videos
        # "sorting" for sorting the downloaded videos
        # "append" for make file inside it download links of playlist
    ]

    def __init__(self):
        # Print Menu Of Options
        self.printMenu()

        # Open Selenium Browser
        if (self.browser):
            self.openBrowser()

        # Print Footer to attribute creator
        self.printFooter()

    def printMenu(self):
        printHash("Menu")
        print("  1. Download The Playlist")
        print("  2. Get The Download Links And Append It To TEXT File")
        print("  3. Get The Download Links And Append It To CSV File")
        print("  4. Download The Playlist From links In Links.txt file")
        print("  5. Exit")
        printSparetor()
        answer = questionInput()
        printSparetor()

        if (answer == "1" or answer == "2" or answer == "3"):
            print("Enter Playlist Link")
            self.playlistLink = input("=> ")
            printSparetor()

        # Download Option
        if (answer == "1"):
            answer = questionInput("Download The Whole Playlist ( yes | no ):")

            printSparetor()

            self.options.append("download")
            answer = questionInput(
                "Download With Automatic Sorting e.g. ( 1. VideoName ) ?:")

            printSparetor()

            if (answer == 'yes' or answer == 'y'):
                self.options.append("sorting")

        # Append TXT Option
        elif (answer == "2"):
            self.options.append("appendTxt")

        # Append Csv Option
        elif (answer == "3"):
            self.options.append("appendCsv")

        elif (answer == "4"):
            self.browser = False
            csvFile = open("links.csv", "r")
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                self.links.append(row["Link"])
                self.titles.append(row["Name"])
                print(row["Name"])
            self.download()

        # Exit Option
        else:
            printHash("Exit")
            exit()

    def openBrowser(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Setup Selenium Driver
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )

        driver.get("https://keepvid.pro/youtube-playlist-downloader")

        driver.find_element_by_xpath(
            "//*[@id='videourl']").send_keys(self.playlistLink)
        driver.find_element_by_xpath("//*[@id='downloadbtn']").click()

        # Check If There A PopUp Has Shown, Back Us To The Main Page
        if (len(driver.window_handles) > 1):
            driver.switch_to.window(driver.window_handles[0])

        parentElement = driver.find_element_by_id("playlist-row")

        # Wait For Loading The Playlist Links
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "#playlist-row a")
                )
            )
        except:
            printHash("Error In Getting Videos Info", "Try Again Later")
            exit()

        self.getTitles(parentElement)
        self.getLinks(parentElement)

        if ("download" in self.options):
            if ("sorting" in self.options):
                self.download(True)
            else:
                self.download()

        if ("appendTxt" in self.options):
            self.createTxt()

        if ("appendCsv" in self.options):
            self.createCSV()

        # Closing All Pages
        driver.quit()

    def getTitles(self, parentElement):
        titlesElements = parentElement.find_elements_by_css_selector(
            "tr td:nth-child(3)")
        titles = [
            title.text.replace("+", "Plus").replace("?", "").replace("|", " ") for title in titlesElements
        ]
        self.titles = titles

    def getLinks(self, parentElement):
        childElements = parentElement.find_elements_by_tag_name("a")
        links = [link.get_attribute('href') for link in childElements]
        self.links = links

    def download(self, sorting=False):
        printHash("Download")
        answer = questionInput("Download Full Playlist ( yes | no ): ")

        printSparetor()

        if (answer == 'yes' or answer == 'y'):
            self.start = 0
            self.end = len(self.links) - 1
        else:
            self.start = int(questionInput(
                "Please Enter The Start Point:")) - 1

            printSparetor()

            self.end = int(questionInput(
                "Please Enter The End Point:")) - 1

            printSparetor()

        # I Used enumerate(zip()) To Add Index To The Loop
        for index, (link, title) in enumerate(zip(self.links, self.titles)):
            if (index <= self.end and index >= self.start and not any(title in videoFile for videoFile in os.listdir("."))):
                if (title.endswith(".mp4")):
                    videoName = f'{title}'
                else:
                    videoName = f'{title}.mp4'

                if (sorting == True):
                    newName = f'{str(index) + 1}. {videoName}'
                else:
                    newName = videoName
                print(f"\n{newName}")
                fileName = wget.download(link, newName)
                fileName
            elif (any(title in videoFile for videoFile in os.listdir("."))):
                print(f"{title} - Already Downloaded")
            else:
                pass

    def createTxt(self):
        printHash("Loading...", "Create TEXT File")
        txtFile = open("links.txt", "w+")
        for index, (link, title) in enumerate(zip(self.links, self.titles)):
            newName = f'{title}.mp4'
            txtFile.write(f'{newName} Link is:\n{link}\n{"-" * 80}')
            print(newName)
        txtFile.close()

    def createCSV(self):
        # Create CSV file contain names of videos and links of downloaded playlist
        printHash("Loading...", "Create CSV File")
        csvFile = open("links.csv", "w+")
        writer = csv.writer(csvFile)
        writer.writerow(["Name", "Link"])
        for (link, title) in zip(self.links, self.titles):
            newName = f'{title}.mp4'
            writer.writerow([newName, link])
            print(newName)

    def printFooter(self):
        printHash("Thanks For Using Our Script", "Coded By Devien George")


# initialize Class
Playlist()
