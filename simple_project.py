from cam import selfi

location = selfi()


import easyocr
reader = easyocr.Reader(['ko'],user_network_directory='./user_network') 

result = reader.readtext(location)

print(result)