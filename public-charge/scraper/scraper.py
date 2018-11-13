from math import ceil
from time import sleep
from selenium import webdriver
from xvfbwrapper import Xvfb


class Scraper(object):
    """ Scrape regulations.go comments
    """

    def __init__(self, delay=4):
        """
        """
        self.delay = delay
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1200, 800)

    def shut_down(self):
        self.driver.quit()

    @staticmethod
    def get_page(results_per_page=50, page_number=1):
        """
        rpp is the results per page (10, 25, 50)
        po is the page offset. If rpp=50, po=0 is 1st page, po=50 is the 2nd 
        page, so on.

        To organize by comment due date, newer to older, change 'sb' to 
        'commentDueDate'. To change the order, older to newer change 'so' to
        'DESC'.
        To organize data by date posted, change 'sb' to 'postedDate'.
        """

        url = "https://www.regulations.gov/docketBrowser"
        url += "?rpp={0}&so=DESC&sb=postedDate".format(results_per_page)
        url += "&po={0}&dct=PS".format((page_number - 1) * results_per_page)
        url += "&D=USCIS-2010-0012"
        return url

    def get_comments_total(self):
        """ Get the total number of comments

        Go to the first page of the comments section and get the total number
        of comments from the bar at the bottom of the page.
        """
        # Get the url for the first page.
        url = Scraper.get_page(page_number=1)

        # Open browser.
        self.driver.get(url)
        sleep(self.delay)

        # Provide two methods to obtain the total number of comments.
        try:
            results_available = self.driver.find_element_by_xpath(
                '//*[contains(text(), "Displaying")]').text
            results_available = int(results_available.split()[-1])
        except:
            results_available = self.driver.find_element_by_xpath(
                '//div[@class="GIY1LSJILB GIY1LSJBL GIY1LSJIK GIY1LSJCL"]').text
            results_available = int(results_available.split()[-1])

        #total_pages = ceil(results_available / 50)
        return results_available

    def get_comments_urls_on_page(self, page_number):
        """ Get a list of all comments on a given page

        INPUTS
        ------
        page_number: int

        RETURNS
        -------
        comments: list of strings
            Each entry in the list corresponds to the url for a comment.
        """
        # Get url for given page.
        url = Scraper.get_page(page_number=page_number)

        # Open browser.
        self.driver.get(url)
        sleep(self.delay)

        # Get comment urls.
        elems = self.driver.find_elements_by_xpath("//a[@href]")
        comments = [
            e.get_attribute("href")
            for e in elems
            if "document?D=USCIS-" in e.get_attribute("href")
        ]

        return list(set(comments))

    def scrape_comment(self, comment_url):
        """
        INPUTS
        ------
        comment_url: str
            URL for a comment.

        RETURNS
        -------
        results: dict
            Name, comment, posted and received date, tracking number, and rin.
        """
        # Go to comment.
        self.driver.get(comment_url)
        sleep(self.delay)

        # Get name.
        name = self.driver.find_element_by_xpath(
            '//*[contains(text(), "Comment Submitted by")]').text

        # Check that text is not empty.
        try:
            comment_text = self.driver.find_element_by_xpath(
                '//div[contains(text(), "View document")]/../following-sibling::div'
            ).text
        except:
            comment_text = self.driver.find_element_by_xpath(
                '//div[@class="GIY1LSJIXD"]').text

        # Get date posted.
        posted_date = self.driver.find_element_by_xpath(
            '//span[contains(@title, "Date the document is posted")]/..').text
        posted_date = posted_date.split(':\n')[-1]

        # Get tracking number.
        tracking_number = self.driver.find_element_by_xpath(
            '//*[contains(text(), "Tracking Number")]/../following-sibling::span'
        ).text

        # Get RIN.
        rin = self.driver.find_element_by_xpath(
            '//*[contains(text(), "RIN")]/../following-sibling::span').text

        # Get received date.
        self.driver.find_element_by_xpath(
            '//a[contains(text(), "Show More Details")]').click()
        received_date = self.driver.find_element_by_xpath(
            '//span[@title="The date the agency received or created the document"]/..'
        ).text
        received_date = received_date.split(':')[-1]

        results = {
            "name": name,
            "comment": comment_text,
            "posted_date": posted_date,
            "received_date": received_date,
            "tracking_number": tracking_number,
            "rin": rin,
        }
        return results


if __name__ == "__main__":

    # If True, browser is run headlessly.
    virtual_display = True
    if virtual_display:
        vdisplay = Xvfb()
        vdisplay.start()

    # Start scraper.
    scraper = Scraper(delay=4)

    # Get comment urls on first page.
    urls = scraper.get_comments_urls_on_page(1)

    for i, url in enumerate(urls):
        print(i, scraper.scrape_comment(comment_url=url))

    scraper.shut_down()

    # Stop xvfb
    if virtual_display:
        vdisplay.stop()
