import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from dev.prompt_generator.promt_generator import PromptGenerator, load_data

class PromptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Prompt Builder")
        self.data = load_data()  # should be schema.json
        self.generator = PromptGenerator(self.data)

        self.build_ui()

    def build_ui(self):
        frm = tk.Frame(self.root, padx=10, pady=10)
        frm.pack(fill="both", expand=True)

        # Mode selection
        tk.Label(frm, text="Prompt Mode:").grid(row=0, column=0, sticky="w")
        self.mode_var = tk.StringVar(value="timeline")
        ttk.Combobox(frm, textvariable=self.mode_var, values=["timeline", "influence_network", "biographical_summaries", "event_chronology", "philosophical_theme"]).grid(row=0, column=1, sticky="ew")

        # Time range
        tk.Label(frm, text="Start Year:").grid(row=1, column=0, sticky="w")
        self.start_entry = tk.Entry(frm)
        self.start_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(frm, text="End Year:").grid(row=2, column=0, sticky="w")
        self.end_entry = tk.Entry(frm)
        self.end_entry.grid(row=2, column=1, sticky="ew")

        # People and Events
        tk.Label(frm, text="People (comma-separated):").grid(row=3, column=0, sticky="w")
        self.people_entry = tk.Entry(frm)
        self.people_entry.grid(row=3, column=1, sticky="ew")

        tk.Label(frm, text="Events (comma-separated):").grid(row=4, column=0, sticky="w")
        self.events_entry = tk.Entry(frm)
        self.events_entry.grid(row=4, column=1, sticky="ew")

        # Filters
        tk.Label(frm, text="Filter by Region:").grid(row=5, column=0, sticky="w")
        self.region_filter = tk.Entry(frm)
        self.region_filter.grid(row=5, column=1, sticky="ew")

        tk.Label(frm, text="Filter by School of Thought:").grid(row=6, column=0, sticky="w")
        self.school_filter = tk.Entry(frm)
        self.school_filter.grid(row=6, column=1, sticky="ew")

        tk.Label(frm, text="Filter by Event Type:").grid(row=7, column=0, sticky="w")
        self.event_type_filter = tk.Entry(frm)
        self.event_type_filter.grid(row=7, column=1, sticky="ew")

        # Theme input for philosophical_theme mode
        tk.Label(frm, text="Philosophical Theme:").grid(row=8, column=0, sticky="w")
        self.theme_entry = tk.Entry(frm)
        self.theme_entry.grid(row=8, column=1, sticky="ew")

        # Detail level
        tk.Label(frm, text="Detail Level:").grid(row=9, column=0, sticky="w")
        self.detail_var = tk.StringVar(value="medium")
        ttk.Combobox(frm, textvariable=self.detail_var, values=["low", "medium", "high"]).grid(row=9, column=1, sticky="ew")

        # Generate button
        tk.Button(frm, text="Generate Prompt", command=self.generate_prompt).grid(row=10, column=0, columnspan=2, pady=10)

        # Prompt display (use correct row index here!)
        self.prompt_box = tk.Text(frm, height=20, wrap="word")
        self.prompt_box.grid(row=11, column=0, columnspan=2, sticky="nsew")

        # Save button
        tk.Button(frm, text="Save to File", command=self.save_prompt).grid(row=12, column=0, columnspan=2, pady=10)

        # Layout config
        frm.grid_columnconfigure(1, weight=1)
        frm.grid_rowconfigure(11, weight=1)



    def generate_prompt(self):
        try:
            mode = self.mode_var.get()
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())

            people_input = self.people_entry.get().strip()
            events_input = self.events_entry.get().strip()

            people = [name.strip() for name in people_input.split(",") if name.strip()]
            events = [name.strip() for name in events_input.split(",") if name.strip()]
            detail = self.detail_var.get()

            # === Gather Filters ===
            filters = {}

            # Theme filter (used only in philosophical_theme)
            theme_input = self.theme_entry.get().strip()
            if theme_input:
                filters["theme"] = [theme_input]


            region_input = self.region_filter.get().strip()
            if region_input:
                filters["region"] = [r.strip() for r in region_input.split(",") if r.strip()]

            school_input = self.school_filter.get().strip()
            if school_input:
                filters["school_of_thought"] = [s.strip() for s in school_input.split(",") if s.strip()]

            event_type_input = self.event_type_filter.get().strip()
            if event_type_input:
                filters["event_type"] = [t.strip() for t in event_type_input.split(",") if t.strip()]

            prompt = self.generator.generate(
                mode=mode,
                start_year=start,
                end_year=end,
                selected_people=people,
                selected_events=events,
                detail_level=detail,
                filters=filters or None
            )

            self.prompt_box.delete("1.0", tk.END)
            self.prompt_box.insert(tk.END, prompt)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def save_prompt(self):
        content = self.prompt_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Nothing to save", "Generate a prompt first.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Prompt saved to " + filepath)


if __name__ == "__main__":
    root = tk.Tk()
    app = PromptApp(root)
    root.mainloop()
