import cv2
import sys
import datetime as dt
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from tkinter import messagebox
from tkinter import ttk
import telebot
from PIL import ImageTk, Image
import math

from ultralytics import YOLO
import cvzone



model = YOLO("nano.pt")
#global A
#global B
#global C
#global D
#global E
#global conf
global clss
global currentClass
global global_token

global_token = '0'
bot = telebot.TeleBot('6613003847:AAEgJ0-Fv-rWETllnN8WwH7eyZGSeTOL8zc')


def get_time():
    time = datetime.now()
    return time

def exit_func():
    sys.exit()


def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(dt.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    progress_value.set(int(vid_player.current_duration()))


def load_video():
    global conf
    global A
    global B
    global C
    global D
    global E
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0

    global clss
    global currentClass
    file_path = filedialog.askopenfilename()
    frame = ttk.Frame(tab_1, width=720, height=720)

    frame.grid(column=0, row=1, columnspan=2, sticky="NSEW", padx=7, pady=2)

    video_path = file_path
    cap = cv2.VideoCapture(video_path)

    label = ttk.Label(frame)
    label.grid(column=0, row=1, columnspan=2, sticky="NSEW", padx=7, pady=2)

    def next_frame():
        global clss
        global currentClass
        global global_token
        global conf

        ret, frame = cap.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)

            results = model(frame)

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    classNames = ['Brick', 'Concrete', 'Empty body', 'Soil', 'Wood']
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    w, h = x2 - x1, y2 - y1
                    cvzone.cornerRect(frame, (x1, y1, w, h), l=15)

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    clss = int(box.cls[0])
                    currentClass = classNames[clss]
                    if currentClass == 'Brick' or currentClass == 'Concrete' or currentClass == 'Empty body' or currentClass == 'Soil' or currentClass == 'Wood' and conf > 0.4:
                        cvzone.putTextRect(frame, f"{classNames[clss]} {conf}", (max(0, x1), max(35, y1)),
                                           scale=3, thickness=0, offset=2)
                        cvzone.cornerRect(frame, (x1, y1, w, h), l=15)

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(image=image)
            cv2.waitKey(1)

            label.configure(image=image_tk)
            label.image = image_tk

            root.after(30, next_frame)
        else:
            return
            # cap.release()
            # cv2.destroyAllWindows()
            # root.destroy()

    next_frame()


    if currentClass == 'Concrete' and conf > 0.4 and A == 0:
        with open("list.txt", 'w') as file:
            file.write(f"Время въезда: {get_time()}. Тип груза: Бетон \n")
        result_label = ttk.Label(
            label_frame,
            text=f"Время въезда: {get_time()}\nТип груза: Бетон",
            justify="left",
            font=("-size", 10, "-weight", "bold"),
        )
        result_label.grid(row=1, column=2, columnspan=1, sticky="N")
        bot.send_message(chat_id=global_token, text=f"Время въезда: {get_time()} \n Тип отходов в грузовике: Бетон")
        A = 1
        B = 0
        C = 0
        D = 0
        E = 0

    if currentClass == 'Brick'  and B == 0:
        with open("list.txt", 'w') as file:
            file.write(f"Время въезда: {get_time()}. Тип груза: Кирпичи \n")
        result_label = ttk.Label(
            label_frame,
            text=f"Время въезда: {get_time()}\nТип груза: Кирпичи",
            justify="left",
            font=("-size", 10, "-weight", "bold"),
        )
        result_label.grid(row=1, column=2, columnspan=1, sticky="N")
        bot.send_message(chat_id=global_token, text=f"Время въезда: {get_time()} \n Тип отходов в грузовике: Кирпичи")
        A = 0
        B = 1
        C = 0
        D = 0
        E = 0

    if currentClass == 'Empty body' and C == 0:
        with open("list.txt", 'w') as file:
            file.write(f"Время въезда: {get_time()}. В кузове грузовика нет отходов \n")
        result_label = ttk.Label(
            label_frame,
            text=f"Время въезда: {get_time()}. \n В кузове грузовика нет отходов",
            justify="left",
            font=("-size", 10, "-weight", "bold"),
        )
        result_label.grid(row=1, column=2, columnspan=1, sticky="N")
        bot.send_message(chat_id=global_token, text=f"Время въезда: {get_time()} \n В кузове грузовика нет отходов")
        A = 0
        B = 0
        C = 1
        D = 0
        E = 0

    if currentClass == 'Soil'  and D == 0:
        with open("list.txt", 'w') as file:
            file.write(f"Время въезда: {get_time()}.Тип груза: Грунт \n")
        result_label = ttk.Label(
            label_frame,
            text=f"Время въезда: {get_time()}\nТип груза: Грунт",
            justify="left",
            font=("-size", 10, "-weight", "bold"),
        )
        result_label.grid(row=1, column=2, columnspan=1, sticky="N")
        bot.send_message(chat_id=global_token, text=f"Время въезда: {get_time()} \n Тип отходов в грузовике: Грунт")
        A = 0
        B = 0
        C = 0
        D = 1
        E = 0

    if currentClass == 'Wood'  and E == 0:
        with open("list.txt", 'w') as file:
            file.write(f"Время въезда: {get_time()}.Тип груза: Дерево \n")
        result_label = ttk.Label(
            label_frame,
            text=f"Время въезда: {get_time()} \nТип груза: Дерево",
            justify="left",
            font=("-size", 10, "-weight", "bold"),
        )
        result_label.grid(row=1, column=2, columnspan=1, sticky="N")
        bot.send_message(chat_id=global_token, text=f"Время въезда: {get_time()} \n Тип отходов в грузовике: Дерево")
        A = 0
        B = 0
        C = 0
        D = 0
        E = 1

    file.close()
    if file_path:
        vid_player.load(video_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def seek(value):
    vid_player.seek(int(value))



def play_pause():
        vid_player.play()

def video_ended(event):
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)


