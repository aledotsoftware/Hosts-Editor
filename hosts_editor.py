import tkinter as tk
from tkinter import messagebox
import os
import locale
import json
import subprocess
import sys
import ipaddress
import re
from datetime import datetime

HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"
LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")

# --- Cargar traducciones según el idioma del sistema ---
system_lang = locale.getdefaultlocale()[0]
lang_file = "es.json" if system_lang and system_lang.startswith("es") else "en.json"
with open(os.path.join(LOCALES_DIR, lang_file), "r", encoding="utf-8") as f:
    T = json.load(f)


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_domain(domain):
    # Regex básico: letras, números, guiones, puntos, y TLD de al menos 2 caracteres
    regex = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    return re.match(regex, domain) is not None


class HostsEditor:
    def __init__(self, master):
        self.master = master
        master.title(T["title"])

        self.listbox = tk.Listbox(master, width=80)
        self.listbox.pack(padx=10, pady=10)

        self.add_button = tk.Button(master, text=T["add"], command=self.add_entry)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(master, text=T["edit"], command=self.edit_entry)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(master, text=T["delete"], command=self.delete_entry)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(master, text=T["save"], command=self.save_hosts)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.load_hosts()

    def load_hosts(self):
        self.listbox.delete(0, tk.END)
        try:
            with open(HOSTS_FILE, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() and not line.startswith("#"):
                        self.listbox.insert(tk.END, line.strip())
        except PermissionError:
            messagebox.showerror("Error", T["error_read"])
        except FileNotFoundError:
            messagebox.showerror("Error", T["file_not_found"])

    def open_entry_form(self, title, ip="", domain="", callback=None):
        """ Un único formulario para IP y dominio """
        form = tk.Toplevel(self.master)
        form.title(title)
        form.geometry("350x200")
        form.resizable(False, False)

        tk.Label(form, text=T["add_ip"]).pack(pady=5)
        ip_entry = tk.Entry(form)
        ip_entry.insert(0, ip)
        ip_entry.pack()

        ip_warning = tk.Label(form, text="", fg="red")
        ip_warning.pack()

        tk.Label(form, text=T["add_domain"]).pack(pady=5)
        domain_entry = tk.Entry(form)
        domain_entry.insert(0, domain)
        domain_entry.pack()

        def validate_ip(*args):
            ip_val = ip_entry.get().strip()
            if ip_val and not is_valid_ip(ip_val):
                ip_warning.config(text=T.get("invalid_ip", "❌ IP inválida"))
            else:
                ip_warning.config(text="")

        ip_entry.bind("<KeyRelease>", validate_ip)

        def submit():
            ip_val = ip_entry.get().strip()
            domain_val = domain_entry.get().strip()

            if not is_valid_ip(ip_val):
                messagebox.showerror("Error", T.get("invalid_ip", "❌ IP inválida"))
                return
            if not is_valid_domain(domain_val):
                messagebox.showerror("Error", T.get("invalid_domain", "❌ Dominio inválido"))
                return

            if callback:
                callback(ip_val, domain_val)
            form.destroy()

        tk.Button(form, text=T["save"], command=submit).pack(pady=10)

    def add_entry(self):
        self.open_entry_form(T["add"], callback=lambda ip, domain: self.listbox.insert(tk.END, f"{ip} {domain}"))

    def edit_entry(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning(T["edit"], T["select_warning"])
            return
        line = self.listbox.get(selected[0])
        try:
            ip, domain = line.split()
        except ValueError:
            ip, domain = "", ""
        self.open_entry_form(
            T["edit"],
            ip,
            domain,
            callback=lambda new_ip, new_domain: self.update_entry(selected[0], new_ip, new_domain)
        )

    def update_entry(self, index, ip, domain):
        self.listbox.delete(index)
        self.listbox.insert(index, f"{ip} {domain}")

    def delete_entry(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning(T["delete"], T["select_warning"])
            return
        self.listbox.delete(selected[0])

    def save_hosts(self):
        # Crear backup con fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{HOSTS_FILE}.{timestamp}.bak"
        try:
            with open(HOSTS_FILE, "r") as f_in, open(backup_file, "w") as f_out:
                f_out.write(f_in.read())
        except Exception:
            pass  # Si no se puede leer, ignoramos

        temp_file = os.path.join(os.path.dirname(__file__), "hosts_temp.txt")
        with open(temp_file, "w") as f:
            for i in range(self.listbox.size()):
                f.write(self.listbox.get(i) + "\n")

        cmd = f'powershell -Command "Start-Process cmd -ArgumentList \'/c copy /Y \"{temp_file}\" \"{HOSTS_FILE}\"\' -Verb RunAs"'
        try:
            subprocess.run(cmd, shell=True, check=True)
            messagebox.showinfo("Info", T["success_save"])
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", T["error_write"])
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


if __name__ == "__main__":
    root = tk.Tk()
    app = HostsEditor(root)
    root.mainloop()
