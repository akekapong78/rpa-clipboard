import tkinter as tk
from tkinter import messagebox, filedialog
import pyperclip
import json
import re

class ClipboardManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPA Clipboard Manager")
        # self.root.geometry("500x400")  # Set initial window size

        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons with styling and grid layout
        self.add_button = tk.Button(self.frame, text="Add Clipboard", command=self.add_clipboard_entry,
                                    bg='#4CAF50', fg='white', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5)
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.copy_button = tk.Button(self.frame, text="Set Clipboard", command=self.copy_to_clipboard,
                                     bg='#9C27B0', fg='white', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5)
        self.copy_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        self.load_button = tk.Button(self.frame, text="Load from File", command=self.load_entries_from_file,
                                     bg='#FF5722', fg='white', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5)
        self.load_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.save_button = tk.Button(self.frame, text="Save to File", command=self.save_entries_to_file,
                                     bg='#2196F3', fg='white', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5)
        self.save_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self.clear_button = tk.Button(self.frame, text="Clear List", command=self.clear_list,
                                      bg='#FFC107', fg='black', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5)
        self.clear_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        # Listbox to display clipboard entries
        self.listbox = tk.Listbox(self.root, font=('Arial', 12), selectmode=tk.SINGLE)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # List to store clipboard entries
        self.clipboard_entries = []

    def find_text_between(self, text, start, end):
        start_index = text.find(start)
        if start_index != -1:
            end_index = text.find(end, start_index + len(start))
            if end_index != -1:
                return text[start_index + len(start):end_index]

        return None

    def add_clipboard_entry(self):
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            # Extract function names using regex
            functions = self.find_text_between(clipboard_content, "FUNCTION ", " GLOBAL")
            # functions = re.findall(r'FUNCTION\s+(\w+)\s+GLOBAL', clipboard_content)
            if functions:
                entry_label = f"{functions}"
                self.clipboard_entries.append({'label': entry_label, 'content': clipboard_content})
                self.update_listbox()
                pyperclip.copy('')  # Optionally clear the clipboard
                self.update_status("Added clipboard entry.")
            else:
                self.update_status("No functions found in clipboard content.")
        else:
            self.update_status("Warning: Clipboard is empty.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for entry in self.clipboard_entries:
            self.listbox.insert(tk.END, entry['label'])

    def save_entries_to_file(self):
        if self.clipboard_entries:
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
                if file_path:
                    with open(file_path, 'w') as file:
                        json.dump(self.clipboard_entries, file)
                    self.update_status(f"Entries saved to {file_path}")
            except Exception as e:
                self.update_status(f"Error: {str(e)}")
        else:
            self.update_status("Warning: No clipboard entries to save.")

    def load_entries_from_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.clipboard_entries = json.load(file)
                self.update_listbox()
                self.update_status(f"Entries loaded from {file_path}")
            except Exception as e:
                self.update_status(f"Error: {str(e)}")

    def copy_to_clipboard(self):
        try:
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_entry = self.clipboard_entries[selected_index[0]]
                pyperclip.copy(selected_entry['content'])
                self.update_status("Copied to clipboard.")
            else:
                self.update_status("Warning: No item selected.")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def clear_list(self):
        self.listbox.delete(0, tk.END)
        self.clipboard_entries = []
        pyperclip.copy('')
        self.update_status("List and clipboard cleared. Ready to load new file.")

    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardManagerApp(root)
    root.mainloop()