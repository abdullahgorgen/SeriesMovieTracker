import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import json
import subprocess




data_file = "data.json"

def load_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

class MovieApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MovieApp")
        self.geometry("1000x600")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.data = load_data()

        self.frames = {}
        for Page in (HomePage, AddPage, DetailPage):
            frame = Page(self)
            self.frames[Page] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, text="HomePage", font=("Arial", 24, "bold"))
        self.label.place(relx=0.5, rely=0.05, anchor="center")

        search_frame = ctk.CTkFrame(self)
        search_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search Movie/Show")
        self.search_entry.place(relx=0.02, rely=0.2, relwidth=0.45)

        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search)
        self.search_button.place(relx=0.48, rely=0.2, relwidth=0.1)

        self.filter_movie_button = ctk.CTkButton(search_frame, text="Movie", command=lambda: self.filter("Movie"))
        self.filter_movie_button.place(relx=0.60, rely=0.2, relwidth=0.1)

        self.filter_show_button = ctk.CTkButton(search_frame, text="Series", command=lambda: self.filter("Series"))
        self.filter_show_button.place(relx=0.72, rely=0.2, relwidth=0.1)

        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ctk.CTkOptionMenu(search_frame, variable=self.filter_var, values=["All", "Watched", "To Watch", "Pending", "Favorites"], command=self.filter)
        self.filter_menu.place(relx=0.84, rely=0.2, relwidth=0.15)


        self.listbox = tk.Listbox(self, 
                                  font=("Courier New", 17, "bold"), 
                                  background="#2e2e2e", 
                                  fg="#ffffff",  
                                  bd=0, 
                                  highlightthickness=0) 
        self.listbox.place(relx=0.1, rely=0.22, relwidth=0.8, relheight=0.5)
        self.listbox.bind("<Double-1>", self.open_detail_page)

        button_frame = ctk.CTkFrame(self)
        button_frame.place(relx=0.1, rely=0.75, relwidth=0.8, relheight=0.1)

        self.to_add_button = ctk.CTkButton(button_frame, text="Add Content", command=self.reset_and_go_add, width=120)
        self.to_add_button.place(relx=0.20, rely=0.2)

        self.add_to_favorites_button = ctk.CTkButton(button_frame, text="Add to Favorites", command=self.add_to_favorites, width=120)
        self.add_to_favorites_button.place(relx=0.4, rely=0.2)

        self.remove_to_favorites_button = ctk.CTkButton(button_frame, text="Remove from Favorites", command=self.remove_to_favorites, width=120)
        self.remove_to_favorites_button.place(relx=0.4, rely=0.2)
        self.remove_to_favorites_button.place_forget()

        self.delete_button = ctk.CTkButton(button_frame, text="Delete", command=self.delete_movie, width=120)
        self.delete_button.place(relx=0.6, rely=0.2)

        self.refresh_list()

        self.back_button = ctk.CTkButton(self, text="Log Out", width=50, command=self.backLogin)
        self.back_button.place(relx=0.01, rely=0.03)



    def refresh_list(self, data=None):
        self.listbox.delete(0, tk.END)
        data = data if data is not None else self.master.data
        for item in data:
            name = item['name']
            rating = item.get('rating', 0)  
            status = item.get('status', 'To Watch')  
            notes = item.get('notes', "")
            
            list_item = f"{name} | status: {status} "
            
            if rating or notes:
                list_item += f"| rating: {rating} | notes: {notes}"

            self.listbox.insert(tk.END, list_item)

            self.filter_var.set("All")




    def search(self):
        query = self.search_var.get().strip().lower()
        filtered_data = []
        
        for item in self.master.data:
            if query in item['name'].lower() or query in item['type'].lower():
                filtered_data.append(item)
        

        self.refresh_list(filtered_data)


    def filter(self, choice):
        self.listbox.delete(0, tk.END)
        for item in self.master.data:
            name = item['name']
            rating = item.get('rating', 0)
            status = item.get('status', 'To Watch')
            notes = item.get('notes', "")
            
            rating_display = f"| rating: {rating}" if rating else ""
            notes_display = f"notes: {notes}" if notes else ""
            
            if choice == "All" or (
                choice == "Movie" and item['type'].lower() == "movie"
            ) or (
                choice == "Series" and item['type'].lower() == "series"
            ) or (
                choice == "Watched" and item['status'].lower() == "watched"
            ) or (
                choice == "To Watch" and item['status'].lower() == "to watch"
            ) or (
                choice == "Pending" and item['status'].lower() == "pending"
            ) or (
                choice == "Favorites" and item.get('favorite', False)
            ):
                self.listbox.insert(tk.END, f"{name} | status: {status} {rating_display} {notes_display}")





        if choice == "Favorites":
            self.add_to_favorites_button.place_forget()
            self.remove_to_favorites_button.place(relx=0.4, rely=0.2)
            
        else:
            self.remove_to_favorites_button.place_forget()
            self.add_to_favorites_button.place(relx=0.4, rely=0.2)

    def open_detail_page(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.master.frames[DetailPage].load_item(self.master.data[index])
            self.master.show_frame(DetailPage)


    def reset_and_go_add(self):
        self.search_var.set("")
        self.master.frames[AddPage].reset_fields()
        self.master.show_frame(AddPage)

    def add_to_favorites(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.master.data[index]

            if item.get('favorite', False):  
                messagebox.showwarning("Warning", "This content is already in favorites.")
            else:
                self.master.data[index]['favorite'] = True  # Favori olarak işaretle
                save_data(self.master.data)  # Güncellenmiş veriyi kaydet
                self.refresh_list()
                messagebox.showinfo("Success", "Content successfully added to favorites.")
        else:
            messagebox.showerror("Error", "Please make a selection.")


    def remove_to_favorites(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.master.data[index]['favorite'] = False
            save_data(self.master.data)
            self.refresh_list()
            messagebox.showinfo("Success", "Content successfully removed from favorites.")
        else:
            messagebox.showerror("Error", "Please make a selection.")





    def delete_movie(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected movie?")
            if confirmation:
                self.master.data.pop(index)
                save_data(self.master.data)
                self.refresh_list()
        else:
            messagebox.showerror("Error", "Please make a selection.")



    def backLogin(self):
        self.master.destroy()
        subprocess.run(["python", "entryPage.py"]) 

class DetailPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, text="Detail Page", font=("Helvetica Neue", 24, "bold"))
        self.label.place(relx=0.5, rely=0.05, anchor="center")

        self.rating_var = tk.IntVar()
        ctk.CTkLabel(self, text="Rating:", font=("Helvetica Neue", 14)).place(relx=0.05, rely=0.2)
        self.rating_slider = ctk.CTkSlider(self, from_=1, to=10, variable=self.rating_var, command=self.update_rating_label)
        self.rating_slider.place(relx=0.2, rely=0.2, relwidth=0.6)
        self.rating_label = ctk.CTkLabel(self, text="0", font=("Helvetica Neue", 14))
        self.rating_label.place(relx=0.9, rely=0.2, anchor="e")

        self.notes_var = tk.StringVar()
        ctk.CTkLabel(self, text="Notes:", font=("Helvetica Neue", 14)).place(relx=0.05, rely=0.35)
        self.notes_entry = ctk.CTkEntry(self, textvariable=self.notes_var)
        self.notes_entry.place(relx=0.2, rely=0.35, relwidth=0.75)

        self.status_var = tk.StringVar(value="to watch")
        ctk.CTkLabel(self, text="Status:", font=("Helvetica Neue", 14)).place(relx=0.05, rely=0.5)
        self.status_menu = ctk.CTkOptionMenu(self, variable=self.status_var, values=["watched", "to watch", "pending"])
        self.status_menu.place(relx=0.2, rely=0.5, relwidth=0.75)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_changes)
        self.save_button.place(relx=0.35, rely=0.75, relwidth=0.3)

        self.back_button = ctk.CTkButton(self, text="Home", command=lambda: parent.show_frame(HomePage))
        self.back_button.place(relx=0.35, rely=0.85, relwidth=0.3)


    def update_rating_label(self, value):
        self.rating_label.configure(text=f"{int(float(value))}")

    def load_item(self, item):
        self.item = item
        self.rating_var.set(item.get("rating", 0))
        self.notes_var.set(item.get("notes", ""))
        self.status_var.set(item.get("status", "to watch"))

    def save_changes(self):
        self.item["rating"] = self.rating_var.get()
        self.item["notes"] = self.notes_var.get()
        self.item["status"] = self.status_var.get()
        save_data(self.master.data)
        self.master.frames[HomePage].refresh_list()
        self.master.show_frame(HomePage)





class AddPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, text="Add Content", font=("Helvetica Neue", 24, "bold"))
        self.label.place(relx=0.5, rely=0.05, anchor="center")

        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar(value="movie")
        self.status_var = tk.StringVar(value="to watch")

        form_frame = ctk.CTkFrame(self)
        form_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.5)

        ctk.CTkLabel(form_frame, text="Name:", font=("Helvetica Neue", 14)).place(relx=0.02, rely=0.1)
        ctk.CTkEntry(form_frame, textvariable=self.name_var).place(relx=0.2, rely=0.1, relwidth=0.75)

        ctk.CTkLabel(form_frame, text="Type:", font=("Helvetica Neue", 14)).place(relx=0.02, rely=0.3)
        ctk.CTkOptionMenu(form_frame, variable=self.type_var, values=["Movie", "Series"]).place(relx=0.2, rely=0.3, relwidth=0.75)

        ctk.CTkLabel(form_frame, text="Status:", font=("Helvetica Neue", 14)).place(relx=0.02, rely=0.5)
        ctk.CTkOptionMenu(form_frame, variable=self.status_var, values=["watched", "to watch", "pending"]).place(relx=0.2, rely=0.5, relwidth=0.75)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_item)
        self.save_button.place(relx=0.4, rely=0.7, relwidth=0.2)

        self.back_button = ctk.CTkButton(self, text="Home", command=lambda: parent.show_frame(HomePage))
        self.back_button.place(relx=0.4, rely=0.8, relwidth=0.2)


    def save_item(self):
        new_item = {
            "name": self.name_var.get(),
            "type": self.type_var.get(),
            "status": self.status_var.get(),
            "rating": 0,
            "notes": "",
            "favorite": False
        }

        if not new_item["name"]:
            messagebox.showerror("Error", "Name field cannot be left empty!")
            return

        self.master.data.append(new_item)
        save_data(self.master.data)
        self.master.frames[HomePage].refresh_list()
        self.master.show_frame(HomePage)
        self.reset_fields()

    def reset_fields(self):
        self.name_var.set("")
        self.type_var.set("movie")
        self.status_var.set("to watch")



if __name__ == "__main__":
    app = MovieApp()
    app.mainloop()
