import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import pyperclip
import json
import re
import pyautogui
import pygetwindow as gw
import hashlib
from datetime import datetime
import time
import os

class ClipboardManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPA Clipboard Manager")

        # Track activation status
        self.activated = False
        self.activation_file = "activation_status.json"

        # Get the current USERNAME from the environment
        self.username = os.getenv('USERNAME')

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add an "Home" menu with activation
        self.home_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Home", menu=self.home_menu)
        self.home_menu.add_command(label="Activate", command=self.show_activation_dialog)
        self.home_menu.add_command(label="Exit", command=self.exit_app)

        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=False)
        
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

        self.get_pad_button = tk.Button(self.frame, text="Get from PAD", command=self.get_from_pad,
                                        bg='#607D8B', fg='white', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5, state=tk.DISABLED)
        self.get_pad_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.set_pad_button = tk.Button(self.frame, text="Set to PAD", command=self.set_to_pad,
                                        bg='#795548', fg='white', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5, state=tk.DISABLED)
        self.set_pad_button.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        self.clear_button = tk.Button(self.frame, text="Clear List", command=self.clear_list,
                                      bg='#FFC107', fg='black', font=('Arial', 12), relief=tk.RAISED, padx=10, pady=5)
        self.clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        # Listbox to display clipboard entries
        self.listbox = tk.Listbox(self.root, font=('Arial', 12), selectmode=tk.SINGLE)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # List to store clipboard entries
        self.clipboard_entries = []

        # Check if the app is already activated for the current user
        self.check_activation_status()


    # Check activation status on startup
    def check_activation_status(self):
        if os.path.exists(self.activation_file):
            with open(self.activation_file, 'r') as file:
                activation_data = json.load(file)
                if activation_data.get(self.username, False):
                    self.activated = True
                    self.get_pad_button.config(state=tk.NORMAL)
                    self.set_pad_button.config(state=tk.NORMAL)
                    self.update_status("Activated for user: " + self.username)
                else:
                    self.update_status("Not activated for user: " + self.username)
        else:
            self.update_status("No activation data found. Please activate.")

    # Function to show the activation dialog
    def show_activation_dialog(self):
        activation_key = simpledialog.askstring("Activate", "Enter activation key:")
        if activation_key:
            self.handle_activate(activation_key)

    # Handle activation logic
    def handle_activate(self, entered_key):
        salt = self.generate_salt()
        generated_key = self.encrypt_key(salt)

        if entered_key == generated_key:
            self.activated = True
            self.get_pad_button.config(state=tk.NORMAL)
            self.set_pad_button.config(state=tk.NORMAL)
            self.save_activation_status()
            messagebox.showinfo("Activation", "Activation successful!")
            self.update_status("Activated.")
        else:
            messagebox.showerror("Activation", "Invalid activation key.")
            self.update_status("Activation failed.")

    # Generate a salt based on the current date (UTC midnight)
    def generate_salt(self):
        utc_midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return utc_midnight.strftime('%Y-%m-%d')

    # Encrypt the salt to create an activation key
    def encrypt_key(self, salt):
        return hashlib.sha256(salt.encode()).hexdigest()
        
    # Save the activation status to a local file
    def save_activation_status(self):
        activation_data = {}
        if os.path.exists(self.activation_file):
            with open(self.activation_file, 'r') as file:
                activation_data = json.load(file)

        activation_data[self.username] = True

        with open(self.activation_file, 'w') as file:
            json.dump(activation_data, file)

        self.update_status(f"Activation saved for user: {self.username}")


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
            if functions:
                entry_label = f"{functions}"
                self.clipboard_entries.append({'label': entry_label, 'content': clipboard_content})
                self.update_listbox()
                pyperclip.copy('')  # Optionally clear the clipboard
                self.update_status("Added Power Automate clipboard entry.")
            else:
                entry_label = f"Clipboard {len(self.clipboard_entries) + 1}"
                self.clipboard_entries.append({'label': entry_label, 'content': clipboard_content})
                self.update_listbox()
                pyperclip.copy('')  # Optionally clear the clipboard
                self.update_status("Added some clipboard entry.")
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
                self.update_status(f"Loaded from {file_path}")
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

    def get_from_pad(self):
        # Find and activate the Power Automate window
        windows = gw.getWindowsWithTitle('Power Automate | ')
        if len(windows) > 0:
            power_automate_window = windows[0]
            power_automate_window.activate()
            self.update_status("Power Automate window focused.")

            # Press subflow_button for show all subflow
            try:
                subflow_button = pyautogui.locateOnScreen('assets/subflow_button.png')
                if subflow_button:
                    image_center = pyautogui.center(subflow_button)
                    pyautogui.click(image_center)
                    pyautogui.press(['up', 'down'])
                    self.update_status("Clicked on the image in Power Automate.")

                    # Loop until the image is found for copy subflow
                    try:
                        while True:
                            pyautogui.hotkey('ctrl', 'c')
                            self.add_clipboard_entry()
                            time.sleep(0.5)  # Adjust the delay as needed
                            pyautogui.press('down')
                            
                            # Image found, click on it and exit the loop
                            try:
                                end_button = pyautogui.locateOnScreen('assets/subflow_button_active.png')
                                if end_button:
                                    self.update_status("Copied all subflow.")
                                    break  # Exit the loop when the image is found
                            except:
                                continue

                    except Exception as e:
                        self.update_status(f"Error during Get from PAD: {str(e)}")
                else:
                    self.update_status("Image not found.")
            except Exception as e:
                self.update_status(f"Error during Get from PAD: {str(e)}")

            # Show a popup message saying "Done"
            self.root.focus_force()
            messagebox.showinfo("Status", "Done subflow copying!")

        else:
            self.update_status("Power Automate window not found. Exiting...")
        


    def set_to_pad(self):
        pyperclip.copy('')  # Optionally clear the clipboard
        # Find and activate the Power Automate window
        windows = gw.getWindowsWithTitle('Power Automate | ')
        if len(windows) > 0:
            power_automate_window = windows[0]
            power_automate_window.activate()
            self.update_status("Power Automate window focused.")

            # Press subflow_button for show all subflow
            try:
                subflow_button = pyautogui.locateOnScreen('assets/subflow_button.png')

                if subflow_button:
                    image_center = pyautogui.center(subflow_button)
                    pyautogui.click(image_center)

                    # Loop through clipboard entries and paste them
                    for index, entry in enumerate(self.clipboard_entries):
                        # Copy each list to clipboard
                        expected_content = entry['content']
                        pyperclip.copy(expected_content)
                        
                        # Add a small delay to ensure the clipboard is properly updated
                        time.sleep(1)  # Wait 1 second before checking clipboard for the first item

                        # Poll the clipboard until the content is set or timeout occurs
                        start_time = time.time()
                        max_wait_time = 30  # Set max wait time to 30 seconds
                        clipboard_ready = False

                        # Keep checking if the clipboard matches the expected content
                        while time.time() - start_time < max_wait_time:
                            if pyperclip.paste() == expected_content:
                                clipboard_ready = True
                                break
                            time.sleep(0.3)  # Check every 300 milliseconds

                        # If clipboard is ready, proceed with pasting
                        if clipboard_ready:
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(1.5)  # Allow time for the paste to complete
                            self.update_status(f"Successfully pasted entry {entry['label']}")
                        else:
                            self.update_status(f"Failed to set clipboard for entry {entry['label']}")
                            break  # Exit if clipboard content was not set in time
                    
                    self.update_status("Subflows pasted successfully.")

                else:
                    self.update_status("Image not found.")
            except Exception as e:
                self.update_status(f"Error during Get from PAD: {str(e)}")
            
            # Show a popup message saying "Done"
            self.root.focus_force()
            messagebox.showinfo("Status", "Done subflow pasting!")

        else:
            self.update_status("Power Automate window not found. Exiting...")
        
    def exit_app(self):
        # Optionally, you can prompt the user to confirm exit
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardManagerApp(root)
    root.mainloop()


# Build script
# pyinstaller --onefile --add-data "assets/subflow_button.png;assets" --add-data "assets/subflow_button_active.png;assets" main.py
