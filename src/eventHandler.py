from tkinter import messagebox
from shopeeFunctions import *
from imageFunctions import *
# def accessToShopee(root, numberOfPage, searched_product):
#     if len(searched_product) == 0:
#         messagebox.showwarning('Warning', 'Bạn chưa điền thông tin!')
#     else:
#         # try:
#         root.showProgressBar()
#         numberOfPage = int(numberOfPage)
#         run(root, numberOfPage, searched_product)
#         root.endProgressBar()
#         if len(root.productList) != 0:
#             root.showProducts()
#         else:
#             messagebox.showerror('Error', 'Có lỗi xảy ra\nVui lòng kiểm tra lại')
#         # except:
#         #     messagebox.showerror('Error', 'Có lỗi xảy ra\nVui lòng kiểm tra lại')

def accessToShopee(root, numberOfPage, searched_product):
    if len(searched_product) == 0:
        messagebox.showwarning('Warning', 'Bạn chưa điền thông tin!')
    else:
        try:
            print(f"Bắt đầu tìm kiếm: {searched_product}, số trang: {numberOfPage}")
            root.showProgressBar()
            numberOfPage = int(numberOfPage)
            run(root, numberOfPage, searched_product)
            print(f"Số sản phẩm tìm thấy: {len(root.productList)}")
            root.endProgressBar()
            if len(root.productList) != 0:
                root.showProducts()
            else:
                messagebox.showerror('Error', 'Có lỗi xảy ra\nKhông tim thấy sản phẩm nào')
        except Exception as e:
            root.endProgressBar()
            messagebox.showerror('Error', f'Có lỗi xảy ra: {str(e)}\nVui lòng kiểm tra lại')

def writeProduct():
    writeToFile()

    
def downloadImages(root, url, path, limit):
    if limit == '':
        limit = 10 ** 6
    else:
        try:
            limit = int(limit)
        except:
            messagebox.showerror('Error', 'Mời bạn nhập đúng định dạng')
            return
    root.showProgressBar()
    getImage(url, path, limit)
    root.endProgressBar()
    response = messagebox.askokcancel("Successfully","Bạn có muốn mở thư mục không?")
    if response == 1 : showFolder()


            