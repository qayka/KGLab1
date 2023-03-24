import tkinter as tk
import tkinter.colorchooser
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
import re
# import ttkthemes

class App:

    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.gridframe = tk.Frame(self.root)
        for col in range(4):
            self.gridframe.columnconfigure(index=col, weight=1)
        for row in range(9):
            self.gridframe.rowconfigure(index=row, weight=1)

        self.current_system = 'hls'

        def get_rgb(rgb):
            return "#%02x%02x%02x" % rgb

        def cmyk_to_rgb(c, m, y, k):
            r = 255 * (1 - c / 100) * (1 - k / 100)
            g = 255 * (1 - m / 100) * (1 - k / 100)
            b = 255 * (1 - y / 100) * (1 - k / 100)
            return int(r), int(g), int(b)

        def hls_to_rgb(h, l, s):
            l /= 100
            s /= 100
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = l - c / 2
            rgb_p = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x), (c, 0, x)]
            rgb = rgb_p[int(h / 60)]
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            return int(255 * (r + m)), int(255 * (g + m)), int(255 * (b + m))

        def rgb_to_cmyk(r, g, b):
            r /= 255
            g /= 255
            b /= 255
            k = 1 - max(r, g, b)
            if r == g == b == 0:
                return 0, 0, 0, 100
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
            return int(c * 100), int(m * 100), int(y * 100), int(k * 100)

        def rgb_to_hls(r, g, b):
            r /= 255
            g /= 255
            b /= 255
            c_max = max(r, g, b)
            c_min = min(r, g, b)
            delta = c_max - c_min

            l = (c_max + c_min) / 2
            s = 0 if delta == 0 else delta / (1 - abs(2 * l - 1))
            h = 60
            if delta == 0:
                h *= 0
            elif c_max == r:
                h *= (g - b) / delta % 6
            elif c_max == g:
                h *= (b - r) / delta + 2
            elif c_max == b:
                h *= (r - g) / delta + 4
            return int(h), int(l * 100), int(s * 100)

        canvas = tk.Canvas(bg="white", width=300, height=100)
        canvas.grid(row=0, column=0, columnspan=4, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSEW")

        rgb = "RGB"
        cmyk = "CMYK"
        hls = "HLS"

        self.model = tk.StringVar(value=rgb)


        def disable_rgb():
            entry_r.config(state='disabled')
            entry_g.config(state='disabled')
            entry_b.config(state='disabled')
            scale_r.config(state='disabled')
            scale_g.config(state='disabled')
            scale_b.config(state='disabled')

        def disable_cmyk():
            entry_c.config(state='disabled')
            entry_m.config(state='disabled')
            entry_y.config(state='disabled')
            entry_k.config(state='disabled')
            slider_c.config(state='disabled')
            slider_m.config(state='disabled')
            slider_y.config(state='disabled')
            slider_k.config(state='disabled')

        def disable_hls():
            entry_h.config(state='disabled')
            entry_l.config(state='disabled')
            entry_s.config(state='disabled')
            slider_h.config(state='disabled')
            slider_l.config(state='disabled')
            slider_s.config(state='disabled')

        def enable_rgb():
            entry_r.config(state='normal')
            entry_g.config(state='normal')
            entry_b.config(state='normal')
            scale_r.config(state='normal')
            scale_g.config(state='normal')
            scale_b.config(state='normal')

        def enable_cmyk():
            entry_c.config(state='normal')
            entry_m.config(state='normal')
            entry_y.config(state='normal')
            entry_k.config(state='normal')
            slider_c.config(state='normal')
            slider_m.config(state='normal')
            slider_y.config(state='normal')
            slider_k.config(state='normal')

        def enable_hls():
            entry_h.config(state='normal')
            entry_l.config(state='normal')
            entry_s.config(state='normal')
            slider_h.config(state='normal')
            slider_l.config(state='normal')
            slider_s.config(state='normal')

        def enable_all():
            enable_rgb()
            enable_hls()
            enable_cmyk()

        def rgb_select():
            self.current_system = self.model.get().lower()
            enable_rgb()
            disable_cmyk()
            disable_hls()

        def cmyk_select():
            self.current_system = self.model.get().lower()
            enable_cmyk()
            disable_hls()
            disable_rgb()

        def hls_select():
            self.current_system = self.model.get().lower()
            enable_hls()
            disable_cmyk()
            disable_rgb()

        btn_rgb = ttk.Radiobutton(text=rgb, value=rgb, variable=self.model, command=rgb_select)
        btn_rgb.grid(row=1, column=0, ipadx=6, ipady=6, padx=40, pady=4, sticky="NSEW")

        btn_cmyk = ttk.Radiobutton(text=cmyk, value=cmyk, variable=self.model, command=cmyk_select)
        btn_cmyk.grid(row=1, column=1, columnspan=2, ipadx=6, ipady=6, padx=80, pady=4, sticky="NSEW")

        btn_hls = ttk.Radiobutton(text=hls, value=hls, variable=self.model, command=hls_select)
        btn_hls.grid(row=1, column=3, ipadx=6, ipady=6, padx=30, pady=4, sticky="NSEW")


        # RGB

        val_r = tk.IntVar(0)
        val_g = tk.IntVar(0)
        val_b = tk.IntVar(0)

        def key_r(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_r.set(int(newval))
                if self.current_system == 'rgb':
                    set_all_based_on_rgb()
            return result

        def key_g(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_g.set(int(newval))
                if self.current_system == 'rgb':
                    set_all_based_on_rgb()
            return result

        def key_b(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_b.set(int(newval))
                if self.current_system == 'rgb':
                    set_all_based_on_rgb()
            return result

        check_r = (self.root.register(key_r), "%P")
        check_g = (self.root.register(key_g), "%P")
        check_b = (self.root.register(key_b), "%P")

        entry_r = ttk.Entry(width=5, validate="key", validatecommand=check_r)
        entry_g = ttk.Entry(width=5, validate="key", validatecommand=check_g)
        entry_b = ttk.Entry(width=5, validate="key", validatecommand=check_b)

        entry_r.grid(row=2, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_g.grid(row=2, column=1, columnspan=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_b.grid(row=2, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

        ttk.Label(text="R").grid(row=2, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")
        ttk.Label(text="G").grid(row=2, column=1, columnspan=2, ipadx=6, ipady=6, padx=65, pady=4, sticky="NSW")
        ttk.Label(text="B").grid(row=2, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")

        def set_entry_rgb(r, g, b):
            entry_r.delete(0, "end")
            entry_g.delete(0, "end")
            entry_b.delete(0, "end")
            entry_r.insert(0, str(r))
            entry_g.insert(0, str(g))
            entry_b.insert(0, str(b))

        def set_all_based_on_rgb():
            enable_all()
            canvas.configure(background=get_rgb((val_r.get(), val_g.get(), val_b.get())))
            hls = rgb_to_hls(val_r.get(), val_g.get(), val_b.get())
            set_entry_hls(hls[0], hls[1], hls[2])
            cmyk = rgb_to_cmyk(val_r.get(), val_g.get(), val_b.get())
            set_entry_cmyk(cmyk[0], cmyk[1], cmyk[2], cmyk[3])
            disable_cmyk()
            disable_hls()


        def slider_rgb(new_val):
            set_all_based_on_rgb()
            set_entry_rgb(val_r.get(), val_g.get(), val_b.get())

        scale_r = tk.Scale(orient="horizontal", length=100, from_=0, to=255, variable=val_r, resolution=1, showvalue=0, command=slider_rgb)
        scale_g = tk.Scale(orient="horizontal", length=100, from_=0, to=255, variable=val_g, showvalue=0, command=slider_rgb)
        scale_b = tk.Scale(orient="horizontal", length=100, from_=0, to=255, variable=val_b, showvalue=0, command=slider_rgb)

        scale_r.grid(row=3, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        scale_g.grid(row=3, column=1, columnspan=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        scale_b.grid(row=3, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

        # CMYK

        val_c = tk.IntVar(0)
        val_m = tk.IntVar(0)
        val_y = tk.IntVar(0)
        val_k = tk.IntVar(0)

        def key_c(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|100)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_c.set(int(newval))
                if self.current_system == 'cmyk':
                    set_all_based_on_cmyk()
            return result

        def key_m(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|100)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_m.set(int(newval))
                if self.current_system == 'cmyk':
                    set_all_based_on_cmyk()
            return result

        def key_y(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|100)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_y.set(int(newval))
                if self.current_system == 'cmyk':
                    set_all_based_on_cmyk()
            return result

        def key_k(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|100)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_k.set(int(newval))
                if self.current_system == 'cmyk':
                    set_all_based_on_cmyk()
            return result

        check_c = (self.root.register(key_c), "%P")
        check_m = (self.root.register(key_m), "%P")
        check_y = (self.root.register(key_y), "%P")
        check_k = (self.root.register(key_k), "%P")

        entry_c = ttk.Entry(width=5, validate="key", validatecommand=check_c)
        entry_m = ttk.Entry(width=5, validate="key", validatecommand=check_m)
        entry_y = ttk.Entry(width=5, validate="key", validatecommand=check_y)
        entry_k = ttk.Entry(width=5, validate="key", validatecommand=check_k)

        entry_c.grid(row=4, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_m.grid(row=4, column=1, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_y.grid(row=4, column=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_k.grid(row=4, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

        ttk.Label(text="C").grid(row=4, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")
        ttk.Label(text="M").grid(row=4, column=1, ipadx=6, ipady=6, padx=0, pady=4, sticky="NSW")
        ttk.Label(text="Y").grid(row=4, column=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")
        ttk.Label(text="K").grid(row=4, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")

        def set_entry_cmyk(c, m, y, k):
            entry_c.delete(0, "end")
            entry_m.delete(0, "end")
            entry_y.delete(0, "end")
            entry_k.delete(0, "end")
            entry_c.insert(0, str(c))
            entry_m.insert(0, str(m))
            entry_y.insert(0, str(y))
            entry_k.insert(0, str(k))

        def set_all_based_on_cmyk():
            enable_all()
            rgb = cmyk_to_rgb(val_c.get(), val_m.get(), val_y.get(), val_k.get())
            canvas.configure(background=get_rgb(rgb))
            set_entry_rgb(rgb[0], rgb[1], rgb[2])
            hls = rgb_to_hls(rgb[0], rgb[1], rgb[2])
            set_entry_hls(hls[0], hls[1], hls[2])
            disable_rgb()
            disable_hls()


        def slider_cmyk(new_val):
            set_all_based_on_cmyk()
            set_entry_cmyk(val_c.get(), val_m.get(), val_y.get(), val_k.get())


        slider_c = tk.Scale(orient="horizontal", length=100, from_=0, to=100, variable=val_c, resolution=1, showvalue=0, command=slider_cmyk)
        slider_m = tk.Scale(orient="horizontal", length=100, from_=0, to=100, variable=val_m, resolution=1, showvalue=0, command=slider_cmyk)
        slider_y = tk.Scale(orient="horizontal", length=100, from_=0, to=100, variable=val_y, resolution=1, showvalue=0, command=slider_cmyk)
        slider_k = tk.Scale(orient="horizontal", length=100, from_=0, to=100, variable=val_k, resolution=1, showvalue=0, command=slider_cmyk)

        slider_c.grid(row=5, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        slider_m.grid(row=5, column=1, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        slider_y.grid(row=5, column=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        slider_k.grid(row=5, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

        # HLS

        val_h = tk.IntVar(0)
        val_l = tk.IntVar(0)
        val_s = tk.IntVar(0)

        def key_h(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|[1-2][0-9][0-9]|3[0-5][0-9]|360)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_h.set(int(newval))
                if self.current_system == 'hls':
                    set_all_based_on_hls()
            return result

        def key_l(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|100)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_l.set(int(newval))
                if self.current_system == 'hls':
                    set_all_based_on_hls()
            return result

        def key_s(newval):
            result = re.match("^$|^([0-9]|[1-9][0-9]|100)$", newval) is not None
            if result:
                if re.match("^$", newval):
                    return result
                val_s.set(int(newval))
                if self.current_system == 'hls':
                    set_all_based_on_hls()
            return result

        check_h = (self.root.register(key_h), "%P")
        check_l = (self.root.register(key_l), "%P")
        check_s = (self.root.register(key_s), "%P")

        entry_h = ttk.Entry(width=5, validate="key", validatecommand=check_h)
        entry_l = ttk.Entry(width=5, validate="key", validatecommand=check_l)
        entry_s = ttk.Entry(width=5, validate="key", validatecommand=check_s)

        entry_h.grid(row=6, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_l.grid(row=6, column=1, columnspan=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        entry_s.grid(row=6, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

        ttk.Label(text="H").grid(row=6, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")
        ttk.Label(text="L").grid(row=6, column=1, columnspan=2, ipadx=6, ipady=6, padx=65, pady=4, sticky="NSW")
        ttk.Label(text="S").grid(row=6, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NSW")

        def set_entry_hls(h, l, s):
            entry_h.delete(0, "end")
            entry_l.delete(0, "end")
            entry_s.delete(0, "end")
            entry_h.insert(0, str(h))
            entry_l.insert(0, str(l))
            entry_s.insert(0, str(s))

        def set_all_based_on_hls():
            enable_all()
            rgb = hls_to_rgb(val_h.get(), val_l.get(), val_s.get())
            canvas.configure(background=get_rgb(rgb))
            set_entry_rgb(rgb[0], rgb[1], rgb[2])
            cmyk = rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
            set_entry_cmyk(cmyk[0], cmyk[1], cmyk[2], cmyk[3])
            disable_rgb()
            disable_cmyk()

        def slider_hls(new_val):
            set_all_based_on_hls()
            set_entry_hls(val_h.get(), val_l.get(), val_s.get())


        slider_h = tk.Scale(orient="horizontal", length=100, from_=0, to=360, variable=val_h, resolution=1, showvalue=0,
                            command=slider_hls)
        slider_l = tk.Scale(orient="horizontal", length=100, from_=0, to=100, variable=val_l, resolution=1, showvalue=0,
                            command=slider_hls)
        slider_s = tk.Scale(orient="horizontal", length=100, from_=0, to=100, variable=val_s, resolution=1, showvalue=0,
                            command=slider_hls)

        slider_h.grid(row=7, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        slider_l.grid(row=7, column=1, columnspan=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")
        slider_s.grid(row=7, column=3, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

        rgb_select()

        def select_color():
            result = colorchooser.askcolor(initialcolor="black")
            rgb = result[0]
            val_r.set(int(rgb[0]))
            val_g.set(rgb[1])
            val_b.set(rgb[2])
            slider_rgb("useless value")
            self.model.set(0)

        open_button = ttk.Button(text="Choose color", command=select_color)
        open_button.grid(row=8, column=1, columnspan=2, ipadx=6, ipady=6, padx=4, pady=4, sticky="NS")

if __name__ == '__main__':
    app = App()
    app.root.title("Dictionary redactor")
    app.root.mainloop()

