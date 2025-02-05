import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt

#base class to handle data operations
class ApplicationManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
    
    def display_all(self):
        """Return all data"""
        return self.data
    
    def view_application(self, identifier):
        """View application details by index or company name"""
        if isinstance(identifier, int) and 0 <= identifier < len(self.data):
            return self.data.iloc[[identifier]]
        elif isinstance(identifier, str):
            return self.data[self.data['Company Name'] == identifier]
        else:
            raise ValueError("Invalid input!")
    
    def filter_applications(self, column, value=None):
        """Filter applications by column and optionally value"""
        if column not in self.data.columns:
            raise ValueError("Invalid column name!")
        if value:  #if value then filter the data and return all columns
            return self.data[self.data[column] == value]
        else:  #if no value then return only 'Company Name' and the requested column
            return self.data[['Company Name', column]]
    
    def update_column(self, identifier, column_name, new_value):
        """Update a column value by index or company name"""
        if isinstance(identifier, int) and 0 <= identifier < len(self.data):
            self.data.at[identifier, column_name] = new_value
        elif isinstance(identifier, str):
            indices = self.data[self.data['Company Name'] == identifier].index
            for idx in indices:
                self.data.at[idx, column_name] = new_value
        else:
            raise ValueError("Invalid input!")
    
    def add_new_row(self, row_data):
        """Add a new row to the data"""
        new_row = pd.DataFrame([row_data], columns=self.data.columns)
        self.data = pd.concat([self.data, new_row], ignore_index=True)
    
    def remove_row(self, identifier):
        """Remove a row by index or company name"""
        if isinstance(identifier, int) and 0 <= identifier < len(self.data):
            self.data = self.data.drop(index=identifier).reset_index(drop=True)
        elif isinstance(identifier, str):
            self.data = self.data[self.data['Company Name'] != identifier].reset_index(drop=True)
        else:
            raise ValueError("Invalid input!")
    
    def save_changes(self):
        """Save changes to CSV"""
        self.data.to_csv(self.file_path, index=False)

