from tkinter import Tk, ttk, Label, Entry, Text, Button, StringVar, END, YES, W
from ttkwidgets import CheckboxTreeview
from PIL import Image, ImageTk

import api_interface


class App:

    def __init__(self):
        self.window = Tk()

        self.im_checked = ImageTk.PhotoImage(Image.open('resources/im_checked.png'))
        self.im_unchecked = ImageTk.PhotoImage(Image.open('resources/im_unchecked.png'))

        self.sv_url_text = StringVar(self.window)
        self.sv_url_text.set('https://www.youtube.com/watch?v=67hNu3A4tts&t=554s')
        self.sv_title_text = StringVar(self.window)
        self.sv_video_id = StringVar(self.window)
        self.sv_video_len = StringVar(self.window)

        Label(self.window, text="Url").grid(row=0, column=1)
        en_url = Entry(self.window, textvariable=self.sv_url_text, width=50)
        en_url.grid(row=0, column=2)
        Label(self.window, text="Title").grid(row=1, column=1)
        en_title = Entry(self.window, textvariable=self.sv_title_text, width=50)
        en_title.grid(row=1, column=2)
        Label(self.window, text="ID").grid(row=0, column=3)
        en_id = Entry(self.window, textvariable=self.sv_video_id, width=20)
        en_id.grid(row=0, column=4)
        Label(self.window, text="Length").grid(row=1, column=3)
        en_len = Entry(self.window, textvariable=self.sv_video_len, width=20)
        en_len.grid(row=1, column=4)

        self.txt_tscript = Text(self.window, width=60, height=10)
        self.txt_tscript.grid(row=3, column=1, columnspan=5)

        self.tree = ttk.Treeview(self.window)
        self.tree.grid(row=2, column=1, columnspan=5)
        self.tree["columns"] = ("time", "text", "duration")
        self.tree.column("#0", stretch=YES, width=45)
        self.tree.column("time", stretch=YES, width=100)
        self.tree.column("text", stretch=YES, width=300)
        self.tree.column("duration", stretch=YES, width=100)
        self.tree.heading("#0", text="Check", anchor=W)
        self.tree.heading("time", text="Timestamp", anchor=W)
        self.tree.heading("text", text="Text", anchor=W)
        self.tree.heading("duration", text="duration", anchor=W)
        self.tree.tag_configure("unchecked", image=self.im_unchecked)
        self.tree.tag_configure("checked", image=self.im_checked)
        self.tree.bind('<Button 1>', self.toggle_checked)

        bt_find_video = Button(self.window, text='find', command=self.cb_find_video)
        bt_find_video.grid(row=0, column=5)
        bt_select_vid = Button(self.window, text='generate links', command=self.cb_select_video)
        bt_select_vid.grid(row=1, column=5)

    def start(self):
        self.window.mainloop()

    def cb_select_from_table(self):
        self.tree

    def cb_find_video(self):
        url = self.sv_url_text.get()
        (response, details) = api_interface.get_video_by_url(url)
        print(response)
        print(details)

        id = response['items'][0]['id']
        self.sv_video_id.set(id)
        title = response['items'][0]['snippet']['title']
        self.sv_title_text.set(title)
        duration = details['items'][0]['contentDetails']['duration']
        self.sv_video_len.set(duration)

        tscripts = api_interface.get_transcript_by_id(id)
        print(tscripts)

        self.txt_tscript.delete('1.0', END)
        for elem in tscripts:
            self.txt_tscript.insert(END, f"{elem['start']} : {elem['text']} : {elem['duration']}\n")

        self.populate_grid(tscripts)

    def cb_select_video(self):
        checked = []
        children = self.tree.get_children()
        for child in children:
            tag = self.tree.item(child, 'tags')[0]
            if tag == 'checked':
                checked.append(child)
        print(checked)

    def populate_grid(self, entries):
        count = 0
        self.tree.delete(*self.tree.get_children())
        for item in entries:
            self.tree.insert("", index="end", values=(item['start'], item['text'], item['duration']), tag='unchecked')
            count += 1

    def toggle_checked(self, event):
        rowid = self.tree.identify_row(event.y)
        tag = self.tree.item(rowid, 'tags')[0]
        tags = list(self.tree.item(rowid, 'tags'))
        tags.remove(tag)
        self.tree.item(rowid, tags=tags)
        if tag == 'checked':
            self.tree.item(rowid, tags='unchecked')
        else:
            self.tree.item(rowid, tags="checked")

