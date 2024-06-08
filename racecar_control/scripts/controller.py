import subprocess
import os
import sys

# 保存当前运行的子进程
process1 = None
process2 = None

## Start program1.py
def start_program1():
    global process1
    if process1 is not None:
        process1.terminate()
        process1.wait()
    process1 = subprocess.Popen(['gnome-terminal', '--', 'python3', 'keyboard_teleop_2.py'])
    print("Started program1.py")

def start_program2():
    global process2
    if process2 is not None:
        process2.terminate()
        process2.wait()
    process2 = subprocess.Popen(['gnome-terminal', '--', 'python3', 'autoparking.py'])
    print("Started program2.py")

def stop_program1():
    global process1
    if process1 is not None:
        close_window("Terminal")
        process1 = None
        print("Stopped program1.py")

def stop_program2():
    global process2
    if process2 is not None:
        close_window("Terminal")
        process2 = None
        print("Stopped program2.py")

def close_window(window_title):
    try:
        # 列出所有窗口
        list_result = subprocess.run(['wmctrl', '-l'], check=True, capture_output=True, text=True)
        windows = list_result.stdout
        print("Current windows:\n", windows)
        
        # 查找包含指定标题的窗口ID
        for line in windows.splitlines():
            if window_title in line:
                window_id = line.split()[0]
                print(f"Found window ID: {window_id} for title: {window_title}")
                # 使用窗口ID关闭窗口
                result = subprocess.run(['wmctrl', '-i', '-c', window_id], check=True, capture_output=True, text=True)
                print(f"Closed window: {window_title}")
                print("wmctrl output:", result.stdout)
                return
        print(f"No window found with title: {window_title}")
    except subprocess.CalledProcessError as e:
        print(f"Error while closing window: {e}")
        print("wmctrl output:", e.output)
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    print("Press 'y' to start program1, 'u' to start program2, 'h' to stop program1, 'j' to stop program2, 'q' to quit.")
    while True:
        command = input("Enter command: ")
        if command == 'y':
            start_program1()
        elif command == 'u':
            start_program2()
        elif command == 'h':
            stop_program1()
        elif command == 'j':
            stop_program2()
        elif command == 'q':
            if process1 is not None:
                process1.terminate()
                process1.wait()
            if process2 is not None:
                process2.terminate()
                process2.wait()
            break
        else:
            print("Unknown command. Use 'y' to start program1, 'u' to start program2, 'h' to stop program1, 'j' to stop program2, 'q' to quit.")

if __name__ == '__main__':
    main()
