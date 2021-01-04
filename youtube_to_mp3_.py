import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException


def mp3():
    links_comp = open('links.txt').read().splitlines()
    i = 0

    print(len(links_comp))
    print(links_comp)

    youtube_mp3_download_link = 'https://www.y2mate.com/en19/youtube-mp3'
    path_to_extension = r'C:/Users/mille/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/4.7.3_0'
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)
    driver = webdriver.Chrome(options=chrome_options)
    driver.create_options()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)

    def try_download_function():
        while True:
            try:
                # finds download button
                download_button = driver.find_element_by_id('process_mp3')
                # clicks download button
                download_button.click()
                print('successful click')
                break
            except (NoSuchElementException, ElementClickInterceptedException):
                print('could not find button or click it... trying again after 2 seconds')
                time.sleep(2)

    def try_download_mp3_function():
        while True:
            try:
                # finds download.mp3 button
                download_mp3_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[1]/div/div[4]/div[2]/div[2]/div/div[2]/div[2]/div[1]/a[1]')
                # clicks download.mp3 button
                download_mp3_button.click()
                print('successful click')
                break
            except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
                print('could not find button or click it... round 2... trying again after 2 seconds')
                time.sleep(2)

    while i <= len(links_comp):
        # goes to youtube_mp3 downloader
        driver.get(youtube_mp3_download_link)
        # finds query box
        query_box = driver.find_element_by_name('query')
        # fills in query box
        query_box.send_keys(links_comp[i])
        i += 1
        query_box.send_keys(u'\ue007')
        # function using try and except
        try_download_function()
        # giving the cpu a slight break
        time.sleep(2)
        # next function test
        try_download_mp3_function()
        print(str(len(links_comp) - i) + ' songs left')


if __name__ == '__main__':
    mp3()
