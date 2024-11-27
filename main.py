import tkinter as tk
from tkinter import colorchooser

class ColorConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Model Converter")

        self.r = tk.IntVar(value=255)
        self.g = tk.IntVar(value=0)
        self.b = tk.IntVar(value=0)

        self.c = tk.DoubleVar(value=0)
        self.m = tk.DoubleVar(value=0)
        self.y = tk.DoubleVar(value=0)
        self.k = tk.DoubleVar(value=0)

        self.l = tk.DoubleVar(value=100)
        self.a = tk.DoubleVar(value=0)
        self.b_lab = tk.DoubleVar(value=0)

        self.create_widgets()

    def create_widgets(self):
        rgb_frame = tk.Frame(self.root)
        rgb_frame.pack(pady=10)

        tk.Label(rgb_frame, text="RGB Colors").grid(row=0, columnspan=3)

        tk.Scale(rgb_frame, from_=0, to=255, variable=self.r, orient='horizontal', label='Red', command=self.update_rgb).grid(row=1, column=0)
        tk.Scale(rgb_frame, from_=0, to=255, variable=self.g, orient='horizontal', label='Green', command=self.update_rgb).grid(row=1, column=1)
        tk.Scale(rgb_frame, from_=0, to=255, variable=self.b, orient='horizontal', label='Blue', command=self.update_rgb).grid(row=1, column=2)

        cmyk_frame = tk.Frame(self.root)
        cmyk_frame.pack(pady=10)

        tk.Label(cmyk_frame, text="CMYK Colors").grid(row=0, columnspan=4)

        tk.Scale(cmyk_frame, from_=0, to=100, variable=self.c, orient='horizontal', label='Cyan', command=self.update_cmyk).grid(row=1, column=0)
        tk.Scale(cmyk_frame, from_=0, to=100, variable=self.m, orient='horizontal', label='Magenta', command=self.update_cmyk).grid(row=1, column=1)
        tk.Scale(cmyk_frame, from_=0, to=100, variable=self.y, orient='horizontal', label='Yellow', command=self.update_cmyk).grid(row=1, column=2)
        tk.Scale(cmyk_frame, from_=0, to=100, variable=self.k, orient='horizontal', label='Key/Black', command=self.update_cmyk).grid(row=1, column=3)

        lab_frame = tk.Frame(self.root)
        lab_frame.pack(pady=10)

        tk.Label(lab_frame, text="LAB Colors").grid(row=0, columnspan=3)

        tk.Scale(lab_frame, from_=0, to=100, variable=self.l, orient='horizontal', label='L*', command=self.update_lab).grid(row=1, column=0)
        tk.Scale(lab_frame, from_=-128, to=127, variable=self.a, orient='horizontal', label='a*', command=self.update_lab).grid(row=1, column=1)
        tk.Scale(lab_frame, from_=-128, to=127, variable=self.b_lab, orient='horizontal', label='b*', command=self.update_lab).grid(row=1, column=2)

        color_button = tk.Button(self.root, text="Choose Color", command=self.choose_color)
        color_button.pack(pady=(10))

    def choose_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            rgb = color[0]
            self.r.set(int(rgb[0]))
            self.g.set(int(rgb[1]))
            self.b.set(int(rgb[2]))
            self.update_rgb()

    def update_rgb(self, event=None):
        r, g, b = self.r.get(), self.g.get(), self.b.get()
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.root.configure(bg=hex_color)
        cmyk = rgb_to_cmyk(r, g, b)
        if cmyk:
            self.c.set(cmyk[0])
            self.m.set(cmyk[1])
            self.y.set(cmyk[2])
            self.k.set(cmyk[3])
        lab = rgb_to_lab(r, g, b)
        if lab:
            self.l.set(lab[0])
            self.a.set(lab[1])
            self.b_lab.set(lab[2])

    def update_cmyk(self, event=None):
        c, m, y = self.c.get(), self.m.get(), self.y.get()
        r, g, b = cmyk_to_rgb(c, m, y, self.k.get())
        self.r.set(r)
        self.g.set(g)
        self.b.set(b)
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.root.configure(bg=hex_color)
        lab = rgb_to_lab(r, g, b)
        if lab:
            self.l.set(lab[0])
            self.a.set(lab[1])
            self.b_lab.set(lab[2])

    def update_lab(self, event=None):
        l, a, b_lab = self.l.get(), self.a.get(), self.b_lab.get()
        r, g, b = lab_to_rgb(l, a, b_lab)
        self.r.set(r)
        self.g.set(g)
        self.b.set(b)
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.root.configure(bg=hex_color)
        cmyk = rgb_to_cmyk(r, g, b)
        if cmyk:
            self.c.set(cmyk[0])
            self.m.set(cmyk[1])
            self.y.set(cmyk[2])
            self.k.set(cmyk[3])

