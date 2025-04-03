from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from Product import Product
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#PATH = 'D:\Python-scraping-application-main\data\chromedriver.exe'
PATH = "./data/chromedriver.exe"

# def login():
#     options = webdriver.ChromeOptions()
#     options.add_argument('--no-sandbox')
#     options.add_argument('--headless')
#     options.add_argument('--disable-notifications')#Disables the Web Notification and the Push APIs.
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
#     options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36')
#
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     # service = Service(executable_path=PATH)
#     driver = webdriver.Chrome( options=options)
#
#     driver.get("https://shopee.vn/buyer/login")
#
#     # Tìm và điền thông tin đăng nhập (sửa thành tài khoản và mật khẩu của bạn)
#     username_input = driver.find_element("name", "loginKey")
#     username_input.send_keys("0847055400")
#
#     password_input = driver.find_element("name", "password")
#     password_input.send_keys("Yeuemdaikho12")
#
#     # Submit form đăng nhập
#     password_input.send_keys(Keys.ENTER)
#     time.sleep(3)
#     return driver

def login():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # Không sử dụng headless mode để nhập CAPTCHA thủ công nếu cần
    # options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-infobars')

    driver = webdriver.Chrome(options=options)

    try:
        driver.set_window_size(1366, 768)
        print("Đang truy cập trang chủ Shopee...")
        driver.get("https://shopee.vn")
        time.sleep(3)

        # # Kiểm tra xem có CAPTCHA không
        # try:
        #     captcha = driver.find_element(By.XPATH, "//div[contains(@class, 'captcha')]")
        #     if captcha:
        #         print("Shopee yêu cầu CAPTCHA. Vui lòng nhập CAPTCHA thủ công.")
        #         # Chờ người dùng nhập CAPTCHA (vì không ở chế độ headless)
        #         WebDriverWait(driver, 60).until_not(
        #             EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'captcha')]"))
        #         )
        #         print("CAPTCHA đã được giải quyết")
        # except:
        #     print("Không phát hiện CAPTCHA")

        # Đợi form đăng nhập xuất hiện
        try:
            # Cập nhật XPath để tìm input tên đăng nhập (dựa trên placeholder hoặc class)
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='text' or @placeholder='Số điện thoại' or @name='phone']"))
            )
            username_input.clear()
            username_input.send_keys("0847055400")
            print("Đã nhập tên đăng nhập")
            time.sleep(1)

            # Tìm và nhập mật khẩu
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='password' or @placeholder='Mật khẩu' or @name='password']"))
            )
            password_input.clear()
            password_input.send_keys("Yeuemdaikho12")
            print("Đã nhập mật khẩu")
            time.sleep(1)

            # Nhấn nút đăng nhập
            try:
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class, 'btn-solid-primary') or contains(text(), 'Đăng nhập')]"))
                )
                login_button.click()
                print("Đã nhấp vào nút đăng nhập")
            except:
                print("Không tìm thấy nút đăng nhập, sử dụng phím Enter")
                password_input.send_keys(Keys.ENTER)

            # Đợi đăng nhập hoàn tất
            print("Đợi đăng nhập hoàn tất...")
            WebDriverWait(driver, 30).until(
                lambda d: "buyer/login" not in d.current_url and "shopee.vn" in d.current_url
            )
            print("Đăng nhập thành công!")
            return driver

        except Exception as e:
            print(f"Lỗi khi nhập thông tin đăng nhập: {str(e)}")
            driver.quit()
            return None

    except Exception as e:
        print(f"Lỗi khi đăng nhập Shopee: {str(e)}")
        driver.quit()
        return None

def generateLinks(numberOfPage, searched_product):
    urlList = []
    for i in range(numberOfPage):
        search = searched_product.lower().replace(' ', '%20')
        url = "https://shopee.vn/search?keyword={}&page={}".format(search, i)
        urlList.append(url)
    return urlList

