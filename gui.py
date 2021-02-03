from tkinter import Tk, Label, Entry, Text, Button, StringVar, END

import api_interface

class App():
    def __init__(self):
        self.window = Tk()

        Label(self.window, text="Url").grid(row=0)
        Label(self.window, text="Title").grid(row=1)

        self.sv_url_text = StringVar(self.window)
        self.sv_url_text.set('https://www.youtube.com/watch?v=-194OAphI-M')
        self.sv_title_text = StringVar(self.window)

        en_url = Entry(self.window, textvariable=self.sv_url_text, width=50)
        en_url.grid(row=0, column=1)
        en_title = Entry(self.window, textvariable=self.sv_title_text, width=50)
        en_title.grid(row=1, column=1)

        self.txt_tscript = Text(self.window, width=100, height=50)
        self.txt_tscript.grid(row=2, column=1)

        bt_find_video = Button(self.window, text='find', command=self.cb_find_video)
        bt_find_video.grid(row=0, column=2)




    def start(self):
        self.window.mainloop()

    def cb_find_video(self):
        url = self.sv_url_text.get()
        response = api_interface.get_video_by_url(url)
        print(response)
        title = response['items'][0]['snippet']['title']
        id = response['items'][0]['id']
        self.sv_title_text.set(title)
        tscripts = api_interface.get_transcript_by_id(id)
        print(tscripts)
        for elem in tscripts:
            self.txt_tscript.insert(END, f"{elem['start']} : {elem['text']}\n")
