import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import threading
import json
import os
import hashlib
import requests
import time # For delays during shutdown

class MinecraftServerUpdaterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Minecraft Server Updater & Runner")
        master.geometry("750x650") # Increased window size for new elements
        master.resizable(True, True) # Allow resizing again for better usability

        self.java_process = None # To hold the reference to the running Java process
        self.server_output_thread = None # To hold the reference to the thread reading server output

        # --- GUI Elements ---

        # Frame for Status and Progress (Packed to TOP)
        status_frame = tk.LabelFrame(master, text="Status", padx=10, pady=10)
        status_frame.pack(padx=10, pady=10, fill=tk.X, side=tk.TOP)

        self.current_status_label = tk.Label(status_frame, text="Initializing...", font=("Helvetica", 12, "bold"))
        self.current_status_label.pack(anchor=tk.W, pady=5)

        # Progress elements (initially not packed, will be packed/unpacked by methods)
        # Corrected: set maximum=100 here for percentage display
        self.progress_bar = ttk.Progressbar(status_frame, orient="horizontal", length=200, mode="determinate", maximum=100)
        self.progress_bar_label = tk.Label(status_frame, text="0%")


        # Frame for Version Information (Packed to TOP, below status)
        version_frame = tk.LabelFrame(master, text="Server Information", padx=10, pady=10)
        version_frame.pack(padx=10, pady=10, fill=tk.X, side=tk.TOP)

        self.latest_version_label = tk.Label(version_frame, text="Latest Version: N/A", font=("Helvetica", 10))
        self.latest_version_label.pack(anchor=tk.W)

        self.local_version_label = tk.Label(version_frame, text="Local Version: N/A", font=("Helvetica", 10))
        self.local_version_label.pack(anchor=tk.W)
        
        # --- Elements packed from the BOTTOM up ---

        # Buttons Frame (Packed to BOTTOM)
        button_frame = tk.Frame(master)
        button_frame.pack(pady=5, side=tk.BOTTOM)

        self.quit_button = tk.Button(button_frame, text="Quit", command=self.on_quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        # Command Input Area (Packed to BOTTOM, above buttons)
        command_frame = tk.Frame(master)
        command_frame.pack(padx=10, pady=5, fill=tk.X, side=tk.BOTTOM)

        self.command_entry = tk.Entry(command_frame, font=("Consolas", 10))
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.command_entry.bind("<Return>", self.send_command_event) # Bind Enter key

        self.send_button = tk.Button(command_frame, text="Send Command", command=self.send_command)
        self.send_button.pack(side=tk.RIGHT)
        self.command_entry.config(state='disabled') # Disable until server runs
        self.send_button.config(state='disabled') # Disable until server runs

        # Log Area (This will fill the remaining space in the middle, packed to TOP last)
        log_frame = tk.LabelFrame(master, text="Server Log & Process Details", padx=10, pady=10)
        log_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.TOP) # Expands to fill middle space

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled', font=("Consolas", 9))
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # Automatically start the process (MOVED TO END OF __init__)
        self.master.after(100, self.start_update_process) # Give GUI time to render before starting

    def log_message(self, message):
        """Appends a message to the log area."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.master.update_idletasks()

    def update_status(self, message):
        """Updates the main status label."""
        self.current_status_label.config(text=message)
        self.master.update_idletasks()

    def update_progress(self, value, total):
        """Updates the progress bar and label."""
        if total > 0:
            percentage = (value / total) * 100
            self.progress_bar.config(value=percentage) # Now correctly sets a percentage value
            self.progress_bar_label.config(text=f"{percentage:.1f}%")
        else: # Handle cases where total_length is 0 or unknown (e.g., if content-length header is missing)
            # For unknown total length, we can show a continuous "indeterminate" progress bar if needed,
            # but for now, we'll reset it.
            self.progress_bar.config(value=0) # Reset bar
            self.progress_bar_label.config(text="N/A")
        self.master.update_idletasks()

    def show_progress_bar(self):
        """Shows the progress bar and label."""
        # Pack within the status_frame
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.progress_bar_label.pack(anchor=tk.E)
        self.master.update_idletasks()

    def hide_progress_bar(self):
        """Hides the progress bar and label."""
        self.progress_bar.pack_forget()
        self.progress_bar_label.pack_forget()
        self.master.update_idletasks()

    def update_version_info(self, latest_v, local_v):
        """Updates the version information labels."""
        self.latest_version_label.config(text=f"Latest Version: {latest_v}")
        self.local_version_label.config(text=f"Local Version: {local_v}")
        self.master.update_idletasks()

    def send_command_event(self, event=None): # Added event parameter for binding
        self.send_command()

    def send_command(self):
        command = self.command_entry.get().strip()
        if not command:
            self.log_message("Attempted to send empty command.")
            return
        
        if self.java_process and self.java_process.poll() is None: # If server is running
            if self.java_process.stdin and not self.java_process.stdin.closed:
                try:
                    self.log_message(f"COMMAND SENT: > {command}") # Echo command to log
                    self.java_process.stdin.write(command + "\n")
                    self.java_process.stdin.flush()
                    self.command_entry.delete(0, tk.END) # Clear input field
                except Exception as e:
                    self.log_message(f"Error sending command to server stdin: {e}")
            else:
                self.log_message("Server stdin pipe is not open or available.")
                messagebox.showwarning("Server Input Error", "Cannot send command: Server input pipe is not available.")
        else:
            self.log_message("Cannot send command: Minecraft server is not running.")
            messagebox.showwarning("Server Not Running", "Cannot send command: Minecraft server is not active.")

    def start_update_process(self):
        """Starts the update and server running process in a separate thread."""
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END) # Clear previous log
        self.log_area.config(state='disabled')
        self.update_status("Starting update process...")
        self.progress_bar.config(value=0) # Reset bar
        self.progress_bar_label.config(text="0%")
        self.hide_progress_bar() # Ensure hidden at start
        self.update_version_info("N/A", "N/A")
        
        # Start the heavy lifting in a new thread
        threading.Thread(target=self._run_update_logic, daemon=True).start()

    def _read_server_output(self):
        """Reads output from the Java process in a separate thread."""
        if self.java_process:
            for line in iter(self.java_process.stdout.readline, ''):
                # Use master.after to update GUI from a non-GUI thread
                self.master.after(0, self.log_message, f"SERVER: {line.strip()}")
            
            self.master.after(0, self.log_message, "Server output stream closed.")
            
            # Disable command input fields when server output stream closes
            self.master.after(0, lambda: self.command_entry.config(state='disabled'))
            self.master.after(0, lambda: self.send_button.config(state='disabled'))
            
            # Wait for the process to truly finish and then update status
            self.java_process.wait() # This waits for the process to terminate
            self.master.after(0, self.update_status, "Server process terminated.")
        
    def _run_update_logic(self):
        """
        Contains the core logic of the CMD script, translated to Python,
        running in a separate thread.
        """
        local_server_jar_path = "server.jar"
        eula_path = "eula.txt"
        current_local_version = "Unknown"

        try:
            self.hide_progress_bar() # Ensure hidden before update starts
            # Determine local server.jar version for display
            if os.path.exists(local_server_jar_path):
                current_local_version = "Present (SHA1 check next)"
            else:
                current_local_version = "Not found"
            self.update_version_info("N/A", current_local_version)

            self.update_status("Checking for Minecraft server updates...")
            self.log_message("Checking for Minecraft server updates...")

            # --- 1. Download version manifest ---
            self.show_progress_bar() # Show bar for download
            self.update_status("Downloading version manifest...")
            self.log_message("Downloading version manifest...")
            MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
            manifest_data = self._download_json(MANIFEST_URL, "manifest.json")
            if not manifest_data:
                self.update_status("Failed to download manifest. Aborting.")
                self.log_message("Failed to download or parse manifest. Aborting.")
                self.hide_progress_bar() # Hide on failure
                return

            # --- 2. Get latest version ID ---
            latest_version_id = manifest_data['latest']['release']
            self.update_status(f"Latest version found: {latest_version_id}")
            self.log_message(f"Latest version: {latest_version_id}")
            self.update_version_info(latest_version_id, current_local_version) # Update with latest version

            # --- 3. Get version JSON URL ---
            version_url = None
            for version_entry in manifest_data['versions']:
                if version_entry['id'] == latest_version_id:
                    version_url = version_entry['url']
                    break
            if not version_url:
                self.update_status("Could not find URL for latest version. Aborting.")
                self.log_message("Could not find URL for latest version. Aborting.")
                self.hide_progress_bar() # Hide on failure
                return
            
            # --- 4. Download version metadata ---
            self.update_status(f"Downloading metadata for {latest_version_id}...")
            self.log_message(f"Downloading version metadata from {version_url}...")
            version_metadata = self._download_json(version_url, "version.json")
            if not version_metadata:
                self.update_status("Failed to download metadata. Aborting.")
                self.log_message("Failed to download or parse version metadata. Aborting.")
                self.hide_progress_bar() # Hide on failure
                return

            # --- 5. Get download URL and SHA1 ---
            server_downloads = version_metadata['downloads']['server']
            server_jar_url = server_downloads['url']
            mojang_sha1 = server_downloads['sha1'].upper()
            self.log_message(f"Mojang SHA1: {mojang_sha1}")

            # --- 6. Check local SHA1 ---
            need_update = True
            local_sha1 = "N/A"
            if os.path.exists(local_server_jar_path):
                self.update_status("Calculating local server.jar SHA1...")
                self.log_message("Calculating local server.jar SHA1...")
                try:
                    local_sha1 = self._calculate_file_sha1(local_server_jar_path).upper()
                    self.log_message(f"Local SHA1 : {local_sha1}")
                    self.update_version_info(latest_version_id, f"Local SHA1: {local_sha1[:8]}...") # Show truncated SHA1 for brevity

                    if local_sha1 == mojang_sha1:
                        self.update_status("server.jar is already up to date.")
                        self.log_message("server.jar is already up to date.")
                        need_update = False
                    else:
                        self.update_status("Local server.jar differs. Update needed.")
                        self.log_message("Local server.jar differs from latest release.")
                except Exception as e:
                    self.update_status(f"Error calculating local SHA1.")
                    self.log_message(f"Error calculating local SHA1: {e}")
                    self.log_message("Assuming update is needed due to SHA1 calculation error.")
                    need_update = True
            else:
                self.update_status("No server.jar found. Downloading.")
                self.log_message("No server.jar found. Downloading.")
                need_update = True

            # --- 7. Download if needed ---
            if need_update:
                self.update_status(f"Downloading updated server.jar (v{latest_version_id})...")
                self.log_message(f"Downloading updated server.jar from {server_jar_url}...")
                success = self._download_file(server_jar_url, local_server_jar_path)
                if success:
                    self.update_status(f"server.jar updated to version {latest_version_id}")
                    self.log_message(f"server.jar updated to version {latest_version_id}")
                    # After download, recalculate local SHA1 to show updated status
                    try:
                        updated_local_sha1 = self._calculate_file_sha1(local_server_jar_path).upper()
                        self.update_version_info(latest_version_id, f"Local SHA1: {updated_local_sha1[:8]}...")
                    except Exception:
                        self.update_version_info(latest_version_id, "Downloaded (SHA1 unknown)")
                else:
                    self.update_status("Failed to download server.jar. Aborting.")
                    self.log_message("Failed to download server.jar. Aborting.")
                    self.hide_progress_bar() # Hide on failure
                    return
            
            self.hide_progress_bar() # Hide progress bar after download is complete

            # --- 8. Cleanup ---
            self.update_status("Cleaning up temporary files...")
            self.log_message("Cleaning up temporary files...")
            for temp_file in ["manifest.json", "version.json"]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    self.log_message(f"Deleted {temp_file}")
            self.progress_bar.config(value=0) # Reset progress bar after download
            self.progress_bar_label.config(text="0%")

            # --- 9. Handle EULA ---
            self.update_status("Checking Minecraft EULA...")
            self.log_message("Checking Minecraft EULA...")
            if not os.path.exists(eula_path) or "eula=true" not in open(eula_path).read():
                self.log_message("EULA not accepted. Setting eula=true.")
                with open(eula_path, 'w') as f:
                    f.write("eula=true\n")
                self.log_message("eula.txt set to eula=true. Server will now start.")
            else:
                self.log_message("EULA already accepted.")


            # --- 10. Run server.jar ---
            self.update_status("Launching Minecraft server...") # Update status before launch
            self.log_message("Running server.jar...")
            
            command = ["java", "-Xmx1024M", "-Xms1024M", "-jar", local_server_jar_path, "nogui"]
            
            self.java_process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE, # Crucial for sending commands
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Enable command input fields using lambda
            self.master.after(0, lambda: self.command_entry.config(state='normal'))
            self.master.after(0, lambda: self.send_button.config(state='normal'))
            self.master.after(0, self.command_entry.focus_set) # Set focus to command input

            # Start a separate thread to read server output
            self.server_output_thread = threading.Thread(target=self._read_server_output, daemon=True)
            self.server_output_thread.start()
            
            # Set status to "Server running" AFTER process is confirmed launched
            self.master.after(0, self.update_status, "Server running...")


        except Exception as e:
            self.update_status(f"An error occurred: {e}")
            self.log_message(f"An unexpected error occurred: {e}")
        finally:
            # The 'finally' block in this thread should *not* reset status to Idle.
            # That's now handled by _read_server_output when the process truly ends.
            # However, ensure command input is disabled if the process didn't start successfully
            if self.java_process is None or self.java_process.poll() is not None:
                self.master.after(0, lambda: self.command_entry.config(state='disabled'))
                self.master.after(0, lambda: self.send_button.config(state='disabled'))
            self.progress_bar.config(value=0) # Ensure bar is reset if process didn't fully launch
            self.progress_bar_label.config(text="0%")
            self.hide_progress_bar() # Ensure hidden at the very end
            

    def _download_json(self, url, filename):
        """Downloads a JSON file and parses it, handling errors."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content) # For small JSON, just get all content
            
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except requests.exceptions.RequestException as e:
            self.log_message(f"Network error downloading {filename}: {e}")
            return None
        except json.JSONDecodeError as e:
            self.log_message(f"Error parsing JSON from {filename}: {e}")
            return None
        except IOError as e:
            self.log_message(f"File system error saving {filename}: {e}")
            return None

    def _download_file(self, url, filename):
        """Downloads a generic file, handling errors and updating progress."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_length = int(response.headers.get('content-length', 0))
            
            # Removed: self.master.after(0, lambda: self.progress_bar.config(maximum=total_length))
            # The maximum is now fixed at 100 in __init__
            self.update_progress(0, total_length) # Initialize progress
            
            downloaded = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_length > 0: # Only update meaningful progress if total is known
                        # Use lambda to correctly update progress from thread
                        self.master.after(0, lambda: self.update_progress(downloaded, total_length))
                    else: # For unknown size, reset the bar and show N/A
                        self.master.after(0, lambda: self.update_progress(0, 0)) # Indicate unknown progress

            self.log_message(f"Downloaded {filename}")
            return True
        except requests.exceptions.RequestException as e:
            self.log_message(f"Network error downloading {filename}: {e}")
            return False
        except IOError as e:
            self.log_message(f"File system error saving {filename}: {e}")
            return False

    def _calculate_file_sha1(self, filepath):
        """Calculates the SHA1 hash of a file."""
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    def on_quit(self):
        """Handles graceful exit, stopping Java process if running."""
        if self.java_process and self.java_process.poll() is None: # If process is still running
            self.log_message("Attempting to gracefully stop Minecraft server...")
            try:
                self.java_process.stdin.write("stop\n")
                self.java_process.stdin.flush()
                # Give server 60 seconds to shut down
                self.log_message("Waiting for server to save and shut down (max 60 seconds)...")
                self.update_status("Server shutting down...")
                self.java_process.wait(timeout=60) 
                self.log_message("Minecraft server stopped gracefully.")
            except (BrokenPipeError, ValueError, subprocess.TimeoutExpired) as e:
                self.log_message(f"Server did not stop gracefully ({e}). Forcing termination...")
                self.java_process.terminate()
                time.sleep(5) # Give it a moment
                if self.java_process.poll() is None:
                    self.log_message("Server still running. Forcing kill.")
                    self.java_process.kill()
            except Exception as e:
                self.log_message(f"An unexpected error occurred during server shutdown: {e}")
                if self.java_process.poll() is None: # If still running despite error
                    self.log_message("Forcing server termination as fallback.")
                    self.java_process.kill()

        # Ensure all background threads are finished or daemon
        if self.server_output_thread and self.server_output_thread.is_alive():
            # Daemon threads will exit when the main program exits, so no explicit action needed here
            pass 
            
        self.master.destroy() # Close the Tkinter window

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftServerUpdaterGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_quit) # Handle window close button
    root.mainloop()