from tkinter import *
from tkinter import ttk, messagebox
import csv
from db import Database

db = Database("clinic.db")

# ===== ألوان وخطوط =====
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#16a085"
ACCENT_COLOR = "#f39c12"
DANGER_COLOR = "#e74c3c"
TEXT_COLOR = "white"
BG_COLOR = "#ecf0f1"
HIGHLIGHT_COLOR = "#dfe6e9"

font_title = ("Segoe UI", 18, "bold")
font_label = ("Segoe UI", 12)
font_button = ("Segoe UI", 11, "bold")

# ===== النافذة =====
m = Tk()
m.geometry("1280x700")
m.title("🏥 نظام إدارة العيادة")
m.config(bg=BG_COLOR)
m.iconbitmap("R.ico")

# ===== المتغيرات =====
patient_name = StringVar()
patient_age = StringVar()
patient_phone = StringVar()
patient_diagnosis = StringVar()
patient_cost = StringVar()
search_var = StringVar()
filter_var = StringVar()

# ===== العنوان =====
title_frame = Frame(m, bg=PRIMARY_COLOR, height=60)
title_frame.pack(fill="x")
Label(title_frame, text="🏥 نظام إدارة العيادة", font=font_title, bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack()

# ===== اليسار =====
left_frame = Frame(m, bg=PRIMARY_COLOR, width=350)
left_frame.pack(side=LEFT, fill=Y)
Label(left_frame, text='👤 بيانات المريض', font=font_title, bg=PRIMARY_COLOR, fg=TEXT_COLOR).place(x=85, y=-10)

def create_labeled_entry(parent, text, var, y):
    Label(parent, text=text, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=font_label).place(x=10, y=y)
    Entry(parent, textvariable=var, width=23, font=("Segoe UI", 11)).place(x=150, y=y+2)

create_labeled_entry(left_frame, "اسم المريض", patient_name, 50)
create_labeled_entry(left_frame, "العمر", patient_age, 100)
create_labeled_entry(left_frame, "رقم الهاتف", patient_phone, 150)
create_labeled_entry(left_frame, "التشخيص", patient_diagnosis, 200)
create_labeled_entry(left_frame, "تكلفة العلاج", patient_cost, 250)

# ===== تصدير CSV =====
def export_csv():
    rows = db.fetch()
    with open("patients_data.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "اسم المريض", "العمر", "رقم الهاتف", "التشخيص", "التكلفة"])
        writer.writerows(rows)
    messagebox.showinfo("تم", "📤 تم تصدير البيانات")

# ===== دوال =====
def getdata():
    global row
    selected = trv.focus()
    data = trv.item(selected)
    row = data["values"]
    if row:
        patient_name.set(row[1]); patient_age.set(row[2]); patient_phone.set(row[3])
        patient_diagnosis.set(row[4]); patient_cost.set(row[5])

def displayall(filter_col=None, filter_val=None):
    trv.delete(*trv.get_children())
    for r in db.fetch():
        if filter_col and filter_val:
            col_idx = {"اسم المريض":1, "العمر":2, "رقم الهاتف":3, "التشخيص":4, "التكلفة":5}[filter_col]
            if filter_val.lower() not in str(r[col_idx]).lower():
                continue
        trv.insert("", END, values=r)

def clear():
    patient_name.set(""); patient_age.set(""); patient_phone.set("")
    patient_diagnosis.set(""); patient_cost.set("")

def add_patient():
    if not (patient_name.get() and patient_age.get() and patient_phone.get() and patient_diagnosis.get() and patient_cost.get()):
        messagebox.showerror("خطأ", "🛑 أدخل جميع البيانات")
        return
    db.insert(patient_name.get(), patient_age.get(), patient_phone.get(), patient_diagnosis.get(), patient_cost.get())
    displayall(); clear()
    messagebox.showinfo("تم", "✅ تمت إضافة المريض")
    m.bell()

def update_patient():
    global row
    if row:
        db.update(row[0], patient_name.get(), patient_age.get(), patient_phone.get(), patient_diagnosis.get(), patient_cost.get())
        displayall(); clear()
        messagebox.showinfo("تم", "✏️ تم التعديل")
    else:
        messagebox.showwarning("تنبيه", "اختر سجلًا أولاً")

def delete_patient():
    global row
    if row:
        if messagebox.askyesno("تأكيد", "⚠️ حذف هذا السجل؟"):
            db.remove(row[0])
            displayall(); clear()
            messagebox.showinfo("تم", "🗑️ تم الحذف")
    else:
        messagebox.showwarning("تنبيه", "اختر سجلًا أولاً")

def search_patients(*args):
    displayall(filter_col=filter_var.get(), filter_val=search_var.get())

# ===== Hover Effect =====
def on_enter(e): e.widget.config(bg="#1abc9c")
def on_leave(e): e.widget.config(bg=e.widget.default_bg)

def styled_button(parent, text, bg, cmd, r, c):
    btn = Button(parent, text=text, width=12, font=font_button, bg=bg, fg=TEXT_COLOR, command=cmd, relief=FLAT, cursor="hand2")
    btn.grid(row=r, column=c, padx=10, pady=10)
    btn.default_bg = bg
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ===== Buttons =====
btn_frame = Frame(left_frame, bg=PRIMARY_COLOR)
btn_frame.place(x=20, y=370, width=300, height=200)

styled_button(btn_frame, "➕ إضافة", SECONDARY_COLOR, add_patient, 0, 0)
styled_button(btn_frame, "✏️ تعديل", "#2980b9", update_patient, 0, 1)
styled_button(btn_frame, "🗑️ حذف", ACCENT_COLOR, delete_patient, 1, 0)
styled_button(btn_frame, "🧹 مسح", DANGER_COLOR, clear, 1, 1)
styled_button(btn_frame, "📤 تصدير CSV", "#9b59b6", export_csv, 2, 0)

Label(left_frame, text="🔍 بحث:", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=font_label).place(x=10, y=580)
Entry(left_frame, textvariable=search_var, width=18, font=("Segoe UI", 11)).place(x=70, y=582)
filter_var.set("اسم المريض")
OptionMenu(left_frame, filter_var, "اسم المريض", "العمر", "رقم الهاتف", "التشخيص", "التكلفة").place(x=230, y=578)
search_var.trace_add("write", search_patients)

# ===== جدول البيانات =====
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=PRIMARY_COLOR, foreground="white")

right_frame = Frame(m, bg=BG_COLOR)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

cols = ("id", "اسم المريض", "العمر", "رقم الهاتف", "التشخيص", "التكلفة")
trv = ttk.Treeview(right_frame, columns=cols, show="headings", height=25)
for col in cols:
    trv.heading(col, text=col)
    trv.column(col, width=150, anchor=CENTER)

scroll_y = Scrollbar(right_frame, orient=VERTICAL, command=trv.yview)
trv.configure(yscroll=scroll_y.set)
scroll_y.pack(side=RIGHT, fill=Y)
trv.bind("<ButtonRelease-1>", lambda e: getdata())
trv.pack(fill=BOTH, expand=True)

displayall()
m.mainloop()
