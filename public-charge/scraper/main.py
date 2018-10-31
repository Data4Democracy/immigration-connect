from math import ceil
from time import sleep
from selenium import webdriver


def get_page(results_per_page=50, page_number=1):
    """
    rpp is the results per page (10, 25, 50)
    po is the page offset. If rpp=50, po=0 is 1st page, po=50 is the 2nd page, 
    so on.
    """
    url = "https://www.regulations.gov/docketBrowser"
    url += "?rpp={0}&so=DESC&sb=commentDueDate".format(results_per_page)
    url += "&po={0}&dct=PS".format((page_number-1)*results_per_page)
    url += "&D=USCIS-2010-0012"
    return url

delay = 4
url = get_page(page_number=1)

driver = webdriver.Chrome()
driver.set_window_size(1200, 800)

driver.get(url)
sleep(delay)

# Provide two methods to obtain the total number of comments for robustness.
try:
    results_available = driver.find_element_by_xpath(
        '//div[@class="GIY1LSJILB GIY1LSJBL GIY1LSJIK GIY1LSJCL"]').text
    results_available = int(results_available.split()[-1])
except:
    results_available = driver.find_element_by_xpath(
        '//*[contains(text(), "Displaying")]').text
    results_available = int(results_available.split()[-1])

total_pages = ceil(results_available / 50)


elems = driver.find_elements_by_xpath("//a[@href]")
comments = [ e.get_attribute("href") 
        for e in elems 
        if "document?D=USCIS-" in e.get_attribute("href") ]


comments = list(set(comments))
for c in comments:
    print(c)

driver.get(comments[1])
sleep(delay)

# Get name.
name = driver.find_element_by_xpath(
    '//*[contains(text(), "Comment Submitted by")]').text

# Check that text is not empty.
try:
    comment_text = driver.find_element_by_xpath(
        '//div[contains(text(), "View document")]/../following-sibling::div').text
except:
    comment_text = driver.find_element_by_xpath('//div[@class="GIY1LSJIXD"]').text

# Get date posted.
posted_date = driver.find_element_by_xpath(
    '//span[contains(@title, "Date the document is posted")]/..').text
posted_date = posted_date.split(':\n')[-1]

# Get tracking number.
tracking_number = driver.find_element_by_xpath(
    '//*[contains(text(), "Tracking Number")]/../following-sibling::span').text

# Get RIN.
rin = driver.find_element_by_xpath(
    '//*[contains(text(), "RIN")]/../following-sibling::span').text

# Get received date.
driver.find_element_by_xpath('//a[contains(text(), "Show More Details")]').click()

received_date = driver.find_element_by_xpath(
    '//span[@title="The date the agency received or created the document"]/..').text
received_date = received_date.split(':')[-1]

print(name)
print(comment_text)
print(posted_date)
print(received_date)
print(tracking_number)
print(rin)

driver.quit()
