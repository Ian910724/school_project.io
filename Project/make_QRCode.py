import uuid
import os
import qrcode

def generate_serial_number():
    identifier = "ID"  # 自定義辨識碼
    random_uuid = uuid.uuid4()
    most_significant_bits = random_uuid.int >> 64
    least_significant_bits = random_uuid.int & ((1 << 64) - 1)

    # 合併 most_significant_bits 和 least_significant_bits 為 128 位的字串
    combined_bits = format(most_significant_bits, 'x') + format(least_significant_bits, 'x')

    # 確保總長度為 32 個字元，不足的部分用 0 填充
    padded_combined_bits = combined_bits.zfill(32)

    # 最終的流水號
    serial_number = f"{identifier}{padded_combined_bits[:8]}-{padded_combined_bits[8:12]}-{padded_combined_bits[12:16]}-{padded_combined_bits[16:20]}-{padded_combined_bits[20:]}"
    
    return serial_number

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join("data_base", data))

def main():
    serial_number = generate_serial_number()
    generate_qr_code(serial_number)
    print("QR code generated with serial number:", serial_number)

    with open("data_base/output.html", "a") as file:
        file.write(serial_number + "\n")
        print("Serial number added to output.txt")

if __name__ == "__main__":
    main()
