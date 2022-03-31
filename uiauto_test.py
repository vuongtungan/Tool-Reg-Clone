from uiautomator import Device

d = Device('emulator-5554', adb_server_host='127.0.0.1', adb_server_port=5037)

#print(d(text="Lite").info)

d(text="Lite").click()