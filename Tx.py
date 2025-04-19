import time
import os

# Hàm delay
def delay(seconds):
    time.sleep(seconds)

# Xóa màn hình console
def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"Lỗi khi xóa màn hình: {e}")

# Phân tích và dự đoán
def analyze_and_predict(history: list) -> tuple:
    """
    Phân tích lịch sử và dự đoán kết quả tiếp theo.
    - Lịch sử: 5 kết quả gần nhất (viết tắt Tài = T, Xỉu = X).
    - Trả về: Dự đoán ("Tài" hoặc "Xỉu") và xác suất.
    """
    if len(history) != 5:
        return "Không đủ dữ liệu", 50

    # Quy luật cầu
    patterns = {
        "bệt": lambda h: h.count(h[-1]) >= 3,  # Cầu bệt (>= 3 lần liên tục)
        "đảo_1_1": lambda h: all(h[i] != h[i + 1] for i in range(4)),  # Cầu đảo 1-1
        "kép_2_2": lambda h: h[:2] == h[2:] and h[:2] in [["Tài", "Tài"], ["Xỉu", "Xỉu"]],
        "1_2_3": lambda h: h[:1] == h[1:3] and h[3:] == [h[1]] * 2,  # Cầu 1-2-3
        "3_3": lambda h: h[:3] == [h[0]] * 3 and h[3:] == [h[3]] * 3,  # Cầu 3-3
        "4_3_2_1": lambda h: h == ["Tài"] * 4 + ["Xỉu"] * 3 + ["Tài"] * 2 + ["Xỉu"],  # Cầu 4-3-2-1
        "inverse_pattern": lambda h: h.count("Tài") >= 4 and h[-1] == "Xỉu",  # Cầu ngược chiều
        "fixed_cycle": lambda h: h[:5] == h[5:10] if len(h) >= 10 else False,  # Cầu chu kỳ cố định
        "reverse_alternating": lambda h: h[:2] == h[2:4] and h[4:] == h[:2],  # Cầu đảo ngược
        "synchronized_pattern": lambda h: len(set(h)) == 1 and h[0] in ["Tài", "Xỉu"],  # Cầu đồng bộ
        "u_shaped": lambda h: h[0] == "Tài" and h[-1] == "Tài" and h[1] == "Xỉu" and h[2] == "Xỉu",  # Cầu kiểu chữ U
        "multiples_pattern": lambda h: len(set(h)) == 2 and h.count("Tài") == 2 and h.count("Xỉu") == 2,  # Cầu bội số
        "parallel_pattern": lambda h: h[:3] == ["Tài"] * 3 and h[3:] == ["Xỉu"] * 3,  # Cầu song song
        "wavy_pattern": lambda h: all(h[i] != h[i + 1] for i in range(len(h) - 1)),  # Cầu gập ghềnh
        "xiu_tai_ratio": lambda h: h.count("Xỉu") == 2 and h.count("Tài") == 1,  # Tỷ lệ Xỉu/Tài
        "tai_tai_xiu_xiu": lambda h: h[:2] == ["Tài"] * 2 and h[2:4] == ["Xỉu"] * 2,  # Cầu Tài-Tài-Xỉu-Xỉu
        # Thêm các quy luật cầu phức tạp hơn
        "bệt_kép": lambda h: h[:2] == h[2:4] and h[:2] in [["Tài", "Tài"], ["Xỉu", "Xỉu"]],  # Cầu bệt kép
        "xoay_chieu": lambda h: h[0] == "Xỉu" and h[4] == "Tài",  # Cầu xoay chiều (Xỉu đầu, Tài cuối)
        "thẳng": lambda h: h == ["Tài", "Tài", "Tài", "Tài", "Tài"],  # Cầu thẳng
        "xiu_quay": lambda h: h[:2] == ["Xỉu", "Xỉu"] and h[2:4] == ["Tài", "Tài"],  # Cầu Xỉu quay
        "tăng_dần": lambda h: h == sorted(h),  # Cầu tăng dần
        "giảm_dần": lambda h: h == sorted(h, reverse=True),  # Cầu giảm dần
        "lặp_lại": lambda h: len(set(h)) == 1,  # Cầu lặp lại
        "3_2": lambda h: h[:3] == ["Tài"] * 3 and h[3:] == ["Xỉu"] * 2,  # Cầu 3 Tài 2 Xỉu
        "2_3": lambda h: h[:2] == ["Tài"] * 2 and h[2:] == ["Xỉu"] * 3,  # Cầu 2 Tài 3 Xỉu
        "quay_lại": lambda h: h[:2] == ["Xỉu", "Tài"],  # Cầu quay lại
        "đa_dạng": lambda h: h[0] != h[1] and h[1] != h[2] and h[2] != h[3] and h[3] != h[4],  # Cầu đa dạng
        "cầu_công": lambda h: h.count("Tài") == 3 and h.count("Xỉu") == 2,  # Cầu công
        "đảo_chieu": lambda h: h == ["Xỉu", "Tài", "Xỉu", "Tài", "Xỉu"],  # Cầu đảo chiều Xỉu-Tài
        "mắc_kép": lambda h: h[:2] == h[2:4] and h[:2] == ["Tài", "Tài"],  # Mắc cầu Tài kép
        "kiểu_lắc": lambda h: h[0] == "Tài" and h[-1] == "Xỉu" and len(set(h)) == 2,  # Cầu lắc
        # Tiếp tục thêm nhiều quy luật phức tạp...
    }

    predictions = {"Tài": 0, "Xỉu": 0}

    # Nhận diện cầu và dự đoán
    for name, rule in patterns.items():
        if rule(history):
            if name == "bệt":
                predictions[history[-1]] += 3  # Cầu bệt tăng trọng số cho kết quả hiện tại
            elif name == "đảo_1_1":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 3
            elif name == "kép_2_2":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 2
            elif name == "1_2_3":
                predictions[history[-1]] += 2
            elif name == "3_3":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 2
            elif name == "4_3_2_1":
                next_prediction = "Xỉu" if history[-1] == "Tài" else "Tài"
                predictions[next_prediction] += 4
            elif name == "inverse_pattern":
                next_prediction = "Xỉu" if history[-1] == "Tài" else "Tài"
                predictions[next_prediction] += 4
            elif name == "fixed_cycle":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 2
            elif name == "reverse_alternating":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 2
            elif name == "synchronized_pattern":
                predictions[history[-1]] += 3
            elif name == "u_shaped":
                next_prediction = "Xỉu"
                predictions[next_prediction] += 3
            elif name == "multiples_pattern":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 3
            elif name == "parallel_pattern":
                next_prediction = "Xỉu"
                predictions[next_prediction] += 3
            elif name == "wavy_pattern":
                next_prediction = "Xỉu" if history[-1] == "Tài" else "Tài"
                predictions[next_prediction] += 2
            elif name == "xiu_tai_ratio":
                next_prediction = "Tài" if history[-1] == "Xỉu" else "Xỉu"
                predictions[next_prediction] += 3
            elif name == "tai_tai_xiu_xiu":
                next_prediction = "Xỉu"
                predictions[next_prediction] += 3

    # Tính tổng trọng số
    total = predictions["Tài"] + predictions["Xỉu"]
    if total == 0:
        counts = {"Tài": history.count("Tài"), "Xỉu": history.count("Xỉu")}
        if counts["Tài"] > counts["Xỉu"]:
            return "Tài", 60
        elif counts["Tài"] < counts["Xỉu"]:
            return "Xỉu", 60
        else:
            return "Tài", 50

    tai_percentage = (predictions["Tài"] / total) * 100
    xiu_percentage = (predictions["Xỉu"] / total) * 100

    if tai_percentage > xiu_percentage:
        return "Tài", tai_percentage
    else:
        return "Xỉu", xiu_percentage

