from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv

# Specify the path to your ChromeDriver executable
chrome_driver_path = "F:/chrome-win64/chromedriver-win64/chromedriver.exe"

# Create a new instance of the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
# driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# Set up Chrome WebDriver
chrome_service = webdriver.chrome.service.Service(chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)

index = 0

def create_csvlog(data, group_name):
    current_datetime = datetime.now().strftime("%Y%m%d")
    file_name = 'backup/'+'_'+current_datetime+'.csv'

    try:
        with open(file_name,'a+', encoding='utf-8') as file:
            print('writing log...')
        with open(file_name,'r+', encoding='utf-8') as file:
            # Append content to the file
            writer = csv.writer(file)

            # read file
            csv_reader = csv.reader(file)
            # print(any(csv_reader))
            
            # Check if the file is empty
            if not any(csv_reader):
               # Column 1->S.No,Column 2->Group Name,Column 3->Chats
               writer.writerow(['Group Name', 'Chats'])
            
            chat_data = '\n'.join(map(str, data))

            print(group_name + ' -- ' + str(len(chat_data)))
            writer.writerow([group_name,chat_data])
            
        # print('logged successfully')
    except IOError as e:
        print(f"An error occurred: {e}")

def create_log(file_name,data):

    try:
        with open(file_name, 'a+', encoding='utf-8') as file:
            # Append content to the file
            file.write(data)
        # print('logged successfully')
    except IOError as e:
        print(f"An error occurred: {e}")

def export_whatsapp_group_chat(group_name):
      current_datetime = datetime.now().strftime("%Y%m%d_%H%M")
      file_name = 'backup/'+group_name+'_'+current_datetime+'.txt'
      file_name = file_name.replace(" ", "_")
      
      # Open WhatsApp Web
      driver.get("https://web.whatsapp.com/")

      # Search for the group by name
      # title="Search input textbox"
      search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Search input textbox']")))
      search_box.click()
      search_box.send_keys(group_name)
      del search_box
      
      try:
        for _ in range(2):  # You may need to adjust the number of iterations based on your needs
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@class='_2a-B5 VfC3c']").send_keys(Keys.PAGE_UP)
            time.sleep(1)
      except Exception as e:
        print(f"----")
      try:  
        try:
            # Wait for the search results to appear
            xpath_expression = f"//span[contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{group_name.lower()}')]"
            group_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
            time.sleep(3)
            del xpath_expression
            # Open the group
            group_element.click()
            del group_element
        
            if index == 1:
                for _ in range(4):  # You may need to adjust the number of iterations based on your needs
                    driver.find_element(By.XPATH, "//div[@class='_5kRIK']").send_keys(Keys.PAGE_UP)
                    time.sleep(1)

                time.sleep(2)
                try:
                    sync_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='sync-in-progress']")))
                    sync_element.click()
                    input("Press enter after syncing all chats")

                except Exception as e:
                    print(f"unable to sync message")
            # Wait for the chat area to be clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_5kRIK']")))

            # Scroll to load chat history
            # element = driver.find_element(By.XPATH, "//div[@class='_5kRIK']")
            # Check if any element contains specific text
            # desired_text = "Use WhatsApp on your phone to see older messages."
            # while desired_text.lower() not in element.text.lower():
            for _ in range(10):
                driver.find_element(By.XPATH, "//div[@class='_5kRIK']").send_keys(Keys.CONTROL + Keys.HOME) # Keys.PAGE_UP
                time.sleep(1)

                try:
                    get_new_message = driver.find_element(By.XPATH,"//button[@class='_1JCqN _1DlhQ']")
                    get_new_message.click()
                except Exception as e:
                    try:
                        get_date = driver.find_element(By.XPATH,"//span[@class='_11JPr']")
                        print("please wait loading chat before "+get_date.text)
                    except Exception as e:
                        print('...')
                # _1JCqN _1DlhQ

            # del element


            # Extract and print the chat messages (you might want to save them to a file)
            #   chat_messages = driver.find_elements(By.XPATH, "//div[@class='CzM4m _2zFLj']")
            chat_messages = driver.find_elements(By.CSS_SELECTOR,".focusable-list-item")
            chat_data = []
            for message in chat_messages:
                if "message-out" in message.get_attribute("class"):
                    # create_log(file_name, )                    
                    chat_data.append("ME\n----\n"+message.text+"\n")
                    create_log(file_name,"\t\t\t\t"+message.text.replace('\n', '\n\t\t\t\t')+"\n")
                    # create_log(file_name,message.get_attribute("class")+"\n")        
                    create_log(file_name,"\t\t\t\t"+"----------------\n\n")
                else:
                    chat_data.append(message.text+"\n")
                    # create_log(file_name, )
                    create_log(file_name,message.text+"\n")
                    # create_log(file_name,message.get_attribute("class")+"\n")        
                    create_log(file_name,""+"----------------\n\n")
            
            create_csvlog(chat_data,group_name)
            del chat_data
            del chat_messages
            del file_name
        
        except NoSuchElementException:
            print('error: '+group_name + 'Chat not found')
        except TimeoutException:
            print('error: '+group_name + 'Timeout')

      except Exception as e:
        print(f"end "+ str(e))
        # export_whatsapp_group_chat(group_name)

