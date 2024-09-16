import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Global variables to store files and folder
files = []
folder = ""

def select_files():
    global files
    files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if files:
        messagebox.showinfo("Selected Files", f"{len(files)} files selected.")
    else:
        messagebox.showwarning("No Files", "No files were selected.")

def select_folder():
    global folder
    folder = filedialog.askdirectory()
    if folder:
        messagebox.showinfo("Selected Folder", f"Folder selected: {folder}")
    else:
        messagebox.showwarning("No Folder", "No folder was selected.")

def process_data():
    state = state_entry.get()
    if not state:
        messagebox.showerror("Error", "Please enter a state name.")
        return
    
    combined_data = pd.DataFrame()  # Create an empty DataFrame to store the combined data
    
    for file in files:
        data = pd.read_csv(file)  # Read each CSV file
        data.columns = data.columns.str.strip()  # Clean column names by removing extra spaces
        
        # Get the date from cell A2 (first column, second row) and clean any extra spaces/characters
        date = data.iloc[1, 0].strip()  # Strip any extra spaces or hidden characters
        
        # Check if the first column contains the state name
        if data.iloc[:, 0].str.contains(state, case=False).any():  # Check if any value in the first column matches the state
            filtered_data = data[data.iloc[:, 0].str.contains(state, case=False)]  # Filter rows where the first column matches the state
            
            # Add the "Date" column at the beginning of the filtered data, filled with the clean date
            filtered_data.insert(0, "Date", date)
            
            # Append filtered data to the combined DataFrame
            combined_data = pd.concat([combined_data, filtered_data])
        else:
            messagebox.showwarning("State Not Found", f"State '{state}' not found in {file}.")
    
    if combined_data.empty:
        messagebox.showerror("Error", f"No data found for the state '{state}' in the selected files.")
        return
    
    if not folder:
        messagebox.showerror("Error", "Please select a folder to save the file.")
        return
    
    save_path = os.path.join(folder, f"{state}.csv")  # Save the combined data as a CSV file in the selected folder
    combined_data.to_csv(save_path, index=False)  # Save without row indices
    messagebox.showinfo("Success", f"Data saved to {save_path}")

# Setting up the GUI
root = tk.Tk()
root.title("CSV Processor")

# Label for instructions
instruction_label = tk.Label(root, text="Select CSV files and process data by State/UTs")
instruction_label.pack(pady=10)

# Button to select CSV files
btn_select_files = tk.Button(root, text="Select CSV Files", command=select_files)
btn_select_files.pack(pady=5)

# Entry for entering the state name
state_label = tk.Label(root, text="Enter State/UT Name:")
state_label.pack(pady=5)
state_entry = tk.Entry(root)
state_entry.pack(pady=5)

# Button to select the folder to save the output
btn_select_folder = tk.Button(root, text="Select Folder to Save Output", command=select_folder)
btn_select_folder.pack(pady=5)

# Button to start the process
btn_process_data = tk.Button(root, text="Process Data", command=process_data)
btn_process_data.pack(pady=10)

# Run the GUI loop
root.mainloop()
