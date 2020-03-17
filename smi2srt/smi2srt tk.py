import re
import tkinter
from tkinter.ttk import Progressbar, Button
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import Open, SaveAs
from tkinter.constants import *
from datetime import timedelta


tk = tkinter.Tk()
tk.title('smi2srt Converter')
tk.wm_minsize(900, 700)
ico = tkinter.PhotoImage(file='convert.ico')
tk.iconphoto(True, ico)


def file_open():
    file_types = (
                ("Subtitle files", "*.smi", "TEXT"),
                ("Text files", "*.txt", "TEXT"),
                ("All files", "*"),
            )
    file = Open(parent=tk, filetypes=file_types)
    link = file.show()
    if link:
        st.delete(0.0, END)
        ts.delete(0.0, END)
        with open(link, 'r') as f:
            for line in f.readlines():
                yield line


def write():
    for text in file_open():
        st.insert(INSERT, text)


def save():
    file_types = (
                ("Subtitle files", "*.srt", "TEXT"),
                ("Text files", "*.txt", "TEXT"),
                ("All files", "*"),
            )
    file = SaveAs(parent=tk, filetypes=file_types)
    link = file.show()
    if link:
        with open(link, 'w') as f:
            f.write(ts.get(0.0, END))
    

def about():
    from tkinter.ttk import Button
    
    top = tkinter.Toplevel(tk, bg='white')
    top.title('About')
    top.transient(tk)
    lb = tkinter.Label(top, text='''Subtitle converter created
to convert subtitle file 
from smi format to srt 
format.

Created by
Kudakwashe Ndokanga''', bg='white')
    lb.place(relwidth=1, relheight=0.8)
    Button(top, text='OK', default='active', command=top.destroy).place(rely=0.8375, relx=0.8, relheight=0.125,
                                                                        anchor='n')
    return None


def help_():
    from tkinter.ttk import Button

    top = tkinter.Toplevel(tk, bg='white')
    top.title('Help')
    top.transient(tk)
    lb = tkinter.Label(top, text='''*Convert*
Converts smi data in left 
section to srt data which
is displayed in the right 
section.

*Note*
Input can also be achieved
by simply writing the smi data
manually into the left section.''', bg='white')
    lb.place(relwidth=1, relheight=0.8)
    Button(top, text='OK', default='active', command=top.destroy).place(rely=0.8375, relx=0.8, relheight=0.125,
                                                                        anchor='n')
    return None


frame0 = tkinter.Frame(tk, relief='flat', borderwidth=2, bg='black')
frame0.place(relwidth=1, relheight=0.95, rely=0)

frame1 = tkinter.Frame(tk, relief='flat', borderwidth=2, bg='#003300')
frame1.place(relwidth=1, relheight=0.05, rely=0.95)

st = ScrolledText(frame0, bg='white', fg='darkred', wrap=WORD)
st.place(relwidth=0.6, relheight=1)
ts = ScrolledText(frame0, bg='white', fg='darkblue', wrap=WORD)
ts.place(relx=0.6, relwidth=0.4, relheight=1)
    

pb = Progressbar(frame1, maximum=100, mode='determinate', value=0)
pb.place(relwidth=0.65, relheight=0.9, rely=0.05, relx=0.33)

menus = (
    ("File", (
        ("Open   Ctrl+O", write),
        ("Save    Ctrl+S", save),
        ("Exit      Alt+F4", tk.destroy)
    )
    ),
    ("Help", (
        ("View Help", help_),
        ("About Converter", about)
    )
    )
)

menu_bar = tkinter.Menu(tk, bg='black', fg='white')
for menu in menus:
    m = tkinter.Menu(tk)
    m.add_command(label='Open', command=write)
    for item in menu[1]:
        m.add_command(label=item[0], command=item[1])
    menu_bar.add_cascade(label=menu[0], menu=m)
tk['menu'] = menu_bar

tk.bind('<Control-Key-o>', write)
tk.bind('<Control-Key-O>', write, '+')
tk.bind('<Control-Key-s>', save)
tk.bind('<Control-Key-S>', save, '+')
tk.bind('<F1>', help_)


def content():
    ent1 = re.sub(r'&#39;', "'", st.get(0.0, END))
    ent2 = re.sub(r'&#40;', '"', ent1)
    # content seeking
    ent3 = re.findall(r'(?<=SYNC\s)Start=.*?<SYNC|(?<=SYNC\s)Start=.*?</body', ent2, re.DOTALL)
    # filter and concatenation of strings
    ent4 = [re.sub(r'\n', ' ', item0) for item0 in ent3]
    ent5 = []
    for item0 in ent4:
        a = re.findall(r'>.*?<', item0)
        b = [c for c in a if c != '><']
        d = []
        for e in b:
            f = re.search(r'[^>].*[^<]', e)
            # filter of None values
            if bool(f) is True:
                d.append(f.group())
            else:
                continue
        g = ''.join(d)
        ent5.append(g)
    for item0 in ent5:
        if bool(re.match(r'.+', item0)) is not True:
            yield '......'
        else:
            yield item0


def time():
    ent1 = re.sub(r'&#39;', "'", st.get(0.0, END))
    ent2 = re.sub(r'&#40;', '"', ent1)
    # define search for times
    a = re.findall(r'Start=[\d]+', ent2)
    # add times to list
    b = [(re.search(r'[\d]+', item0)).group() for item0 in a]
    # convert times to desired format
    d = []
    for item0 in b:
        e = timedelta(milliseconds=int(item0))
        if re.search(r'[.]', str(e)) is None:
            f = str(e) + '.000'
        else:
            f = str(e)
        d.append(f[0:11])
    return list(enumerate(d))


def inc():
    ts['fg'] = ts['bg']
    ts.delete(0.0, END)
    pb.stop()
    convert()
    
    
    def incr():
        pb['value'] += 5
        if pb['value'] == pb['maximum']:
            ts['fg'] = 'blue'
            return None
        tk.after(50, incr)
        

    return incr()


def convert():
    for tim, cont in zip(time(), content()):
        # iteration correction for last
        if tim[0] == len(time()) - 1:
            var1 = re.sub(r"[0-5][0-9]\Z", '58', tim[1])
            var2 = re.sub(r'[0-5][0-9][^:\d]', '59.', var1)
            ts.insert(INSERT, str(tim[0] + 1) + '\n')
            ts.insert(INSERT, tim[1] + ' --> ' + var2 + '\n')
            ts.insert(INSERT, cont + '\n')
            break
        # writing of srt file
        ts.insert(INSERT, str(tim[0] + 1) + '\n')
        ts.insert(INSERT, tim[1] + ' --> ' + time()[tim[0] + 1][1] + '\n')
        ts.insert(INSERT, cont + '\n\n')


# conversion button
bt0 = Button(frame1, default='normal', text="Convert", command=inc)
bt0.place(relwidth=0.3, relheight=0.8, rely=0.1, relx=0.01)

tk.mainloop()