#child class to add GUI
class ApplicationManagerApp(ApplicationManager):
    def __init__(self, root, file_path):
        super().__init__(file_path)  #call base class
        self.root = root
        self.root.title("Job Application Tracker")
        self.create_main_menu()

    def create_main_menu(self):
        """Main Menu Frame"""
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Label(self.main_frame, text="Job Application Tracker", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        #main menu buttons
        ttk.Button(self.main_frame, text="Display All Applications", command=self.display_applications_app).grid(row=1, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="View Application", command=self.view_application_app).grid(row=2, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Filter Applications", command=self.filter_applications_app).grid(row=3, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Update Application", command=self.update_application_app).grid(row=4, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Add New Application", command=self.add_new_application_app).grid(row=5, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Remove Application", command=self.remove_application_app).grid(row=6, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Data Visualisation", command=self.data_visualisation_menu).grid(row=7, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Save Changes", command=self.save_changes_app).grid(row=8, column=0, sticky="ew", pady=5)
        ttk.Button(self.main_frame, text="Exit", command=self.root.quit).grid(row=9, column=0, sticky="ew", pady=5)
        
    def data_visualisation_menu(self):
        """Menu for Data Visualisation Options"""
        window = tk.Toplevel(self.root)
        window.title("Data Visualisation")

        ttk.Label(window, text="Choose Visualisation Option:").grid(row=0, column=0, padx=10, pady=10)

        #visualisation buttons
        ttk.Button(window, text="Bar Chart: Status Visualisation", command=self.bar_chart_status_visualisation).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(window, text="Pie Chart: Sector Visualisation", command=self.pie_chart_sector_visualisation).grid(row=2, column=0, padx=10, pady=5)
        ttk.Button(window, text="Close", command=window.destroy).grid(row=3, column=0, padx=10, pady=10)

    def bar_chart_status_visualisation(self):
        """Bar Chart: Status Visualisation"""
        sector_status_counts = self.data.groupby(['Sector', 'Application Status']).size().unstack(fill_value=0)
        
        colors = {"Applied": "blue","Not Open": "orange","Rejected": "red", "Successful": "green"}
        
        sector_status_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=[colors[col] for col in sector_status_counts.columns])
        
        plt.title("Sector-Focused Application Status Visualisation", fontsize=14)
        plt.xlabel("Sector", fontsize=12)
        plt.ylabel("Number of Applications", fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title="Application Status", fontsize=10)
        plt.show()

    def pie_chart_sector_visualisation(self):
        """Pie Chart: Sector Visualisation"""
        sector_counts = self.data['Sector'].value_counts()
        plt.figure(figsize=(10, 10))
        plt.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
        plt.title("Tech Sector Application Distribution", fontsize=14)
        plt.show()

    def display_applications_app(self):
        """Display All Applications"""
        self.show_data_window(self.display_all(), "All Applications")

    def view_application_app(self):
        """View an application with a dropdown to select company names."""
        window = tk.Toplevel(self.root)
        window.title("View Application")
        ttk.Label(window, text="Select Company Name:").grid(row=0, column=0, padx=5, pady=5)

        #drop down list with company names
        company_names = list(self.data['Company Name'].unique())  #aquire unique company names
        company_box = ttk.Combobox(window, values=company_names, state="readonly")
        company_box.grid(row=0, column=1, padx=5, pady=5)
        company_box.focus_set()

        #confirm selection
        def on_confirm():
            identifier = company_box.get()
            print(identifier)
            if identifier:  #check selection is not empty
                try:
                    result = self.view_application(identifier)
                    self.show_data_window(result, f"Application - {identifier}")
                    window.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Please select a company name!")

        #button for user to confirm and trigger action
        ttk.Button(window, text="View", command=on_confirm).grid(row=1, column=0, columnspan=2, pady=10)

    def filter_applications_app(self):
        """Filter Applications with dropdown for column selection."""
        window = tk.Toplevel(self.root)
        window.title("Filter Applications")

        #label for column selection
        ttk.Label(window, text="Select Column to Filter By:").grid(row=0, column=0, padx=5, pady=5)

        #drop down list for columns
        column_names = [col.strip().replace('_', ' ').title() for col in self.data.columns]
        column_box = ttk.Combobox(window, values=column_names, state="readonly")
        column_box.grid(row=0, column=1, padx=5, pady=5)
        column_box.focus_set()
        ttk.Label(window, text="Enter Value (Leave blank for all):").grid(row=1, column=0, padx=5, pady=5)
        value_entry = ttk.Entry(window)
        value_entry.grid(row=1, column=1, padx=5, pady=5)

        #apply filter
        def on_confirm():
            column = column_box.get()
            value = value_entry.get()

            if column:  #check column is selected
                try:
                    result = self.filter_applications(column, value)
                    self.show_data_window(result, f"Filtered by {column}")
                    window.destroy()  #close window after applying
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Please select a column to filter by!")

        ttk.Button(window, text="Apply Filter", command=on_confirm).grid(row=2, column=0, columnspan=2, pady=10)


    def update_application_app(self):
        """Update an application using Combobox for column selection."""
        window = tk.Toplevel(self.root)
        window.title("Update Application")

        #clean and structure column names for better readability
        raw_column_names = list(self.data.columns)
        column_mapping = {col.strip().replace('_', ' ').title(): col for col in raw_column_names}  # Map display name to raw name
        display_column_names = list(column_mapping.keys())

        #label for column selection
        ttk.Label(window, text="Select Column to Update:").grid(row=0, column=0, padx=5, pady=5)

        #dropdows for column selection
        column_box = ttk.Combobox(window, values=display_column_names, state="readonly")
        column_box.grid(row=0, column=1, padx=5, pady=5)
        column_box.focus_set()
        ttk.Label(window, text="Select Company Name:").grid(row=1, column=0, padx=5, pady=5)

        #drop down for company selection
        company_names = list(self.data['Company Name'].unique())  # Assuming 'Company Name' exists in the data
        company_box = ttk.Combobox(window, values=company_names, state="readonly")
        company_box.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(window, text="Enter New Value:").grid(row=2, column=0, padx=5, pady=5)

        new_value_entry = ttk.Entry(window)
        new_value_entry.grid(row=2, column=1, padx=5, pady=5)

        #confirm user update
        def on_confirm():
            display_column = column_box.get()
            column = column_mapping.get(display_column) 
            identifier = company_box.get()
            new_value = new_value_entry.get()

            if not display_column or not identifier:  #error checkiung
                messagebox.showerror("Error", "Please select a column and a company name!")
                return

            try:
                self.update_column(identifier, column, new_value)
                messagebox.showinfo("Success", f"{display_column} updated successfully for {identifier}!")
                window.destroy()  #close window after update
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(window, text="Update", command=on_confirm).grid(row=3, column=0, columnspan=2, pady=10)


    def add_new_application_app(self):
        """Add a new application row"""
        new_row_data = {}
        for column in self.data.columns:
            value = simpledialog.askstring("Input", f"Enter value for '{column}':")
            new_row_data[column] = value
        try:
            self.add_new_row(new_row_data)
            messagebox.showinfo("Success", "New application added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_application_app(self):
        """Remove an application using a dropdown for selection."""
        #new Toplevel window
        window = tk.Toplevel(self.root)
        window.title("Remove Application")

        #label for selecting
        ttk.Label(window, text="Select Application to Remove:").grid(row=0, column=0, padx=5, pady=5)

        #drop down menu for companyh names
        identifiers = list(self.data['Company Name'].unique())
        identifier_box = ttk.Combobox(window, values=identifiers, state="readonly")
        identifier_box.grid(row=0, column=1, padx=5, pady=5)
        identifier_box.focus_set()

        #confirm removal
        def on_confirm():
            identifier = identifier_box.get()
            if not identifier:
                messagebox.showerror("Error", "Please select an application to remove!")
                return

            try:
                result = self.view_application(identifier)
                self.show_data_window(result, "Confirm Deletion")
                confirm = messagebox.askyesno("Confirm", f"Do you want to delete the application for '{identifier}'?")
                if confirm:
                    self.remove_row(identifier)
                    messagebox.showinfo("Success", f"Application for '{identifier}' removed successfully!")
                    window.destroy()  #close window after deletion
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Button to confirm removal
        ttk.Button(window, text="Remove", command=on_confirm).grid(row=1, column=0, columnspan=2, pady=10)


    def save_changes_app(self):
        """Save Changes and Notify User"""
        self.save_changes()
        messagebox.showinfo("Success", "Changes saved to CSV!")

    def show_data_window(self, data, title):
        """Display Data in a New Window"""
        window = tk.Toplevel(self.root)
        window.title(title)

        tree = ttk.Treeview(window)
        tree["columns"] = list(data.columns)
        tree["show"] = "headings"

        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for _, row in data.iterrows():
            tree.insert("", tk.END, values=list(row))

        tree.pack(expand=True, fill="both")

#run main application
if __name__ == "__main__":
    file_path = "data_da.csv"
    root = tk.Tk()
    app = ApplicationManagerApp(root, file_path)
    root.mainloop()