# Replace "path/to/chromedriver" with the actual path to your ChromeDriver executable
# Replace "Your Group Name" with the name of the WhatsApp group you want to export
# group_list = ["Kenmark ITan Solutions", "KiTS - Equity Address ", "Medical Mandi Integration"]

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")

# Wait for the user to scan the QR code and log in
input("Scan the QR code and press Enter after logging in:")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='pane-side']")))
group_list = []
unique_set = set()

# Find the element by ID
element = driver.find_element("id", "pane-side")
total_scroll_length = driver.execute_script("return arguments[0].scrollHeight;", element)

print("Please wait fetching group list..." + str(total_scroll_length))
# Scroll to the bottom slowly
# for i in range(0, total_scroll_length, 30):  # element.size["height"]
for i in range(0, total_scroll_length, 30):
    driver.execute_script(f"arguments[0].scroll(0, {i});", element)
    # time.sleep(0.000001)  # Adjust the sleep duration as needed
    chat_list = driver.find_elements(By.CSS_SELECTOR, "._21S-L")
    for a in chat_list:
        try:
            if a.text not in unique_set:
                print(str(index) + '. ' + a.text)
                group_list.append(a.text)
                unique_set.add(a.text)
                index += 1
        except Exception as e:
            print(f"An unexpected error occurred{e}")


# print(len(group_list))
for group_name in group_list:
    print(group_name+'---')
    index += 1
    export_whatsapp_group_chat(group_name)

driver.get("https://web.whatsapp.com/")
print("process completed")

menu_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Menu']")))
menu_element.click()

# Specify the specific text you are looking for
specific_text = 'Log out'

# Build the XPath to locate the element with the specific text
xpath_exp = f'//*[text()="{specific_text}"]'
# Find the element based on the specific text using XPath
element = driver.find_element(By.XPATH, xpath_exp)
# Click on the found element
element.click()
time.sleep(2)

logout_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='emrlamx0 aiput80m h1a80dm5 sta02ykp g0rxnol2 l7jjieqr hnx8ox4h f8jlpxt4 l1l4so3b le5p0ye3 m2gb0jvt rfxpxord gwd8mfxi mnh9o63b qmy7ya1v dcuuyf4k swfxs4et bgr8sfoe a6r886iw fx1ldmn8 orxa12fk bkifpc9x rpz5dbxo bn27j4ou oixtjehm hjo1mxmu snayiamo szmswy5k']")))
logout_element.click()

time.sleep(10)

# Close the browser window
driver.quit()
