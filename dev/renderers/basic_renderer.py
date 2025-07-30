from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Rectangle, FancyArrowPatch
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class BasicRenderer:
    def __init__(self, config, theme_name="light"):
        self.theme = config["THEMES"][theme_name]
        self.school_colors = config.get("SCHOOL_COLORS", {})

    def render(self, persons, events, output_path="timeline.png"):
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, FancyArrowPatch
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        import os

        fig, ax = plt.subplots(figsize=(16, 8))

        # === Apply theme colors ===
        bg = self.theme["background"]
        fg = self.theme["text_color"]
        grid = self.theme["grid_color"]
        event_colors = self.theme["event_colors"]

        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)
        ax.tick_params(colors=fg)
        ax.xaxis.label.set_color(fg)
        ax.yaxis.label.set_color(fg)
        ax.title.set_color(fg)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5, color=grid)

        box_height = 0.8
        box_padding = 0.5
        name_to_coords = {}
        all_years = []

        # === Draw person boxes ===
        for i, person in enumerate(persons):
            start = person.parsed_start()
            end = person.parsed_end()
            y = i * (box_height + box_padding)

            is_ghost = start is None or end is None
            if is_ghost:
                start = 1900 + i * 10
                end = start + 5
                label = f"{person.name}\n(context only)"
                fill_color = "#999999"
                linestyle = (0, (4, 2))  # dashed
            else:
                label = f"{person.name}\n{person.start}–{person.end}\n{person.school_of_thought or ''}"
                fill_color = self.school_colors.get(person.school_of_thought, "black")
                linestyle = "solid"

            edge_color = fg
            all_years.extend([start, end])
            width = end - start

            rect = Rectangle((start, y), width, box_height,
                            facecolor=fill_color,
                            edgecolor=edge_color,
                            linewidth=1.5,
                            linestyle=linestyle)
            ax.add_patch(rect)

            ax.text(start + width / 2, y + box_height / 2, label,
                    ha='center', va='center', fontsize=8, color='white')

            name_to_coords[person.name] = (start, end, y + box_height / 2)

        # === Influence arrows ===
        for person in persons:
            src_coords = name_to_coords.get(person.name)
            if not src_coords:
                continue
            _, src_end, src_y = src_coords

            for influence in person.influences:
                tgt_coords = name_to_coords.get(influence.target)
                if not tgt_coords:
                    continue
                tgt_start, _, tgt_y = tgt_coords
                arrow = FancyArrowPatch((src_end, src_y), (tgt_start, tgt_y),
                                        connectionstyle="arc3,rad=0.2",
                                        arrowstyle="->", color='gray', lw=1.8)
                ax.add_patch(arrow)

        # === Events ===
        y_event = len(persons) * (box_height + box_padding) + 1
        for event in events:
            color = event_colors.get(event.scope, "black")
            s = event.start_year
            e = event.end_year
            all_years.append(s)
            if e:
                all_years.append(e)
                ax.axvspan(s, e, color=color, alpha=0.2)
                ax.text((s + e) / 2, y_event, event.name, ha='center', va='bottom', fontsize=7, rotation=90, color=fg)
            else:
                ax.axvline(s, linestyle=':', color=color, alpha=0.7)
                ax.text(s, y_event, event.name, rotation=90, ha='center', va='bottom', fontsize=7, color=fg)

            # Draw icon (optional)
            if hasattr(event, "type") and event.type:
                icon_path = f"assets/icons/{event.type}.png"
                if os.path.exists(icon_path):
                    try:
                        img = mpimg.imread(icon_path)
                        imagebox = OffsetImage(img, zoom=0.04)
                        ab = AnnotationBbox(imagebox, (s, y_event + 0.4), frameon=False)
                        ax.add_artist(ab)
                    except Exception as e:
                        print(f"⚠️ Failed to render icon {icon_path}: {e}")

        # === Set axis limits dynamically based on all_years ===
        if all_years:
            ax.set_xlim(min(all_years) - 10, max(all_years) + 10)
        ax.set_ylim(-1, y_event + 2)
        ax.set_yticks([])

        # === Final layout and save ===
        try:
            plt.tight_layout()
        except Exception as e:
            print(f"⚠️ tight_layout() adjustment failed: {e}")
            plt.subplots_adjust(left=0.1, right=0.9)

        plt.savefig(output_path)
        plt.close()


    def draw_icon(self, ax, x, y, path, zoom=0.04):
        if not os.path.exists(path):
            return
        try:
            img = mpimg.imread(path)
            imagebox = OffsetImage(img, zoom=zoom)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f"⚠️ Failed to render icon {path}: {e}")
