import tkinter as tk
from tkinter import simpledialog, messagebox, font as tkfont
from report_card import Subject, Period, ReportCard

class BoletimApp:
    def __init__(self, root):
        # Main presets
        self.root = root
        self.root.title("Boletim Escolar")
        self.root.geometry("1280x720")

        self.period_count = 0

        self.report_card = ReportCard()
        
        self.create_main_frames()
        self.create_period_display_area()

        self.button_font = tkfont.Font(family="Arial", size=50)
        self.root.bind("<Configure>", self.update_button_font)

        self.add_period_button = tk.Button(self.aux_frame, text="Adicionar Período", font=self.button_font, command=self.add_period)
        self.add_period_button.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.8, relheight=0.1)

        self.load_report_card = tk.Button(self.aux_frame, text="Carregar Boletim", font=self.button_font, command=self.load_report_card_periods)
        self.load_report_card.place(relx=0.5, rely=0.68, anchor="center", relwidth=0.8, relheight=0.1)

        self.save_report_card = tk.Button(self.aux_frame, text="Salvar Boletim", font=self.button_font, command=self.save_report_card_to_file)
        self.save_report_card.place(relx=0.5, rely=0.56, anchor="center", relwidth=0.8, relheight=0.1)

    def create_main_frames(self):
        self.main_frame = tk.Frame(self.root, bd=10, relief="sunken")
        self.main_frame.place(relx=0, rely=0, relwidth=0.8, relheight=1.0)

        self.aux_frame = tk.Frame(self.root, bd=10, relief="sunken")
        self.aux_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1.0)

    def create_period_display_area(self):
        container = tk.Frame(self.main_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_button_font(self, event=None):
        height = self.aux_frame.winfo_height()
        width = self.aux_frame.winfo_width()
        avg = (width + height) / 2

        new_font_size = max(10, int(avg * 0.02))
        self.button_font.configure(size=new_font_size)

    def add_period(self):
        period_name = simpledialog.askstring("Nome do Período", "Digite o nome do novo período:")
        if not period_name:
            return

        if any(p.name == period_name for p in self.report_card.periods):
            messagebox.showerror("Erro", "Já existe um período com esse nome.")
            return
        
        self.period_count += 1
        new_period = Period(period_name)
        self.report_card.insert_period(new_period)

        self.add_gui_period(period_name)
        messagebox.showinfo("Sucesso!", "Período carregado com sucesso!")

    def add_gui_period(self, period_name):
        period = next((p for p in self.report_card.periods if p.name == period_name), None)
        if period is None:
            return

        frame = tk.LabelFrame(self.scrollable_frame, text=period_name, padx=10, pady=10, font=("Arial", 14))
        frame.pack(fill="x", pady=10, padx=10)

        if not period.subjects:
            label = tk.Label(frame, text="(Nenhuma matéria ainda)", font=("Arial", 12))
            label.pack(anchor="w")
        else:
            header = tk.Frame(frame)
            header.pack(fill="x", pady=(0, 5))
            tk.Label(header, text="Matéria", width=37, anchor="w", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(header, text="Nota", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(header, text="Créditos", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(header, text="Resultado", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")

            for subject in period.subjects:
                row = tk.Frame(frame)
                row.pack(fill="x", pady=2)

                tk.Label(row, text=str(subject.name), width=41, anchor="w", font=("Arial", 12)).pack(side="left")
                tk.Label(row, text=str(subject.grade), width=16, anchor="center", font=("Arial", 12)).pack(side="left")
                tk.Label(row, text=str(subject.credits), width=15, anchor="center", font=("Arial", 12)).pack(side="left")
                tk.Label(row, text="Aprovado" if subject.result else "Reprovado", width=16, anchor="center", font=("Arial", 12)).pack(side="left")

                remove_button = tk.Button(row, text="Remover", font=("Arial", 10),
                                  command=lambda s=subject, p=period: self.remove_subject(p, s))
                remove_button.pack(side="left", padx=5)

        add_subject_btn = tk.Button(frame, text="Adicionar Matéria", font=("Arial", 12),
                                    command=lambda p=period: self.add_subject_dialog(p))
        add_subject_btn.pack(anchor="w", pady=(5, 0))

        remove_btn = tk.Button(frame, text="X", font=("Arial", 12, "bold"), fg="red",
                               command=lambda p=period: self.remove_period(p))
        remove_btn.place(relx=1.0, x=0, y=0, anchor="ne")

        stats_frame = tk.Frame(frame)
        stats_frame.pack(fill="x", pady=10)

        index = self.report_card.periods.index(period) + 1

        period_average = period.calculate_period_average()
        period_credits = period.calculate_period_credits()
        earned_period_credits = period.calculate_period_earned_credits()
        period_fails = period.calculate_period_fails()
        total_average = self.report_card.calculate_current_total_average(index)
        total_credits = self.report_card.calculate_current_total_credits(index)
        total_earned_credits = self.report_card.calculate_current_total_earned_credits(index)
        total_reprov = self.report_card.calculate_current_total_fails(index)

        stats_text = (
            f"Média do Período: {period_average:.2f}   Créditos do Período: {period_credits:.2f}   Créditos Obtidos: {earned_period_credits:.2f}   Reprovações: {period_fails}\n"
            f"Média Total: {total_average:.2f}    Créditos Acumulados: {total_credits:.2f}   CRO Total: {total_earned_credits:.2f}   Total de Reprovações: {total_reprov}"
        )
        tk.Label(stats_frame, text=stats_text, font=("Arial", 10, "bold"), anchor="center").pack()

    def add_subject_dialog(self, period):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Adicionar matéria - {period.name}")
        dialog.geometry("350x250")
        dialog.grab_set()

        tk.Label(dialog, text="Nome da Matéria:").pack(pady=5)
        entry_name = tk.Entry(dialog)
        entry_name.pack(pady=5, fill="x", padx=10)

        tk.Label(dialog, text="Nota:").pack(pady=5)
        entry_grade = tk.Entry(dialog)
        entry_grade.pack(pady=5, fill="x", padx=10)

        tk.Label(dialog, text="Créditos:").pack(pady=5)
        entry_credits = tk.Entry(dialog)
        entry_credits.pack(pady=5, fill="x", padx=10)

        def on_add():
            try:
                name = entry_name.get().strip()
                grade = float(entry_grade.get())
                credits = float(entry_credits.get())
                if not name:
                    raise ValueError("Nome da matéria vazio")

                subject = Subject(name, grade, credits)
                period.insert_subject(subject)

                dialog.destroy()
                self.refresh_display()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar matéria: {e}")

        btn_add = tk.Button(dialog, text="Adicionar", command=on_add)
        btn_add.pack(pady=10)

    def remove_subject(self, period, subject):
        confirm = messagebox.askyesno("Confirmar", f"Remover a matéria '{subject.name}'?")
        if confirm:
            period.delete_subject(subject)
            self.refresh_display()

    def remove_period(self, period):
        confirm = messagebox.askyesno("Confirmar", f"Remover o período '{period.name}'?")
        if confirm:
            self.report_card.delete_period(period)
            self.period_count -= 1
            self.refresh_display()
            messagebox.showinfo("Sucesso!", "Período removido com sucesso!")

    def refresh_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for p in self.report_card.periods:
            self.add_gui_period(p.name)

    def load_report_card_periods(self):
        self.report_card.load_from_file_json("report_card_save.json")
        self.period_count = 0
        self.refresh_display()
        messagebox.showinfo("Sucesso!", "Período carregado com sucesso!")

    def save_report_card_to_file(self):
        self.report_card.save_to_file_json("report_card_save.json")
        messagebox.showinfo("Sucesso", "Boletim salvo com sucesso!")

def startWindow():
    root = tk.Tk()
    app = BoletimApp(root)
    root.mainloop()
