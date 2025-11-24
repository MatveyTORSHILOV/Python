
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os

AUTHOR_FIO = "Торшилов Матвей Алексеевич"
AUTHOR_GROUP = "УБ-52"


GITHUB_API_BASE_URL = "https://api.github.com"
OUTPUT_FILENAME = f"{AUTHOR_FIO.replace(' ', '_')}_{AUTHOR_GROUP}_github_results.json"

DEFAULT_REPO_FOR_VARIANT_7 = "vuejs/vue"

root = None
repo_name_entry = None
status_text_widget = None

def log_message(message, level="info"):
    global status_text_widget
    if status_text_widget:
        status_text_widget.insert(tk.END, message + "\n")
        status_text_widget.see(tk.END)
        if level == "error":
            print(f"ERROR: {message}")
        else:
            print(message)


def fetch_repo_data():
    global repo_name_entry, status_text_widget

    repo_full_name = repo_name_entry.get().strip()
    log_message(f"Запрос данных для репозитория: {repo_full_name}")

    if not repo_full_name:
        messagebox.showerror("Ошибка ввода", "Введите имя репозитория (например, 'owner/repo_name').")
        log_message("Ошибка: Имя репозитория не введено.", "error")
        return

    if '/' not in repo_full_name:
        messagebox.showerror("Ошибка ввода", "Некорректный формат имени репозитория. Используйте 'owner/repo_name'.")
        log_message("Ошибка: Некорректный формат имени репозитория.", "error")
        return

    owner, repo = repo_full_name.split('/', 1)

    repo_url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}"
    log_message(f"API запрос к: {repo_url}")
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        repo_data = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка API", f"Не удалось получить данные репозитория: {e}")
        log_message(f"Ошибка при запросе репозитория: {e}", "error")
        log_message("Возможно, репозиторий не существует, проблемы с сетью или превышен лимит запросов GitHub API (60 запросов в час для неаутентифицированных).", "error")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка API", "Не удалось декодировать JSON ответ от GitHub (репозиторий).")
        log_message("Ошибка: Не удалось декодировать JSON (репозиторий).", "error")
        return

    if 'owner' not in repo_data or 'url' not in repo_data['owner']:
        messagebox.showerror("Ошибка данных", "Не удалось найти информацию о владельце репозитория.")
        log_message("Ошибка: Не найдена информация о владельце в данных репозитория.", "error")
        return
    
    owner_api_url = repo_data['owner']['url']
    log_message(f"API запрос к данным владельца: {owner_api_url}")


    try:
        response = requests.get(owner_api_url)
        response.raise_for_status()
        owner_data = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка API", f"Не удалось получить данные владельца: {e}")
        log_message(f"Ошибка при запросе владельца: {e}", "error")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка API", "Не удалось декодировать JSON ответ от GitHub (владелец).")
        log_message("Ошибка: Не удалось декодировать JSON (владелец).", "error")
        return

    extracted_data = {
        'company': owner_data.get('company', None),
        'created_at': owner_data.get('created_at', None),
        'email': owner_data.get('email', None),
        'id': owner_data.get('id', None),
        'name': owner_data.get('name', None),
        'url': owner_data.get('url', None)
    }

    extracted_data['repo_name_requested'] = repo_full_name

    log_message(f"Получены данные: {json.dumps(extracted_data, indent=2, ensure_ascii=False)}")

    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Успех", f"Данные успешно записаны в файл:\n{os.path.abspath(OUTPUT_FILENAME)}")
        log_message(f"Данные успешно записаны в файл: {OUTPUT_FILENAME}")
    except IOError as e:
        messagebox.showerror("Ошибка файла", f"Не удалось записать данные в файл {OUTPUT_FILENAME}: {e}")
        log_message(f"Ошибка при записи в файл: {e}", "error")
    except Exception as e:
        messagebox.showerror("Неизвестная ошибка", f"Произошла непредвиденная ошибка: {e}")
        log_message(f"Неизвестная ошибка: {e}", "error")

def create_gui():
    global root, repo_name_entry, status_text_widget

    root = tk.Tk()
    root.title(AUTHOR_FIO)
    root.geometry("700x500")
    root.resizable(True, True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    ttk.Label(root, text="Введите имя репозитория на GitHub (например, 'owner/repo_name'):", font=('Arial', 10, 'bold')) \
        .grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ttk.Label(root, text=f"Для варианта 7 (по последней цифре зачетки) используйте: {DEFAULT_REPO_FOR_VARIANT_7}", font=('Arial', 9)) \
        .grid(row=1, column=0, padx=10, pady=2, sticky="w")
    input_frame = ttk.Frame(root)
    input_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    input_frame.columnconfigure(0, weight=1)

    repo_name_entry = ttk.Entry(input_frame, width=50)
    repo_name_entry.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
    repo_name_entry.insert(0, DEFAULT_REPO_FOR_VARIANT_7)

    fetch_button = ttk.Button(input_frame, text="Получить данные", command=fetch_repo_data)
    fetch_button.grid(row=0, column=1, padx=5, pady=0, sticky="e")
    ttk.Label(root, text="Логи выполнения:", font=('Arial', 10, 'bold')) \
        .grid(row=3, column=0, padx=10, pady=5, sticky="w")
    
    status_text_widget = tk.Text(root, wrap="word", height=15, width=80)
    status_text_widget.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

    scrollbar = ttk.Scrollbar(root, command=status_text_widget.yview)
    scrollbar.grid(row=4, column=1, sticky="ns")
    status_text_widget.config(yscrollcommand=scrollbar.set)
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Файл", menu=file_menu)
    file_menu.add_command(label="Выход", command=root.quit)

    log_message(f"Приложение запущено. Ожидается ввод репозитория. Результаты будут сохранены в: {OUTPUT_FILENAME}")
    log_message("Учтите лимиты GitHub API: неаутентифицированные запросы ограничены (обычно 60 запросов в час).")

if __name__ == "__main__":
    create_gui()
    root.mainloop()
