try:
    import Tkinter as tk
    from Tkinter.ttk import *
    from Tkinter import *
    from Tknter import filedialog, Menu

except ImportError: # Python 3
    import tkinter as tk
    from tkinter.ttk import *
    from tkinter import *
    from tkinter import filedialog, Menu
    from tkinter.messagebox import showinfo
import bluetooth

def get_device_nearby():

    target_name = 'HUNG-WEI 的 iPhone' #--- 特定裝置名稱 ---#
    target_address = None

    #--- 尋找附近藍牙訊號 ---#
    nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5)

    device_text = ''

    for device in nearby_devices:
        device_text = device_text + 'Name:{}, Address:{}\n'.format(device[1], device[0])

    result_label.configure(text='Could not find any device' if device_text == '' else device_text, foreground='white')

    #--- 查看是否有符合的目標 ---#
    for detail in nearby_devices:
        if target_name == detail[1]:
            target_address = detail[0]
            break

    if target_address is not None:
        print('found target bluetooth device with address {}'.format(target_address))
    else:
        print('could not find target bluetooth device nearby')

def write_in_str_to_device(string, addr):

    port = 3 

    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((addr, port)) #--- 連上裝置 ---#

    sock.send(b'{}'.format(string)) #--- 寫入字串 ---#

    sock.close()

def listen_to_device_podcast():

    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 6
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print('Accepted connection from {}', address)

    data = client_sock.recv(1024)
    print('received [{}]'.format(data))

    client_sock.close()
    server_sock.close()

window = tk.Tk()
window.title('MCU+IC Temperature Sensor')
window.configure(background='white')

#--- 窗口尺寸 ---#
window.geometry('500x300')

#--- 標題初始化 ---#
# header_label = tk.Label(window, text='MCU+IC Temperature Sensor', width='500', height='1', font=('Helvetica-Light', 15))
# header_label.pack()

#--- 結果顯示 ---#
result_label = tk.Label(window, width=50, height=7, bg="black")
result_label.pack(fill=X, pady=20)

#--- 取得附近藍芽裝置 ---#
device_nearby_btn = tk.Button(window, text='Device Nearby', command=get_device_nearby, width='30', height='2', font='Helvetica-Light')
device_nearby_btn.pack()

#--- 取得溫度 ---#
tmp_btn = tk.Button(window, text='Temperature', command=get_device_nearby, width='30', height='2', font='Helvetica-Light')
tmp_btn.pack()

#--- 取得電壓值 ---#
adc_btn = tk.Button(window, text='Voltage', command=get_device_nearby, width='30', height='2', font='Helvetica-Light')
adc_btn.pack()

#--- 取得封包 ---#
nif_btn = tk.Button(window, text='NIF', command=get_device_nearby, width='30', height='2', font='Helvetica-Light')
nif_btn.pack()

window.mainloop()

