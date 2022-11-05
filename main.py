'''
  TODO
    1. ping check-in page for if it's opened
    2. how to wait for page load explicitly after following link
    3. add functionality to support other aeronautic companies
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import time

# flight regestering utility
class Regestrizer():
  def __init__(
      self, 
      reference_number: str, 
      name: str,
      email: str = None,
      company: str = 'aeroflot', 
      seat_pref: str = 'front-row',
      driver: webdriver.Firefox = None
    ) -> None:
    assert company == 'aeroflot', 'Only Aeroflot regestration is supported for now.'
    self.driver = driver
    self.data = {
      'company': company.lower(),
      'ref_num': reference_number,
      'name': name,
      'pref': seat_pref,
      'email': email,
    }
    self.status = 'Not regestered'

  @staticmethod 
  def getCurrTime() -> tuple:
    t = time.localtime()
    return (t.tm_hour, t.tm_min, t.tm_sec)

  def openBrowser(self) -> None:
    self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
  
  def quitBrowser(self) -> None:
    self.driver.quit()
  
  def gotoCheckinWebpage(self, company_page: str = 'https://www.aeroflot.ru/sb/ckin/app/ru-en') -> None:
    self.driver.implicitly_wait(5)
    self.driver.get(company_page)

  def companySpecificDelay(self) -> None:
    if self.data['company'] == 'aeroflot':
      time.sleep(2)
    else:
      pass

  def inputRefAndName(self) -> None:
    try:
      # find inputs
      input_boxes = self.driver.find_elements(by=By.CLASS_NAME, value='input__text-input')
      ref_input = input_boxes[0]
      name_input = input_boxes[1]
      # click on them
      ref_input.click()
      name_input.click()
      # set their values
      ref_input.send_keys(self.data['ref_num'])
      name_input.send_keys(self.data['name'])
      # click on button to proceed to next stage
      link = self.driver.find_element(by=By.CLASS_NAME, value='next__button')
      link.click()
    except NoSuchElementException:
      self.status = 'Unknown webpage structure led to error'

  def completeRegestration(self) -> None:
    try:
      # click on button to proceed to next stage
      link = self.driver.find_element(by=By.CLASS_NAME, value='next__button')
      link.click()
      # select seat
      first_available_seat = self.driver.find_element(by=By.CLASS_NAME, value='seating__number')
      first_available_seat.click()
      # close popup
      try:
        popup = self.driver.find_element(by=By.ID, value='countryListToggle')
        popup.click()
        country = self.driver.find_element(by=By.CLASS_NAME, value='notification__countrys-label')
        country.click()
        select = self.driver.find_element(by=By.CLASS_NAME, value='submitSelectedCountry')
        select.click()
      except NoSuchElementException:
        pass
      # click on Check in button
      button = self.driver.find_element(by=By.CLASS_NAME, value='button--medium-padding')
      button.click()
      # check in successful
      self.status = 'Success'
    except NoSuchElementException:
      self.status = 'Unknown webpage structure led to error'

  def sendTicketToEmail(self):
    pass

  def __repr__(self) -> str:
    return f'|Reference: { self.data["ref_num"] } \n|Name: { self.data["name"] } \n|Status: { self.status }'

# how regestration should be proceved
if __name__ == '__main__':
  ref = input('Your reference code >')
  name = input('Your family name >')
  regestrizer = Regestrizer(reference_number=ref, name=name)
  regestrizer.openBrowser()
  regestrizer.gotoCheckinWebpage()
  regestrizer.inputRefAndName()
  regestrizer.companySpecificDelay()
  regestrizer.completeRegestration()
  regestrizer.sendTicketToEmail()
  regestrizer.quitBrowser()
  print(regestrizer.status)
