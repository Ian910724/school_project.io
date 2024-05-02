from __future__ import print_function
import setting as blescan
import sys
import time
import bluetooth._bluetooth as bluez

def check_uuid_in_file(uuid):
    try:
        with open("data_base/output.html", "r") as file:
            for text in file:
                if uuid.strip() == text.strip():
                    return uuid
    except Exception as e:
        print("Error:", e)
        return None

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("BLE thread started")

except Exception as e:
    print("Error accessing bluetooth device:", e)
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    returnedList = blescan.parse_events(sock, 10)
    rssiDict = {}
    for item in returnedList:
        itemList = item.split(',')
        #itemKey = itemList[1] + ':' + str(itemList[2]) + ':' + str(itemList[3])
        LowerItemList = itemList[1].lower()
        # itemKey = "ID" +  LowerItemList[:8] + "-" + LowerItemList[8:12] + "-" + LowerItemList[12:16] + "-" + LowerItemList[16:20] + "-" + LowerItemList[20:]
        itemKey = LowerItemList[:8] + "-" + LowerItemList[8:12] + "-" + LowerItemList[12:16] + "-" + LowerItemList[16:20] + "-" + LowerItemList[20:]
        if itemKey in rssiDict:
            rssiDict[itemKey]['count'] += 1
            rssiDict[itemKey]['total_rssi'] += int(itemList[-1])
        else:
            rssiDict[itemKey] = {'count': 1, 'total_rssi': int(itemList[-1])}

    print("Detected BLE devices:")
    for mac_address, data in rssiDict.items():
        average_rssi = data['total_rssi'] / data['count']
        print("MAC Address:", mac_address, "- Average RSSI:", average_rssi)
        
        # 檢查UUID並返回
        uuid = mac_address.strip()
        matched_uuid = check_uuid_in_file(uuid)
        if matched_uuid:
            with open("data_base/passenger.html", "a") as file:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                file.write(matched_uuid + "\t" + current_time + "\n")
            print("Found matched UUID:", matched_uuid)
        else:
                print("Matched Failed\n")
    print("--------------------")
    time.sleep(1)