def getHtml(driver, url):  # get source code of web
    try:
        driver.get(url)
        time.sleep(3)
        for i in range(15):
            driver.execute_script("window.scrollBy(0, 450)")
            time.sleep(0.1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        return soup
    except:
        driver.close()
        return None

def fillProductList(root, driver, url):
    soup = getHtml(driver, url)
    # print(soup)
    if soup == None:
        return
    items = soup.find_all('div', class_='col-xs-2-4 shopee-search-item-result__item')
    for item in items:

        # name
        nameItem = item.find('div', class_='ie3A+n bM+7UW Cve6sh').text
        price = item.findAll('span', class_='ZEgDH9')

        minPrice, maxPrice = 0, 0
        if len(price) > 1:
            minPrice, maxPrice = [int(x.text.replace('.', '')) for x in price]
        else:
            minPrice = maxPrice = int(price[0].text.replace('.', ''))

        # rating
        stars = item.findAll('div', class_='shopee-rating-stars__lit')
        rating = None
        if len(stars) != 0:
            rating = 0
            for star in stars:
                rating += float(star['style'].split()[1][:-2]) / 100

        quantity, sales = item.find('div', class_='r6HknA uEPGHT'), '0'
        if quantity != None:
            sales = quantity.text.split(
            )[-1].replace(',', '').replace('k', '000')

        # link
        linkItem = 'https://shopee.vn' + item.find('a')['href']
        discount_tmp = item.find('span', class_='percent')
        if discount_tmp == None:
            discount = None
        else:
            discount = int(discount_tmp.text[:-1])
        p = Product(nameItem, minPrice, maxPrice, rating, sales, linkItem, discount)
        # print(p)
        root.productList.append(p)
# def run(root, numberOfPage, searched_product):
#     root.productList.clear()
#     driver = login()
#     if driver is None:
#         print("Không thể đăng nhập vào Shopee")
#         return
#     urls = generateLinks(numberOfPage, searched_product)
#     print(f"Danh sách URL: {urls}")
#     for url in urls:
#         fillProductList(root, driver, url)
#     driver.close()

def run(root, numberOfPage, searched_product):
    """Hàm chính để chạy quá trình tìm kiếm và trích xuất dữ liệu với đăng nhập"""
    root.productList.clear()

    # Đăng nhập vào Shopee
    driver = login()
    if driver is None:
        messagebox.showerror("Lỗi", "Không thể khởi tạo trình duyệt Chrome")
        return

    try:
        # Tạo danh sách URL tìm kiếm
        urls = generateLinks(numberOfPage, searched_product)

        for url in urls:
            print(f"Đang quét URL: {url}")
            fillProductList(root, driver, url)

        # Kiểm tra kết quả
        if len(root.productList) == 0:
            messagebox.showwarning("Cảnh báo", "Không tìm thấy sản phẩm nào phù hợp")
        else:
            messagebox.showinfo("Thành công", f"Đã tìm thấy {len(root.productList)} sản phẩm")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
    finally:
        # Đảm bảo đóng trình duyệt
        driver.quit()


def writeToFile(name, root):
    if len(name) == 0:
        messagebox.showerror("Error", "Bạn chưa nhập tên file")
    else:
        path = './data/shopee'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        csvFile = open(f'{path}/{name}.csv', 'w+',
                       encoding='utf-16', newline='')
        try:
            writer = csv.writer(csvFile, delimiter='\t')
            writer.writerow(
                ('Tên sản phẩm', 'Giá nhỏ nhất', 'Giá lớn nhất', 'Đánh giá sản phẩm', 'Doanh số', 'Giảm giá (%)', 'Link sản phẩm'))
            writer.writerows(root.productList)
        except:
            messagebox.showerror('ERROR', 'Đã có lỗi xảy ra!')
        finally:
            csvFile.close()
            messagebox.showinfo(
                "Sucessfully!", 'Đã lưu vào file vào thư mục data')