def on_token_entered():
    global global_token
    global_token = entry.get()
    #
    # проверка токена
    #
    messagebox.showinfo('Введенный токен', f'Вы ввели токен: {global_token}')




root = tk.Tk()
root.title("File_creat_zero")
root.geometry('1920x1080')
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=2)
root.rowconfigure(2, weight=1)

root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

check_frame = ttk.LabelFrame(root, text="Введите токен", padding=(10, 5))
check_frame.grid(
    row=0, column=0, columnspan=3,  sticky="nsew"
)
entry = ttk.Entry(check_frame)
entry.grid(row=0, column=0, columnspan=2, padx=15, pady=(0, 2), sticky="w")

token_btn = ttk.Button(check_frame, text='OK', style="Accent.TButton", command=on_token_entered)
token_btn.grid(column=2, row=0, columnspan=1, padx=(5, 5), sticky="e")

exit_btn = ttk.Button(check_frame, text='Выход', style="Accent.TButton", command=exit_func)
exit_btn.grid(column=3, row=0, columnspan=1, padx=(5, 5), sticky="E")


paned = ttk.PanedWindow(root)
paned.grid(row=1, column=0, columnspan=3, sticky="nsew", rowspan=3)
pane = ttk.Frame(paned, padding=5)
paned.add(pane, weight=3)

notebook = ttk.Notebook(pane)
notebook.pack(fill="both", expand=True)

tab_1 = ttk.Frame(notebook)
tab_1.rowconfigure(1, weight=1)
tab_1.columnconfigure(0, weight=2)
tab_1.columnconfigure(1, weight=2)
tab_1.columnconfigure(2, weight=2)
notebook.add(tab_1, text="Загрузка")

load_btn = ttk.Button(tab_1, text="Load", style="Accent.TButton", command=load_video)
load_btn.grid(column=0, row=0, columnspan=1, padx=5, sticky="NSEW")

vid_player = TkinterVideo(scaled=bool(1), master=tab_1, borderwidth=1, relief="solid")
vid_player.set_size((385, 615))
vid_player.grid(column=0, row=1, columnspan=2, sticky="NSEW", padx=7, pady=2)

label_frame = ttk.LabelFrame(tab_1, text="Результаты:", padding=(10, 5))
label_frame.grid(
    row=1, column=2, columnspan=3, padx=(10, 5), pady=(10, 5), sticky="nsew")

progress_value = tk.IntVar(tab_1)

progress_slider = tk.Scale(tab_1, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.grid(column=0, row=3, columnspan=3, padx=5, pady=5, sticky="NSEW")
progress_slider.config(state = tk.DISABLED)

vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)

end_time = tk.Label(tab_1, text=str(dt.timedelta(seconds=0)))
end_time.grid()

play_pause_btn = ttk.Button(tab_1, text="Play", style="Accent.TButton", command=play_pause)
play_pause_btn.grid(column=0, row=4, columnspan=1, padx=5, pady=5, sticky="NSEW")


vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)


root.mainloop()

# bot.send_message(chat_id=token, text=f"Время въезда: {tm} \n Тип отходов в грузовике: {material}")