# Chuyển đổi từ viết tắt sang đầy đủ
def convert_history(input_str: str) -> list:
    mapping = {"T": "Tài", "X": "Xỉu"}
    try:
        return [mapping[char] for char in input_str.upper()]
    except KeyError:
        return []

# Hàm chính
def main():
    clear_screen()

    while True:
        input_str = input("Nhập 5 kết quả gần nhất (viết tắt: T = Tài, X = Xỉu, ví dụ: TXTXT): ").strip()
        history = convert_history(input_str)
        if len(history) != 5:
            print("Vui lòng nhập đúng định dạng (5 ký tự, T hoặc X).")
            continue

        # Thực hiện phân tích trong 10 giây
        print("Đang phân tích, vui lòng chờ trong 10 giây...")
        delay(10)  # Chờ 10 giây

        prediction, confidence = analyze_and_predict(history)
        print(f"Dự đoán: {prediction}, Xác suất: {confidence:.2f}%")

        actual_result = input("Nhập kết quả thực tế (viết tắt: T = Tài, X = Xỉu): ").strip().upper()
        if actual_result not in ["T", "X"]:
            print("Kết quả nhập không hợp lệ. Bỏ qua phiên này.")
            continue

        actual_result = "Tài" if actual_result == "T" else "Xỉu"
        print(f"Kết quả thực tế: {actual_result}. Bạn đã {'thắng' if prediction == actual_result else 'thua'}!")

        delay(2)
        clear_screen()

if __name__ == "__main__":
    main()
