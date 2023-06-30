    import tkinter as tk
    from tkinter import ttk
    import threading
    import pyautogui
    import pytesseract
    import cv2
    import numpy as np
    import time
    import re

    from fuzzywuzzy import fuzz
    from PIL import Image

    class TransparentWindow:
        def __init__(self):
            self.root = tk.Tk()
            self.root.overrideredirect(True)
            self.root.lift()
            self.root.wm_attributes('-topmost', True)

            self.area_x_start = 2246  # Início da área em X (3840 é a largura total da tela)
            self.area_x_end = 2390  # Fim da área em X
            self.area_y_start = 87  # Início da área em Y
            self.area_y_end = 250  # Fim da área em Y
            self.previous_screenshot = None  # Armazena a captura de tela anterior para comparação 

            self.drag_start = None

            self.root.bind("<ButtonPress-1>", self.start_drag)
            self.root.bind("<B1-Motion>", self.on_drag)
            self.root.bind("<ButtonRelease-1>", self.stop_drag)

            self.blacklist = []

            self.sections = []
            for _ in range(6):
                section_frame = ttk.Frame(self.root)
                section_frame.pack(padx=10, pady=0, fill=tk.X)

                name_label = ttk.Label(section_frame, text="")
                name_label.pack()

                progress_bar = ttk.Progressbar(section_frame, orient=tk.HORIZONTAL, mode='determinate')
                progress_bar.pack(fill=tk.X)

                timer_label = ttk.Label(section_frame, text="00:00")
                timer_label.pack()

                self.sections.append((name_label, progress_bar, timer_label))

            config_button = ttk.Button(self.root, text="Fechar", command=self.root.destroy)
            config_button.pack(pady=10)

            self.update_thread = None
            self.running = False

        def start(self):
            self.running = True
            self.update_thread = threading.Thread(target=self.update_interface)
            self.update_thread.start()

            self.root.mainloop()

        def stop(self):
            self.running = False
            if self.update_thread:
                self.update_thread.join()

        def update_interface(self):
            while self.running:
                # Captura de tela
                screenshot = pyautogui.screenshot(region=(self.area_x_start, self.area_y_start, self.area_x_end - self.area_x_start, self.area_y_end - self.area_y_start))
                # screenshot.save("screenshot.png")
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # Converte para o formato esperado pelo OpenCV

                # Aplica filtro para facilitar a leitura de texto vermelho em fundo marrom
                hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
                lower_red = np.array([0, 50, 50])
                upper_red = np.array([10, 255, 255])
                mask1 = cv2.inRange(hsv, lower_red, upper_red)
                lower_red = np.array([170, 50, 50])
                upper_red = np.array([180, 255, 255])
                mask2 = cv2.inRange(hsv, lower_red, upper_red)
                mask = cv2.bitwise_or(mask1, mask2)
                filtered_screenshot = cv2.bitwise_and(screenshot, screenshot, mask=mask)

                # Verifica se houve mudança na captura de tela
                if self.previous_screenshot is not None and np.array_equal(filtered_screenshot, self.previous_screenshot):
                    # Não houve mudança, nenhum jogador morreu
                    continue

                self.previous_screenshot = filtered_screenshot  # Atualiza a captura de tela anterior

                # Realiza o reconhecimento de texto na imagem
                text = pytesseract.image_to_string(
                    Image.fromarray(filtered_screenshot),
                    config='--psm 7',
                    lang='por',
                )

                if text.strip() and text not in self.blacklist and self.validate_name(text):
                    print(text)
                    # Verifica se o nome já está presente em alguma seção
                    name_exists = any(fuzz.ratio(text, name_label.cget("text")) > 50 for name_label, _, _ in self.sections)

                    # Atualiza a primeira seção existente com o nome encontrado
                    section_index = next((i for i, (name_label, _, _) in enumerate(self.sections) if not name_label.cget("text") and not name_exists), None)
                    if section_index is not None:
                        self.update_section(section_index, text)


                self.root.update()
                time.sleep(0.1)  # Adiciona um pequeno atraso para evitar consumo excessivo de recursos

        def update_section(self, section_index, name):
            name_label, progress_bar, timer_label = self.sections[section_index]
            name_label.configure(text=name)
            progress_bar.configure(value=31)
            timer_label.configure(text="30:00")

            self.start_countdown(section_index)
        
        def start_countdown(self, section_index):
            def countdown():
                progress_bar = self.sections[section_index][1]
                timer_label = self.sections[section_index][2]

                for i in range(31):
                    progress_bar.configure(value=i * 3)
                    timer_label.configure(text="{:02d}:{:02d}".format(0, 30 - i))
                    self.root.update()
                    time.sleep(1)

                    if i == 30:
                        self.reset_section(section_index)
            threading.Thread(target=countdown).start()
            
        def reset_section(self, section_index):
            name_label, progress_bar, timer_label = self.sections[section_index]
            name_label.configure(text="")
            progress_bar.configure(value=0)
            timer_label.configure(text="00:00")

        def open_config(self):
            config_window = tk.Toplevel(self.root)
            config_window.title("Configuração")

            blacklist_label = ttk.Label(config_window, text="Blacklist")
            blacklist_label.pack()

            blacklist_text = tk.Text(config_window, height=10, width=30)
            blacklist_text.pack()

            save_button = ttk.Button(config_window, text="Salvar", command=lambda: self.save_blacklist(blacklist_text))
            save_button.pack()

        def save_blacklist(self, blacklist_text):
            blacklist = blacklist_text.get("1.0", tk.END).strip().split("\n")
            self.blacklist = blacklist

        def start_drag(self, event):
            self.drag_start = event.x, event.y

        def on_drag(self, event):
            x = event.x_root - self.drag_start[0]
            y = event.y_root - self.drag_start[1]
            self.root.geometry("+{x}+{y}".format(x=x, y=y))

        def stop_drag(self, event):
            self.drag_start = None
            
        def validate_name(self, name):
            # Remove os espaços em branco da string
            name_without_spaces = name.replace(" ", "")

            # Verifica o comprimento mínimo do nome
            if len(name_without_spaces) < 4:
                return False


            # Verifica se o nome contém apenas letras e espaços
            if not re.match(r'^[a-zA-Z\s]+$', name):
                return False

            return True

    window = TransparentWindow()
    window.start()
