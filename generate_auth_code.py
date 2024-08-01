import credentials as cr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fyers_apiv3 import fyersModel
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import totp_pin as tp

# Get values from credentials file
client_id = cr.client_id
secret_key = cr.secret_key
redirect_uri = cr.redirect_uri
response_type = cr.response_type  
state = cr.state
grant_type = cr.grant_type
auth_code = cr.auth

# create a public method generateAuthCode which returns a string
def generateAuthCode():
    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )

    # Generate the auth code using the session model
    uri = session.generate_authcode()

    # driver = webdriver.Chrome()
    # Set Chrome options for headless mode
    options = Options()
    options.add_argument('--headless=new')

    # Initialize Chrome webdriver
    driver = webdriver.Chrome(options=options)

    driver.get(uri)

    time.sleep(1)
    login_with_clien_id_x_path='//*[@id="login_client_id"]'
    elem = driver.find_element(By.XPATH, login_with_clien_id_x_path)
    elem.click()
    time.sleep(1)
    client_id_input_x_path='//*[@id="fy_client_id"]'
    elem2 = driver.find_element(By.XPATH, client_id_input_x_path)
    elem2.send_keys(cr.username)
    elem2.send_keys(Keys.RETURN)
    time.sleep(1)

    t=tp.get_totp()

    driver.find_element(By.XPATH, '//*[@id="first"]').send_keys(t[0])
    driver.find_element(By.XPATH, '//*[@id="second"]').send_keys(t[1])
    driver.find_element(By.XPATH, '//*[@id="third"]').send_keys(t[2])
    driver.find_element(By.XPATH, '//*[@id="fourth"]').send_keys(t[3])
    driver.find_element(By.XPATH, '//*[@id="fifth"]').send_keys(t[4])
    driver.find_element(By.XPATH, '//*[@id="sixth"]').send_keys(t[5])

    driver.find_element(By.XPATH, '//*[@id="confirmOtpSubmit"]').click() 
    time.sleep(1)

    driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"first").send_keys(cr.pin1)
    driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"second").send_keys(cr.pin2)
    driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"third").send_keys(cr.pin3)
    driver.find_element(By.ID,"verifyPinForm").find_element(By.ID,"fourth").send_keys(cr.pin4)

    driver.find_element(By.XPATH,'//*[@id="verifyPinSubmit"]').click()
    time.sleep(1)
    newurl = driver.current_url
    print(newurl)
    auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    print(auth_code)
    driver.close()
    return auth_code