# 🕰️ Timeline GPT: Historical Influence Timeline Generator

**Timeline GPT** is a Python-based tool that generates rich, visually styled historical timelines from structured JSON data. It captures key figures, events, and intellectual influences across history, and renders them into clear, annotated timeline images.

---

## 📌 Features

- 📚 Supports historical figures with influences, summaries, quotes, and metadata
- 🌍 Includes global, major, and local events with categories and relationships
- 🎨 Customizable visual themes (`light`, `dark`, `parchment`)
- 🧠 GUI-based AI prompt generation for timeline creation
- 🖼️ Visual output with influence arrows and event bands
- 🧩 Modular design with pluggable renderers and data pipelines

---

## 🏗️ Project Structure

```
timeline_gpt/
├── dev/
│   ├── core/                 # Domain models for Person and Event
│   ├── renderers/           # Timeline renderers (e.g., BasicRenderer)
│   ├── themes/              # JSON config for color themes
│   ├── utils/               # Helper modules for loading, transforming, validating
│   └── prompt_generator/    # Prompt creation scripts and GUI
├── generated_timeline.json  # Input data with people & events
├── mock_timeline.py         # Example script to build a timeline
├── output_timeline.png      # Final generated timeline image
```

---

## 🚀 How to Run

### 🧪 Generate a Timeline from JSON

```bash
python main_launcher.py
```

This will:
- Open a window to select between the prompt generator or the timeline generator <img width="218" height="140" alt="image" src="https://github.com/user-attachments/assets/483549a0-fee1-4b27-b344-c8d040af9a48" />
- In the prompt generator you can choor between different modes and enter a start/end Year upon some other filters <img width="659" height="675" alt="image" src="https://github.com/user-attachments/assets/abd34d96-be84-4fa2-86cc-6248215a68f6" />
- You can generate the prompt and copy it out of the window below or save it to a text file
- The prompt is designed to create a downloadable json file as an output from the AI
- When selecting the timeline generator you can choose the generated json file <img width="1020" height="635" alt="image" src="https://github.com/user-attachments/assets/0d02c4c5-ed56-45d4-8490-e6f072729d62" />
- The program will choose the theme and renderer according to the config.json file at themes/config.json, it will then generate the timeline according to the data from the json file
- Append any "ghost" figures (referenced influencers not in the dataset)
- Render the timeline using your configured theme (default: `parchment`)
- Save output to `output_timeline.png`

### 🛠 Customize Theme

Modify `dev/themes/config.json` to change background, text color, event shades, and school-of-thought colors.

---

## 🧠 Generate Prompts with GUI

Use the built-in GUI tool to create JSON-generation prompts for the AI:

```bash
python dev/prompt_generator/prompt_gui.py
```

- Choose a mode: `timeline`, `influence_network`, or `biographical_summaries`
- Set a year range and add people or events
- Choose a detail level
- Generate and save prompt text

---

## 🧬 Data Format

See `dev/schema.json` for the complete schema. Key sections include:

### 👤 Person

```json
{
  "name": "Mao Zedong",
  "start": 1893,
  "end": 1976,
  "influences": [{ "target": "Karl Marx", "type": "ideological", "certainty": "high" }],
  "summary": "...",
  "quotes": [...],
  "school_of_thought": "...",
  "region": "..."
}
```

### 🗓️ Event

```json
{
  "name": "World War II",
  "start_year": 1939,
  "end_year": 1945,
  "description": "...",
  "type": "war",
  "scope": "global",
  "region": "Europe",
  "related_to": ["Hitler", "Stalin"]
}
```

---

## 🧪 Example Output

![Timeline Screenshot](<img width="1600" height="800" alt="image" src="https://github.com/user-attachments/assets/b376c7e1-fab3-401f-ba0b-895cd8420e6d" />
)

The visualization includes:
- Timelines of people
- Influence arrows between them
- Historical events placed proportionally
- Icons for war, discovery, birth (customizable in `assets/icons`)

---

## 📦 Requirements

- Python 3.8+
- `matplotlib`
- `tkinter` (for GUI)

Install with:

```bash
pip install matplotlib
```

---

## 🔧 Future Ideas

- Add interactive timeline export (e.g., HTML/JS)
- Auto-completion and suggestion in GUI
- Historical accuracy checks and prompts
