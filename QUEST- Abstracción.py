import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class EvaluadorCredito(ABC):
    @abstractmethod
    def calcular_puntaje(self):
        pass

class Persona(EvaluadorCredito):
    def __init__(self, tarjetas_otras_frans, sin_riesgo, trabajo_definido, trabajo_indefinido,
                 credito_otra_banca, credito_misma_banca, edad):
        self.tarjetas_otras_frans = tarjetas_otras_frans
        self.sin_riesgo = sin_riesgo
        self.trabajo_definido = trabajo_definido
        self.trabajo_indefinido = trabajo_indefinido
        self.credito_otra_banca = credito_otra_banca
        self.credito_misma_banca = credito_misma_banca
        self.edad = edad

    def calcular_puntaje(self):
        puntos = 0

        if self.tarjetas_otras_frans and self.edad >= 18:
            puntos += 1

        if self.sin_riesgo:
            puntos += 3

        if self.trabajo_definido:
            puntos += 2

        if self.trabajo_indefinido:
            puntos += 3

        if self.credito_otra_banca:
            puntos += 2

        if self.credito_misma_banca:
            puntos += 3

        if 18 <= self.edad <= 22:
            puntos += 2
        elif 23 <= self.edad <= 30:
            puntos += 4
        elif 31 <= self.edad <= 40:
            puntos += 3
        elif self.edad > 41:
            puntos += 1

        return puntos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluador de Crédito")
        self.aprobados = 0
        self.total_personas = 0

        tk.Label(root, text="Edad:").grid(row=0, column=0, sticky="e")
        self.edad_entry = tk.Entry(root)
        self.edad_entry.grid(row=0, column=1)

        self.tarjeta_var = tk.IntVar()
        tk.Checkbutton(root, text="¿Posee tarjetas con otras franquicias?", variable=self.tarjeta_var).grid(row=1, columnspan=2, sticky="w")

        self.riesgo_var = tk.IntVar()
        tk.Checkbutton(root, text="¿No está reportado ante entidades de riesgo?", variable=self.riesgo_var).grid(row=2, columnspan=2, sticky="w")

        self.definido_var = tk.IntVar()
        tk.Checkbutton(root, text="¿Trabaja a término definido?", variable=self.definido_var).grid(row=3, columnspan=2, sticky="w")

        self.indefinido_var = tk.IntVar()
        tk.Checkbutton(root, text="¿Trabaja a término indefinido?", variable=self.indefinido_var).grid(row=4, columnspan=2, sticky="w")

        self.credito_otra_var = tk.IntVar()
        tk.Checkbutton(root, text="¿Obtuvo créditos en otra entidad bancaria?", variable=self.credito_otra_var).grid(row=5, columnspan=2, sticky="w")

        self.credito_misma_var = tk.IntVar()
        tk.Checkbutton(root, text="¿Obtuvo créditos en la misma entidad bancaria?", variable=self.credito_misma_var).grid(row=6, columnspan=2, sticky="w")


        tk.Button(root, text="Calcular Puntaje", command=self.calcular_credito).grid(row=7, columnspan=2, pady=10)


        self.resultado_label = tk.Label(root, text="Total de aprobados: 0")
        self.resultado_label.grid(row=8, columnspan=2)

    def calcular_credito(self):
        try:
            edad = int(self.edad_entry.get())

            if edad < 18:
                tarjeta = False
                messagebox.showinfo("Aviso", "La persona es menor de 18 años, no puede tener tarjeta de crédito.")
            else:
                tarjeta = bool(self.tarjeta_var.get())

            persona = Persona(
                tarjetas_otras_frans=tarjeta,
                sin_riesgo=bool(self.riesgo_var.get()),
                trabajo_definido=bool(self.definido_var.get()),
                trabajo_indefinido=bool(self.indefinido_var.get()),
                credito_otra_banca=bool(self.credito_otra_var.get()),
                credito_misma_banca=bool(self.credito_misma_var.get()),
                edad=edad
            )

            puntaje = persona.calcular_puntaje()
            self.total_personas += 1

            if puntaje >= 6:
                self.aprobados += 1
                messagebox.showinfo("Resultado", f"Puntaje: {puntaje}\nCrédito aprobado.")
            else:
                messagebox.showinfo("Resultado", f"Puntaje: {puntaje}\nCrédito no aprobado.")

            self.resultado_label.config(text=f"Total de aprobados: {self.aprobados} de {self.total_personas}")

            self.limpiar_campos()

        except ValueError:
            messagebox.showerror("Error", "Ingrese una edad válida (número).")

    def limpiar_campos(self):
        self.edad_entry.delete(0, tk.END)
        self.tarjeta_var.set(0)
        self.riesgo_var.set(0)
        self.definido_var.set(0)
        self.indefinido_var.set(0)
        self.credito_otra_var.set(0)
        self.credito_misma_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
