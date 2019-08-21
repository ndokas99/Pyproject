import re
import tkinter
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import LoadFileDialog, SaveFileDialog
from tkinter.constants import *
from datetime import timedelta

tk = tkinter.Tk()
tk.title('smi2srt Converter')
tk.wm_minsize(600, 600)
ico = tkinter.PhotoImage(file='convert.ico')
tk.iconphoto(True, ico)


def file_open(*args):
    file = LoadFileDialog(tk, title='Load file')
    link = file.go(r'C:\Users\NDOKKAS', pattern='*.smi')
    if link:
        st.delete(0.0, END)
        ts.delete(0.0, END)
        with open(link, 'r') as f:
            ent = f.read()
            st.insert(INSERT, ent)


def save(*args):
    file = SaveFileDialog(tk, title='Save file')
    link = file.go(r'C:\Users\NDOKKAS', pattern='*.srt')
    if link:
        with open(link, 'w') as f:
            f.write(ts.get(0.0, END))


def about(*args):
    top = tkinter.Toplevel(tk, bg='white')
    top.title('About')
    top.transient(tk)
    lb = tkinter.Label(top, text='Experimental \nnotepad \nKuda Ndox', bg='grey')
    lb.place(relwidth=1, relheight=0.8)
    tkinter.Button(top, text='Close', command=top.destroy).place(rely=0.8, relx=0.5, relheight=0.2, anchor='n')
    return None


def help_(*args):
    top = tkinter.Toplevel(tk, bg='white')
    top.title('Help')
    top.transient(tk)
    lb = tkinter.Label(top, text='This is a \nsubtitle converter \nmade to convert an \nsmi file to srt', bg='grey')
    lb.place(relwidth=1, relheight=0.8)
    tkinter.Button(top, text='Close', command=top.destroy).place(rely=0.8, relx=0.5, relheight=0.2, anchor='n')
    return None


menus = (
    ("File", (
        ("Open   Ctrl+O", file_open),
        ("Save    Ctrl+S", save),
        ("Exit", tk.destroy)
    )
    ),
    ("Help", (
        ("View Help   F1", help_),
        ("About converter", about)
    )
    )
)

menu_bar = tkinter.Menu(tk, bg='grey', fg='white')
for menu in menus:
    m = tkinter.Menu(tk)
    for item in menu[1]:
        m.add_command(label=item[0], command=item[1])
        m.configure(font='Arial 7 italic')
    menu_bar.add_cascade(label=menu[0], menu=m)
menu_bar.configure(font='Arial 7 italic')
tk['menu'] = menu_bar


tk.bind('<Control-Key-o>', file_open)
tk.bind('<Control-Key-O>', file_open, '+')
tk.bind('<Control-Key-s>', save)
tk.bind('<Control-Key-o>', save, '+')
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


frame0 = tkinter.Frame(tk, relief='flat', borderwidth=2, bg='black')
frame0.place(relwidth=1, relheight=0.95, rely=0)

frame1 = tkinter.Frame(tk, relief='flat', borderwidth=2, bg='#aa0000')
frame1.place(relwidth=1, relheight=0.05, rely=0.95)

st = ScrolledText(frame0, bg='white', fg='red')
st.place(relwidth=1, relheight=0.5)

ts = ScrolledText(frame0, bg='white', fg='green')
ts.place(rely=0.5, relwidth=1, relheight=0.5)

'''st = tkinter.scrolledtext.ScrolledText(frame0, bg='white', fg='red')
st.place(relwidth=0.5, relheight=1)

ts = tkinter.scrolledtext.ScrolledText(frame0, bg='white', fg='green')
ts.place(relx=0.5, relwidth=0.5, relheight=1)'''

pb = ttk.Progressbar(frame1, maximum=100, mode='determinate', value=0)
pb.place(relwidth=0.65, relheight=0.9, rely=0.05, relx=0.325)


def inc():
    ts.delete(0.0, END)
    pb.stop()

    def incr():
        pb['value'] += 1
        if pb['value'] == pb['maximum']:
            convert()
            return None
        tk.after(50, incr)

    return incr()


def convert():
    for tim, cont in zip(time(), content()):
        # iteration correction for last
        if tim[0] == len(time()) - 1:
            var1 = re.sub(r'[0-5][0-9]\Z', '58', tim[1])
            var2 = re.sub(r'[0-5][0-9][^:\d]', '59.', var1)
            ts.insert(INSERT, str(tim[0] + 1) + '\n')
            ts.insert(INSERT, tim[1] + ' --> ' + var2 + '\n')
            ts.insert(INSERT, cont + '\n')
            break
        # writing of srt file
        ts.insert(INSERT, str(tim[0] + 1) + '\n')
        ts.insert(INSERT, tim[1] + ' --> ' + time()[tim[0] + 1][1] + '\n')
        ts.insert(INSERT, cont + '\n\n')


bt0 = tkinter.Button(frame1, default='active', text="Convert", font='Arial 5 italic', command=inc)
bt0.place(relwidth=0.3, relheight=1, rely=0)

tk.mainloop()
