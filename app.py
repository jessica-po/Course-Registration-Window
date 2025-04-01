# %%
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import *
import db
import tables
from typing import List
import os 

FONT = "Arial"

# allow for connection to the database based on users login credentials
class Login(object):
    def __init__(self):

        # window visuals
        window = Tk()
        window.geometry(center_window(root=window, width=300,height=200))
        window.title("Login")

        Label(window, text="user id", font=(FONT, 12)).place(x=20, y=40)
        self.user_id = Entry(window)
        self.user_id.place(x=100, y=40, width=150)

        Label(window, text="password", font=(FONT, 12)).place(x=20, y=90)
        self.user_pwd = Entry(window, show="*")
        self.user_pwd.place(x=100, y=90, width=150)

        Button(window, text="Login", width=25, font=(FONT,12), command=self.auth).place(x=30, y=140)
        
        self.login_window= window
        
        self.login_window.mainloop()
        
    # authentication
    def auth(self):
        os.environ["ora_uid"] = self.user_id.get()
        os.environ["ora_pwd"] = self.user_pwd.get()
        self.login_window.grab_release()
        self.login_window.destroy()        

# update date if update is true, and add data if update is false
class addupdateRecordForm(object):
    def __init__(self, parent, table_name: str, update_record: bool, table_frame):
        self.data = None
        self.entries = []
        self.table_name = table_name
        self.table_frame = table_frame 
        self.fields = []
        self.update_record = update_record

        table_exists = False
        for w in table_frame.winfo_children():
            if isinstance(w, Treeview): 
                table_exists=True
        
        columns = []
        if table_exists:
            tb = tables.get_table(table_name)  
            columns = tb.columns 

        width = 500
        height = 50 * int(len(columns)/2) + 100

        self.root=Toplevel(parent)

        self.root.geometry(center_window(root=parent, width=width,height=height))
        if update_record:
            edit_data = self.edit_data()
            if not edit_data:
               columns=[]

        if columns: # check if table exists
            self.fields = columns

            y_pos = 10
            cc = 0
            for col in columns:
                cc +=1
                x_pos = 250 if cc % 2 == 0 else 20
            
                required=""
                if col.primary_key:
                    required="*"
                
                Label(self.root, text=f"{required} {col.name} ({col.type.lower()})").place(x=x_pos, y=y_pos)
                y_pos +=20
                
                self.entries.append(Entry(self.root))
                ee= self.entries[len(self.entries)-1]

                if update_record:
                    ee.insert(0, edit_data[cc-1])
                    if col.primary_key:
                        ee.configure(state="disabled", disabledbackground="light gray")

                ee.place(x=x_pos, y=y_pos, width=200)

                y_pos +=30 if cc % 2 == 0 else -20

            if update_record:
                self.update_btn = Button(self.root, text="Update", width=15, command=self.update).place(x=50, y=(height-40))
            else:
                self.save_btn = Button(self.root, text="Save", width=15, command=self.save).place(x=50, y=(height-40))
            
            self.cancel_btn = Button(self.root, text="Cancel", width=15, command=self.cancel).place(x=250, y=(height-40))
        else:
            Label(self.root, text=f"Table/record does not exist", font=(FONT, 14)).place(x=125, y=35)

        self.root.wait_visibility()   
        self.root.grab_set()          
        self.root.transient(parent)   
        
        self.parent = parent

    # saving data
    def save(self):
        self.data = [ e.get() for e in self.entries]
        insert_script = tables.insert_script(self.table_name, self.fields, self.data)

        ok, error = db.db_ddl(insert_script)
        if not ok:
            messagebox.showerror("save", error)
        else:
            self.update_grid(self.data)    
            self.root.grab_release()
            self.root.destroy()

    # updating data
    def update(self):
        self.data = [ e.get() for e in self.entries]
        update_script = tables.update_script(self.table_name, self.fields, self.data)

        ok, error = db.db_ddl(update_script)
        if not ok:
            messagebox.showerror("update", error)
        else:
            self.update_grid(self.data)    
            self.root.grab_release()
            self.root.destroy()


    # display selected data into the grid view
    def update_grid(self, data):
        for w in self.table_frame.winfo_children():
            if isinstance(w, Treeview):
                if not self.update_record:
                   w.insert('', 'end', values = data)
                   rows = w.get_children()
                   w.focus(rows[-1])                   
                   w.selection_set(rows[-1])
                else:
                    self.edit_data(True)

    # update table instance with the newly updated data
    def edit_data(self, update_grid=False):
        table_tree: Treeview = None
        for w in self.table_frame.winfo_children():
            if isinstance(w, Treeview):
                table_tree = w

        if table_tree:
            curr_item = table_tree.focus()
            
            if curr_item:
                record = table_tree.item(curr_item)
                if (record["values"]):
                    if update_grid:
                        table_tree.item(curr_item, values=self.data)
                    else:
                        return record['values']
        
        return None
    
    # resume back to home screen
    def cancel(self):
        self.data = {}
        self.root.grab_release()      
        self.root.destroy()

