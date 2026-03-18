import customtkinter as ctk
import sys
import threading
import subprocess
import time
import os
from main import agency


# --- TEXT REDIRECTOR ---
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", string)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass


class AgencyDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CORE CONFIG ---
        self.title("🏢 NEURAL NEXUS v3.1 - CYBERNETIC FORGE")
        self.geometry("1200x850")

        # Colors
        self.COLOR_BG_BLACK = "#070708"
        self.COLOR_NEON_CYAN = "#00FFFF"
        self.COLOR_DEEP_CYAN = "#008B8B"
        self.COLOR_TEXT_PRIMARY = "#FFFFFF"
        self.COLOR_UI_PANEL_BG = "#0F0F13"
        self.COLOR_LAUNCH_GREEN = "#39FF14"
        self.COLOR_ERROR_RED = "#FF3131"

        self.configure(fg_color=self.COLOR_BG_BLACK)
        self.glow_value = 0

        # --- TOP HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side=ctk.TOP, fill=ctk.X, pady=(20, 10))

        self.title_label = ctk.CTkLabel(self.header_frame, text="NEURAL NEXUS v3.1",
                                        font=("Orbitron", 36, "bold"),
                                        text_color=self.COLOR_NEON_CYAN)
        self.title_label.pack()

        self.status_indicator = ctk.CTkLabel(self.header_frame, text="● SYSTEM STABLE",
                                             font=("Consolas", 13, "bold"), text_color=self.COLOR_LAUNCH_GREEN)
        self.status_indicator.pack()

        # --- MAIN CONTAINER ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill=ctk.BOTH, expand=True, padx=30, pady=10)
        self.main_container.grid_columnconfigure(0, weight=4)
        self.main_container.grid_columnconfigure(1, weight=6)
        self.main_container.grid_rowconfigure(0, weight=1)

        # --- LEFT PANEL (NEURAL BLUEPRINTS) ---
        self.left_panel = ctk.CTkFrame(self.main_container, fg_color=self.COLOR_UI_PANEL_BG,
                                       corner_radius=25, border_width=2, border_color=self.COLOR_NEON_CYAN)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        self.input_label = ctk.CTkLabel(self.left_panel, text="INPUT SPECIFICATIONS",
                                        font=("Arial", 16, "bold"), text_color=self.COLOR_TEXT_PRIMARY)
        self.input_label.pack(pady=(30, 5))

        self.prompt_input = ctk.CTkTextbox(self.left_panel, height=200,
                                           fg_color="#000000",
                                           text_color=self.COLOR_NEON_CYAN,
                                           font=("Consolas", 14),
                                           corner_radius=15,
                                           border_width=1, border_color=self.COLOR_DEEP_CYAN)
        self.prompt_input.pack(padx=25, pady=10, fill=ctk.X)

        # PROGRESS SECTION
        self.progress_label = ctk.CTkLabel(self.left_panel, text="SYNCING NEURAL NETS: 0%",
                                           font=("Consolas", 14, "bold"), text_color=self.COLOR_TEXT_PRIMARY)
        self.progress_label.pack(pady=(25, 5))

        self.progress_bar = ctk.CTkProgressBar(self.left_panel, orientation="horizontal",
                                               width=320, height=18,
                                               progress_color=self.COLOR_NEON_CYAN,
                                               fg_color="#1A1A1A",
                                               corner_radius=10)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=25, pady=5)

        # MAIN BUTTONS
        self.build_button = ctk.CTkButton(self.left_panel, text="LAUNCH NEXUS",
                                          font=("Arial", 18, "bold"),
                                          fg_color=self.COLOR_NEON_CYAN,
                                          text_color="#000000",
                                          hover_color="#00DCDC",
                                          height=60, corner_radius=15,
                                          command=self.run_agency_thread)
        self.build_button.pack(pady=15, padx=40, fill=ctk.X)

        self.reset_button = ctk.CTkButton(self.left_panel, text="↺ RESET SYSTEM",
                                          font=("Arial", 14, "bold"),
                                          fg_color="transparent",
                                          border_width=1,
                                          border_color="#555555",
                                          text_color="#AAAAAA",
                                          hover_color="#222222",
                                          height=40, corner_radius=15,
                                          command=self.reset_ui)
        self.reset_button.pack(pady=5, padx=40, fill=ctk.X)

        # LAUNCH APP BUTTON (Hidden initially)
        self.launch_button = ctk.CTkButton(self.left_panel, text="⚡ LAUNCH APP",
                                           font=("Arial", 18, "bold"),
                                           fg_color=self.COLOR_LAUNCH_GREEN,
                                           text_color="#000000",
                                           hover_color="#32CD32",
                                           height=60, corner_radius=15,
                                           command=self.launch_app)
        self.launch_button.pack_forget()

        # --- RIGHT PANEL (NEURAL STREAM) ---
        self.right_panel = ctk.CTkFrame(self.main_container, fg_color="#050505",
                                        corner_radius=25, border_width=1, border_color="#333333")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        self.log_label = ctk.CTkLabel(self.right_panel, text="LIVE AGENT NEURAL STREAM",
                                      font=("Arial", 16, "bold"), text_color=self.COLOR_NEON_CYAN)
        self.log_label.pack(pady=(20, 0))

        self.log_window = ctk.CTkTextbox(self.right_panel, fg_color="#000000",
                                         text_color="#00FF41", font=("Consolas", 13),
                                         corner_radius=20, border_width=0)
        self.log_window.pack(padx=20, pady=20, fill=ctk.BOTH, expand=True)
        self.log_window.insert("0.0", ">>> [CORE] NEXUS ONLINE\n>>> [CORE] AWAITING COMMANDS...\n")
        self.log_window.configure(state="disabled")

        sys.stdout = RedirectText(self.log_window)
        self.animate_glow()

    def animate_glow(self):
        """3D Breathing Glow effect on the panel border."""
        colors = ["#00FFFF", "#00AAAA", "#008888", "#00AAAA", "#00FFFF"]
        self.glow_value = (self.glow_value + 1) % len(colors)
        self.left_panel.configure(border_color=colors[self.glow_value])
        self.after(500, self.animate_glow)

    def update_progress_anim(self, target, duration):
        """Smoothly animates progress for 'GENESIS IN PROGRESS' phase."""
        current = self.progress_bar.get()
        steps = 30
        for i in range(steps):
            current += (target - current) / (steps - i)
            self.progress_bar.set(current)
            self.progress_label.configure(text=f"GENESIS IN PROGRESS... {int(current * 100)}%",
                                          text_color=self.COLOR_NEON_CYAN)
            self.update_idletasks()
            time.sleep(duration / steps)

    def reset_ui(self):
        """Reset the system to initial state."""
        self.prompt_input.delete("1.0", "end")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Forge Idle: 0%", text_color=self.COLOR_TEXT_PRIMARY)
        self.launch_button.pack_forget()
        self.build_button.configure(state="normal", text="LAUNCH NEXUS")
        self.status_indicator.configure(text="● SYSTEM STABLE", text_color=self.COLOR_LAUNCH_GREEN)
        print("\n>>> [SYSTEM] BUFFER PURGED. READY FOR NEW GENESIS.")

    def run_agency_thread(self):
        user_prompt = self.prompt_input.get("1.0", "end-1c")
        if not user_prompt.strip(): return

        self.launch_button.pack_forget()
        self.build_button.configure(state="disabled", text="EXECUTING...")
        self.status_indicator.configure(text="● AGENTS ENGAGED", text_color="orange")

        thread = threading.Thread(target=self.start_agency, args=(user_prompt,))
        thread.daemon = True
        thread.start()

    def start_agency(self, prompt):
        try:
            print(f"\n[NEURAL] INITIALIZING EXTRACTION FOR: {prompt}")
            self.update_progress_anim(0.35, 1.5)

            print("[NEURAL] OPTIMIZING OOP BLUEPRINT...")
            self.update_progress_anim(0.70, 2.5)

            agency.kickoff(inputs={'app_idea': prompt})

            self.update_progress_anim(1.0, 0.5)
            print("\n✅ MISSION SUCCESS: SOURCE CODE DEPLOYED.")

            self.status_indicator.configure(text="● BUILD READY", text_color=self.COLOR_LAUNCH_GREEN)
            self.after(0, lambda: self.launch_button.pack(pady=15, padx=40, fill=ctk.X))

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {str(e)}")
            self.status_indicator.configure(text="● CORE FAILURE", text_color="red")
        finally:
            self.after(0, lambda: self.build_button.configure(state="normal", text="LAUNCH NEXUS"))

    def launch_app(self):
        """Fixed Launch: Spawns the app in a new process so it's visible."""
        print("\n[SYSTEM] EXECUTING generated_app.py IN NEW RUNTIME...")
        filename = "generated_app.py"
        if os.path.exists(filename):
            # OS based runtime execution
            if os.name == 'nt':  # Windows
                subprocess.Popen(['start', 'cmd', '/k', sys.executable, filename], shell=True)
            else:  # Linux/Mac
                subprocess.Popen([sys.executable, filename])
        else:
            print(f"❌ Runtime Error: {filename} not found.")


if __name__ == "__main__":
    app = AgencyDashboard()
    app.attributes('-alpha', 0.98)
    app.mainloop()