import subprocess
import sys

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"Lỗi khi xóa màn hình: {e}")

def a1():
    return True

def b2():
    return "Ẩn!"

def c3(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

p1 = ['hashlib']
for p in p1:
    try:
        __import__(p)
    except ImportError:
        c3(p)

def d4(s):
    x = int(s, 16)
    y = x % 100
    z = 100 - y
    return y, z

def e5(md5_input):
    if len(md5_input) != 32:
        return False
    return all(c in '0123456789abcdef' for c in md5_input.lower())

def f6():
    while True:
        inp = input("@Nopermcc vui lòng gửi mã MD5 : ")
        if inp.lower() == "thoat":
            print("Chương trình kết thúc.")
            break
        if not e5(inp):
            print("đéo phải mã MD5 !!!")
            continue
        t, x = d4(inp)
        output = f" kết quả TÀI🔴🎲🎲 : {t:.2f}%\n kết quả XỈU🟢🎲🎲: {x:.2f}%"
        print(output)
        print("-" * 30)

def g7():
    a1()
    b2()
    f6()

if __name__ == "__main__":
    g7()
