import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
NOTES:
- Incorporate multithreading to speed up the process 
'''


# retrieves the correct links and reorganizes
def mp3():
    links_unfinished = open('links_unfinished.txt').read().splitlines()

    print(len(links_unfinished))
    print(links_unfinished)
    links_2 = [x for x in links_unfinished if 'https://www.youtube.com/user' not in x]
    links_comp = [x for x in links_2 if 'https://www.youtube.com/channel' not in x]
    print(len(links_comp))
    print(links_comp)

    # saves cleaned links to a finished .txt file
    with open("links_fin.txt", 'w') as output:
        for row in links_comp:
            output.write(str(row) + '\n')

    youtube_mp3_download_link = 'https://www.y2mate.com/en19/youtube-mp3'
    path_to_extension = r'C:/Users/mille/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/4.7.3_0'
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)
    driver = webdriver.Chrome(options=chrome_options)
    driver.create_options()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)

    i = 0
    while i <= len(links_comp):
        # goes to youtube_mp3 downloader
        driver.get(youtube_mp3_download_link)
        time.sleep(5)
        # finds query box
        query_box = driver.find_element_by_name('query')
        # fills in query box
        query_box.send_keys(links_comp[i])
        i += 1
        query_box.send_keys(u'\ue007')
        time.sleep(5)
        # finds download button
        download_button = driver.find_element_by_id('process_mp3')
        # clicks download button
        download_button.click()
        time.sleep(30)
        # finds download.mp3 button
        download_mp3_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[1]/div/div[4]/div[2]/div[2]/div/div[2]/div[2]/div[1]/a[1]')
        # clicks download.mp3 button
        download_mp3_button.click()
        time.sleep(2)


if __name__ == '__main__':
    mp3()
