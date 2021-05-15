# code refactorered from:
# https://github.com/xjdeng/pinterest-image-scraper/blob/master/pinterest_scraper/scraper.py


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from six.moves.urllib.parse import urlparse

import time
import random
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class PinterestFetcher(object):
  def __init__(self, email, password, browser=None):
    if browser is None:
      browser_options = webdriver.ChromeOptions()
      browser_options.add_argument('--headless')
      browser_options.add_argument('--no-sandbox')
      browser_options.add_argument('--disable-dev-shm-usage')
      browser_options.add_argument("--width=1920")
      browser_options.add_argument("--height=1080")
      self.browser = webdriver.Chrome("chromedriver",
                                      options=browser_options)

    self.email = email
    self.password = password

    self.browser.get("https://www.pinterest.com")

    if not self._login():
      raise RuntimeError("Could not log into pintrest")


  def _login(self, login_class="tBJ, dyH, iFc, yTZ, erh, tg7, mWe", login_text="Log in"):
    login_element = self.browser.find_elements_by_css_selector(
      "div[data-test-id=simple-login-button")

    if not login_element:
      raise RuntimeError("Could not find login button")
  
    login_element[0].click()

    # log in
    email_field = self.browser.find_element_by_name("id")
    email_field.send_keys(self.email)

    # enter password and hit enter
    password_field = self.browser.find_element_by_name("password")
    password_field.send_keys(self.password)
    password_field.send_keys(Keys.RETURN)

    # act natural
    self._randdelay(2, 4)

    return True


  def _homepage(self):
    self.browser.get("https://www.pinterest.com")


  def _click_searchbar(self):
    self.browser.find_element_by_name("searchBoxInput").click()
  

  def get_suggestions(self):
    self._homepage()
    self._click_searchbar()
    search_suggestions = self.browser.find_elements_by_css_selector(
        "div[id*=SuggestionGroup-Option-]")

    if not search_suggestions:
      raise RuntimeError("Couldnt get search suggestions, are you on the seach page?")
  
    suggestion_labels = []
    suggestion_links = []

    for suggestion in search_suggestions:

      # it's a recent search and not a suggestion
      if len(suggestion.find_elements_by_css_selector("div")) != 7:
        continue

      # get the link elements
      link_element = suggestion.find_element_by_css_selector("a")
      if not link_element:
        print("couldnt find link, may be an error")
        continue

      suggestion_labels.append(suggestion.text)
      suggestion_links.append(link_element.get_property("href"))

    self._click_searchbar()
    return(pd.DataFrame({ "label": suggestion_labels, "link": suggestion_links }))


  def run(self, url, num_images=500):
    self.browser.get(url)

    image_links = list()
    prev_len = 0
    while len(image_links) < num_images:
      image_links += self._get_image_links(existing_links=set(image_links))

      n_retrieved = len(image_links)

      if n_retrieved == prev_len:
        print("cant scrape anymore... returning")
        break

      self._print_percent_output(n_retrieved, num_images)
      prev_len = n_retrieved

      self.browser.find_element_by_css_selector("body").send_keys(Keys.END)

      # wait for page to reload
      self._randdelay(10, 11)
    print("Done Scraping")

    return(image_links[:num_images])


  @staticmethod
  def _print_percent_output(n_through, max_n):
    percent_retrieved = (n_through / max_n) * 100
    formatted_percent = "{0:.2f}".format(percent_retrieved)
    print(f"{formatted_percent}/100%")

  def _get_image_links(self, existing_links=set()):
    if isinstance(existing_links, list):
      existing_links = set(existing_links)
    
    image_links = []
    page_pins = self.browser.find_elements_by_css_selector("div[data-test-id=pinWrapper]")
    for pin in page_pins:

      # check if it's an ad
      if pin.find_elements_by_css_selector("div[title='Promoted by']"):
        continue

      pin_img = pin.find_elements_by_css_selector("div[data-test-id=non-story-pin-image]")

      if not pin_img:
        print("couldnt find image link, may be an error")
        continue

      pin_img = pin_img[0].find_elements_by_css_selector("img")

      if not pin_img:
        print("couldnt find image link, may be an error")

      image_link = pin_img[0].get_property("src")
      if image_link in existing_links:
        continue

      image_links.append(image_link)
    return(image_links)


  def screenshot(self, filename="screenshot"):
    filename = f"{filename}.png" if "." not in filename else filename
    with open(filename, "wb") as outfile:
      outfile.write(self.browser.get_screenshot_as_png())
  
    img = mpimg.imread(filename)
    plt.imshow(img)
    plt.show()


  def close(self):
    self.browser.close()

  def __del__(self):
    self.close()


  @staticmethod
  def download(
    imagelinks,
    output_directory = "./", print_id=0, print_every=50, n_to_download=0):
    if isinstance(imagelinks, str) or isinstance(imagelinks, bytes):
      # get the image
      res = requests.get(imagelinks)

      # raise on bad status
      res.raise_for_status()

      # get the image name and make the output filename
      imagename = os.path.basename(urlparse(imagelinks).path)
      outfilename = f"{output_directory}/{imagename}"

      if n_to_download and not print_id % print_every:
        PinterestFetcher._print_percent_output(print_id, n_to_download)

      # save to file
      with open(outfilename, "wb") as outfile:
        for chunk in res.iter_content(100000):
          outfile.write(chunk)
      return(outfilename)
    elif isinstance(imagelinks, list):
      downloaded_filenames = []
      for i, link in enumerate(imagelinks):
        downloaded_filenames.append(
          PinterestFetcher.download(
            link, output_directory,
            print_id=i, n_to_download=len(imagelinks)))
      return(downloaded_filenames)
    else:
        pass
  
  @staticmethod
  def _randdelay(a, b):
    time.sleep(random.uniform(a, b))
