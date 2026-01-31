import tkinter as tk
from tkinter import ttk


def labeled_scale(parent, label_text, from_, to, variable, **kwargs):
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label_text).pack(anchor='w')
    scale = ttk.Scale(frame, from_=from_, to=to, variable=variable, **kwargs)
    scale.pack(fill='x')
    return frame, scale


def simple_button(parent, text, command, **kwargs):
    btn = ttk.Button(parent, text=text, command=command, **kwargs)
    return btn
