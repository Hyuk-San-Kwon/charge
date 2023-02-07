import easyocr
reader = easyocr.Reader(['ko'],user_network_directory='./user_network', )#gpu=False) 

result = reader.readtext('번호판.jpeg')
print(result)