# diaplay table records to grid view
def table_view_grid(frame: Frame, columns):

    # clear frame
    for w in frame.winfo_children():
        w.grab_release()
        w.destroy()
    
    tree: Treeview = None

    if columns:
        Label(frame, text="Grid view", font=(FONT, 12, "bold")).pack()   
        tree = Treeview(frame, name="table_record", height=14)

        tree.column("#0", width=0, stretch=False)
        tree['columns'] = columns
        col_width = 840//len(columns)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=10, width=col_width, stretch=NO)

        scrollbar = Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")
        
        tree.pack()

    # error message
    else:
        msg1 = "Table does not exist"
        msg2 = "click [create table] button to add table in the database"
        
        Label(frame, text=msg1, font=(FONT, 14, "bold")).place(x=290, y=80)   
        Label(frame, text=msg2, font=(FONT, 12)).place(x=200, y=110)   

    frame.place(x=5, y=200) # 175
    
    return tree

# drop down menu box
def create_combo_box(window, values, var, x_pos, y_pos):
    cb = Combobox(window, textvariable=var, state="readonly")
    cb['values'] = values
    cb.current(0)
    cb.place(x=x_pos, y=y_pos)

    return cb

# get the data and displays it onto the grid
def cb_table_selected(*arg):
    if (var_table.get()):
        populate_table_grid(table_frame, f"select * from {var_table.get()}")

# grabs the data from database, columns, and rows
def populate_table_grid(frame, query):
    columns, data, error = db.db_sql(query)
    if columns:
        tree = table_view_grid(frame, columns)
    
        for row in data:
            row=tree.insert('', 'end', values=row)
        
        rows = tree.get_children()
        if rows:
            tree.focus(rows[0])
            tree.selection_set(rows[0])

    else:
        if error:
            messagebox.showerror("view", error)
        else:
            table_view_grid(frame, [])


# gets a list of all tables in the database and 
def populate_combo_box(window, var, x_pos, y_pos):
    data = tables.list_tables()
    cb = create_combo_box(window, data, var, x_pos, y_pos)
    
    return cb


def delete_record(frame: Frame):
    table_tree: Treeview = None

    for w in frame.winfo_children():
        if isinstance(w, Treeview):
            table_tree = w
    
    if table_tree:
        curr_item = table_tree.focus()
        if curr_item:
            table_name = var_table.get()
            pk_cols = [ {"idx":idx, "name":col.name} for idx, col in enumerate(tables.get_table(table_name).columns) if col.primary_key]
            field_name = pk_cols[0]["name"]
            field_idx = pk_cols[0]["idx"]

            record = table_tree.item(curr_item)
            if (record["values"]):
                r = record['values']
                script = f"delete from {table_name} where {field_name} = '{r[field_idx]}'"
                db.db_ddl(script=script)
                table_tree.delete(curr_item)
        else:
            print("select the table record!!!")
            messagebox.showinfo("Delete", "Please select a record.")


def delete_table(frame: Frame):
    
    table_name = var_table.get()

    script = f"drop table {table_name}"
    ok, error = db.db_ddl(script=script)
    if not ok:
        messagebox.showerror("delete", error)
    else:
        # table_view_grid(window, None)
        for w in frame.winfo_children():
            w.destroy()
    print("drop the table", table_name)

  
def create_table(table_name: str):
    tb = tables.get_table(table_name)    
    script = tables.create_table(tb)
    ok, error = db.db_ddl(script=script)
    if not ok:
        messagebox.showerror("create table", error)
    else:
        cb_table_selected()


def addupdate_popup(w, table_name, update_record, table_frame):
    d = addupdateRecordForm(w, table_name, update_record, table_frame)
    w.wait_window(d.root) 


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    return f"{width}x{height}+{x}+{y}"

def run_query(frame):
    input = query.get(1.0, "end-1c")
    populate_table_grid(frame, input)


#################### Main ##############

login = Login()

window = Tk()
window.geometry(center_window(window,850,600))
window.title("Data Form")

table_frame = Frame(window, width=850, height=200, bd=0)

lb_title = Label(window, text="Data Tool", anchor=CENTER, width="500", bg="lightblue", font=(FONT, 20, "bold"), fg="grey")
lb_title.pack()

var_table = StringVar()
lb_table = Label(window, text="Table list", font=(FONT, 12)).place(x=5, y=50)
cb_tbl_list = populate_combo_box(window, var_table, 80, 50)
var_table.trace('w', cb_table_selected)

Button(window, text="Add data", width=20, command=lambda: addupdate_popup(window, var_table.get(), False, table_frame) ).place(x=50, y=550)
Button(window, text="Update record", width=20, command=lambda: addupdate_popup(window, var_table.get(), True, table_frame) ).place(x=320, y=550)
Button(window, text="Delete record", width=20, command=lambda: delete_record(frame=table_frame)).place(x=600, y=550)

Button(window, text="Create table", width=20, command=lambda: create_table(var_table.get())).place(x=630, y=50)
Button(window, text="Drop table", width=20, command=lambda: delete_table(frame=table_frame )).place(x=630, y= 90)
Button(window, text="Query", width=20, command=lambda: run_query(frame=table_frame)).place(x=630, y=130)

Label(window, text="Query", font=(FONT, 12)).place(x=5, y=90)
query = Text(window, width=150, height=6)
query.place(x=80, y=90, width=500)

cb_table_selected()

window.mainloop()

# %%