def rgb_to_cmyk(r, g, b):
    if r == 0 and g == 0 and b == 0:
        return 0.0, 0.0, 0.0, 100.0
    c, m, y = 1 - r / 255.0, 1 - g / 255.0, 1 - b / 255.0
    k = min(c, m, y)
    c, m, y = (c - k) / (1 - k) * 100, (m - k) / (1 - k) * 100, (y - k) / (1 - k) * 100
    return round(c), round(m), round(y), round(k * 100)

def cmyk_to_rgb(c, m, y, k):
    r, g, b = int(255 * (1 - c / 100) * (1 - k / 100)), int(255 * (1 - m / 100) * (1 - k / 100)), int(255 * (1 - y / 100) * (1 - k / 100))
    return r, g, b

def rgb_to_lab(r, g, b):
    var_R = r / 255.0
    var_G = g / 255.0
    var_B = b / 255.0

    var_R = ((var_R > 0.04045) * ((var_R + 0.055) / 1.055) ** 2.4 + (var_R <= 0.04045) * (var_R / 12.92))
    var_G = ((var_G > 0.04045) * ((var_G + 0.055) / 1.055) ** 2.4 + (var_G <= 0.04045) * (var_G / 12.92))
    var_B = ((var_B > 0.04045) * ((var_B + 0.055) / 1.055) ** 2.4 + (var_B <= 0.04045) * (var_B / 12.92))

    var_R *= 100
    var_G *= 100
    var_B *= 100

    X = var_R * 0.4124564 + var_G * 0.3575761 + var_B * 0.1804375
    Y = var_R * 0.2126729 + var_G * 0.7151522 + var_B * 0.0721750
    Z = var_R * 0.0193339 + var_G * 0.1191920 + var_B * 0.9503041

    REF_X = 95.047
    REF_Y = 100.000
    REF_Z = 108.883

    var_X = X / REF_X
    var_Y = Y / REF_Y
    var_Z = Z / REF_Z

    var_X = (var_X ** (1/3) if var_X > 0.008856 else (7.787 * var_X) + (16 / 116))
    var_Y = (var_Y ** (1/3) if var_Y > 0.008856 else (7.787 * var_Y) + (16 / 116))
    var_Z = (var_Z ** (1/3) if var_Z > 0.008856 else (7.787 * var_Z) + (16 / 116))

    L_star = max(0, (116 * var_Y) - 16)
    a_star = round(500 * (var_X - var_Y))
    b_star = round(200 * (var_Y - var_Z))

    return L_star, a_star, b_star


def lab_to_rgb(l, a, b):
    REF_X, REF_Y, REF_Z = 95.047, 100.000, 108.883
    Y = (l + 16) / 116
    X, Z = Y + (a / 500), Y - (b / 200)
    X, Y, Z = REF_X * (X ** 3 if X ** 3 > 0.008856 else (X - 16 / 116) / 7.787), \
              REF_Y * (Y ** 3 if Y ** 3 > 0.008856 else (Y - 16 / 116) / 7.787), \
              REF_Z * (Z ** 3 if Z ** 3 > 0.008856 else (Z - 16 / 116) / 7.787)
    var_R, var_G, var_B = X * 0.032406 + Y * -0.015372 + Z * -0.004986, \
                          X * -0.009689 + Y * 0.018758 + Z * 0.000415, \
                          X * 0.000557 + Y * -0.002040 + Z * 0.010570
    R, G, B = int(max(0, min(255, var_R * 255))), int(max(0, min(255, var_G * 255))), int(max(0, min(255, var_B * 255)))
    return R, G, B

root = tk.Tk()
app = ColorConverterApp(root)
root.mainloop()
