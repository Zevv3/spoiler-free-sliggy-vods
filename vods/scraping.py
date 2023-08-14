from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import time
from collections import deque

def get_videos():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--remote-allow-origins=*") 
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.youtube.com/@Sliggytv/videos')

    WAIT_IN_SECONDS = 2
    SCROLL_TIMES = 3 
    scroll_count = 0

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while scroll_count < SCROLL_TIMES:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        # Wait for new videos to show up
        time.sleep(WAIT_IN_SECONDS)

        # Calculate the new document height and compare it with the last height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        scroll_count += 1
        
    # Continue with scraping the loaded videos


    titles = driver.find_elements(By.ID, 'video-title')
    links = driver.find_elements(By.ID, 'video-title-link')
    # driver.find_element(By.CLASS_NAME)

    videos = {title.text: link.get_attribute('href') for title, link in zip(titles, links)}

    # titles = [title.text for title in titles]
    # teams = [title.split('Map')[0] for title in titles]
    # links = [link.get_attribute('href') for link in links]

    series = {}
    for title, link in videos.items():
        if 'final' in title.lower() or 'finals' in title.lower():
            best_of = 5
        else:
            best_of = 3
        if 'lower' in title.lower():
            lower = True
        else:
            lower = False
        split_title = title.lower().split(' ')
        teams = split_title[0].upper() + ' ' + split_title[1] + ' ' + split_title[2].upper()
        teams_variation = split_title[2].upper() + ' ' + split_title[1] + ' ' + split_title[0].upper()
        if best_of == 5:
            if teams + ' finals' not in series and teams_variation + ' finals' not in series:
                default_value = 'https://www.youtube.com/'
                maps = deque([default_value] * best_of)
                series[teams + ' finals'] = maps
                maps.appendleft(link)
                maps.pop()
            if teams_variation + ' finals' in series:
                maps = series[teams_variation + ' finals']
                maps.appendleft(link)
                maps.pop()
            else:
                maps = series[teams + ' finals']
                maps.appendleft(link)
                maps.pop()
        if best_of == 3:
            if lower:
                if teams + ' lower' not in series and teams_variation + ' lower' not in series:
                    default_value = 'https://www.youtube.com/'
                    maps = deque([default_value] * best_of)
                    series[teams + ' lower'] = maps
                    maps.appendleft(link)
                    maps.pop()
                if teams_variation + ' lower' in series:
                    maps = series[teams_variation + ' lower']
                    maps.appendleft(link)
                    maps.pop()
                else:
                    maps = series[teams + ' lower']
                    maps.appendleft(link)
                    maps.pop()
            else:
                if teams not in series and teams_variation not in series:
                    default_value = 'https://www.youtube.com/'
                    maps = deque([default_value] * best_of)
                    series[teams] = maps
                    maps.appendleft(link)
                    maps.pop()
                if teams_variation in series:
                    maps = series[teams_variation]
                    maps.appendleft(link)
                    maps.pop()
                else:
                    maps = series[teams]
                    maps.appendleft(link)
                    maps.pop()
        
        
    return series