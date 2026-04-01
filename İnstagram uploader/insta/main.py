from instagrapi import Client
import os
import json
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from functools import lru_cache
import time
import webbrowser

# --- MODERN RENK VE STİL AYARLARI ---
BG_COLOR = "#F8F9FA"         # Çok açık, ferah gri arka plan
FG_COLOR = "#262626"         # Koyu gri metin rengi
ACCENT_COLOR = "#0095F6"     # Instagram mavisi (Ana butonlar)
ACCENT_HOVER = "#1877F2"     # Hover (üzerine gelince) rengi
DANGER_COLOR = "#ED4956"     # Instagram kırmızısı (Çıkış butonu)
DANGER_HOVER = "#E03C49"     
SUCCESS_COLOR = "#28A745"    # Başarılı işlemi gösteren yeşil
FONT_MAIN = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")

# Oturum kayıt dizini
SESSION_DIR = os.path.join(tempfile.gettempdir(), "InstagramUploader_Marpace1")
os.makedirs(SESSION_DIR, exist_ok=True)

@lru_cache(maxsize=128)
def get_session_file(username):
    return os.path.join(SESSION_DIR, f"{username}.json")

def save_session(cl, username):
    with open(get_session_file(username), "w") as f:
        json.dump(cl.get_settings(), f)

def load_session(cl, username):
    session_file = get_session_file(username)
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            cl.set_settings(json.load(f))
        return True
    return False

# --- YARDIMCI ARAYÜZ FONKSİYONLARI ---
def center_window(win, width, height):
    """Pencereyi ekranın tam ortasında açar"""
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

def create_modern_button(parent, text, command, color, hover_color, width=15):
    """Hover efektli modern buton oluşturur"""
    btn = tk.Button(parent, text=text, command=command, bg=color, fg="white",
                    font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", width=width, pady=6)
    
    # Hover efektleri
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def prompt_for_password():
    dialog = tk.Toplevel(root)
    dialog.title("Şifre Gerekli")
    dialog.configure(bg=BG_COLOR)
    dialog.resizable(False, False)
    center_window(dialog, 320, 180)

    tk.Label(dialog, text=f"'{username}' için şifrenizi girin:", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).pack(pady=(20, 10))
    password_entry = ttk.Entry(dialog, show="*", width=30, font=FONT_MAIN)
    password_entry.pack(pady=5)
    password_entry.focus()

    password_var = tk.StringVar()
    def on_ok():
        password_var.set(password_entry.get().strip())
        dialog.destroy()

    btn = create_modern_button(dialog, "Onayla", on_ok, ACCENT_COLOR, ACCENT_HOVER)
    btn.pack(pady=15)
    
    dialog.grab_set()
    dialog.wait_window()
    return password_var.get()

def animate_loading(canvas, stop_flag, operation_type, total_files=1, current_file=1):
    angle = 0
    while not stop_flag():
        canvas.delete("loading")
        canvas.create_arc(10, 10, 50, 50, start=angle, extent=90, outline=ACCENT_COLOR, width=4, style=tk.ARC, tags="loading")
        canvas.create_text(30, 30, text=f"{current_file}/{total_files}" if total_files > 1 else "", fill=FG_COLOR, font=("Segoe UI", 8, "bold"), tags="loading")
        angle = (angle + 15) % 360
        root.update()
        time.sleep(0.03)
    
    canvas.delete("loading")
    canvas.create_text(30, 30, text="✔", fill=SUCCESS_COLOR, font=("Segoe UI", 20, "bold"))
    root.after(1500, lambda: canvas.delete("all"))

def check_existing_session(login_status_canvas, login_button):
    global cl, username
    session_files = [f for f in os.listdir(SESSION_DIR) if f.endswith(".json")]
    if not session_files:
        return False

    username = session_files[0].replace(".json", "")
    use_saved = messagebox.askyesno("Kayıtlı Oturum", f"'{username}' için kayıtlı bir oturum bulundu. Kullanılsın mı?")
    if not use_saved:
        return False

    cl = Client()
    try:
        load_session(cl, username)
        password = prompt_for_password()
        if not password:
            messagebox.showerror("Hata", "Oturumu yeniden kullanmak için şifre gereklidir.")
            return False

        login_status_canvas.pack(pady=5)
        login_button.config(state="disabled")
        stop_animation = False
        def stop_flag(): return stop_animation
        threading.Thread(target=animate_loading, args=(login_status_canvas, stop_flag, "login"), daemon=True).start()

        cl.login(username, password, relogin=True)
        stop_animation = True
        show_upload_frame()
        return True
    except Exception as e:
        stop_animation = True
        messagebox.showerror("Hata", f"Oturum açma başarısız oldu: {e}")
        os.remove(get_session_file(username))
        return False
    finally:
        login_button.config(state="normal")
        login_status_canvas.pack_forget()

def login():
    global cl, username
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if not username or not password:
        messagebox.showerror("Hata", "Lütfen kullanıcı adı ve şifrenizi girin.")
        return

    login_button.config(state="disabled")
    login_status_canvas.pack(pady=5)
    stop_animation = False
    def stop_flag(): return stop_animation
    threading.Thread(target=animate_loading, args=(login_status_canvas, stop_flag, "login"), daemon=True).start()

    def login_thread():
        global cl
        try:
            cl = Client()
            cl.login(username, password)
            save_session(cl, username)
            root.after(0, show_upload_frame)
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Giriş Başarısız", f"Hata: {e}"))
        finally:
            nonlocal stop_animation
            stop_animation = True
            root.after(0, lambda: login_status_canvas.pack_forget())
            root.after(0, lambda: login_button.config(state="normal"))

    threading.Thread(target=login_thread, daemon=True).start()

def logout():
    session_file = get_session_file(username)
    if os.path.exists(session_file):
        os.remove(session_file)
        messagebox.showinfo("Çıkış Yapıldı", "Başarıyla çıkış yapıldı ve oturum bilgileri silindi.")
        upload_frame.pack_forget()
        login_frame.pack(fill="both", expand=True)
    else:
        messagebox.showerror("Hata", "Kayıtlı bir oturum bulunamadı.")

def show_upload_frame():
    login_frame.pack_forget()
    upload_frame.pack(fill="both", expand=True, padx=25, pady=25)

def select_file(var, file_types, label):
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        var.set(file_path)
        label.config(text=os.path.basename(file_path)[:30] + "...", fg=ACCENT_COLOR)

def select_multiple_files(var, file_types, label):
    file_paths = filedialog.askopenfilenames(filetypes=file_types)
    if file_paths:
        var.set(list(file_paths) if file_paths else "")
        label.config(text=f"{len(file_paths)} dosya seçildi", fg=ACCENT_COLOR)

def upload():
    current_tab = notebook.tab(notebook.select(), "text")
    media_files = media_file_var.get()
    cover_file = cover_file_var.get() or None
    caption = caption_text_widget.get("1.0", tk.END).strip()
    tags = tags_entry_widget.get().strip()

    final_caption = caption
    if tags:
        final_caption = f"{caption}\n\n{tags}" if caption else tags

    if not media_files:
        messagebox.showerror("Hata", "Lütfen yüklenecek medya dosyasını seçin.")
        return

    if isinstance(media_files, str):
        if not os.path.exists(media_files):
            messagebox.showerror("Hata", "Seçilen dosya bulunamadı.")
            return
        media_files = [media_files]
    elif isinstance(media_files, (list, tuple)):
        if not all(os.path.exists(f) for f in media_files):
            messagebox.showerror("Hata", "Seçilen dosyalardan biri veya birkaçı bulunamadı.")
            return

    if "Reel" in current_tab and not all(f.lower().endswith(".mp4") for f in media_files):
        messagebox.showerror("Hata", "Reel sekmesinde sadece MP4 video formatı desteklenir.")
        return
    elif ("Hikaye" in current_tab or "Gönderi" in current_tab) and not all(f.lower().endswith((".jpg", ".png", ".mp4")) for f in media_files):
        messagebox.showerror("Hata", "Gönderi/Hikaye için desteklenen formatlar: JPG, PNG, MP4.")
        return

    status_canvas.pack(pady=5)
    upload_button.config(state="disabled")
    total_files = len(media_files)
    
    def upload_thread():
        current_file = 0
        stop_animation = False
        def stop_flag(): return stop_animation
        threading.Thread(target=animate_loading, args=(status_canvas, stop_flag, "upload", total_files, 1), daemon=True).start()

        def process_upload(file_list):
            nonlocal current_file
            for i, media_file in enumerate(file_list, 1):
                current_file = i
                root.after(0, lambda: status_canvas.delete("loading"))
                root.after(0, lambda: threading.Thread(target=animate_loading, args=(status_canvas, stop_flag, "upload", total_files, current_file), daemon=True).start())
                try:
                    if "Reel" in current_tab:
                        cl.clip_upload(media_file, caption=final_caption if final_caption else None, thumbnail=cover_file)
                    elif "Gönderi" in current_tab:
                        if media_file.lower().endswith(".mp4"):
                            cl.clip_upload(media_file, caption=final_caption if final_caption else None, thumbnail=cover_file)
                        else:
                            cl.photo_upload(media_file, caption=final_caption if final_caption else None)
                    elif "Hikaye" in current_tab:
                        if media_file.lower().endswith(".mp4"):
                            cl.clip_upload_to_story(media_file)
                        else:
                            cl.photo_upload_to_story(media_file)
                    time.sleep(2)
                except Exception as e:
                    root.after(0, lambda: messagebox.showerror("Yükleme Başarısız", f"{i}. dosya yüklenemedi:\n{e}"))
                    return False
            return True

        success = process_upload(media_files)
        stop_animation = True
        root.after(0, lambda: status_canvas.pack_forget())
        root.after(0, lambda: upload_button.config(state="normal"))
        if success:
            root.after(0, lambda: messagebox.showinfo("Başarılı", "Tüm dosyalar başarıyla Instagram'a yüklendi!"))

    threading.Thread(target=upload_thread, daemon=True).start()

def create_gui():
    global root, login_frame, upload_frame, username_entry, password_entry, login_status_canvas, login_button
    global notebook, media_file_var, cover_file_var, caption_text_widget, tags_entry_widget, upload_button, status_canvas

    root = tk.Tk()
    root.title("Instagram Yükleyici Pro")
    root.configure(bg=BG_COLOR)
    center_window(root, 650, 750) 

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass
    
    style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
    style.configure('TNotebook.Tab', padding=[25, 10], font=FONT_LABEL, background="#EAEAEA")
    style.map('TNotebook.Tab', background=[('selected', ACCENT_COLOR)], foreground=[('selected', 'white')])
    style.configure('TEntry', padding=6)

    # --- LOGIN FRAME ---
    login_frame = tk.Frame(root, bg=BG_COLOR)
    login_frame.pack(fill="both", expand=True, pady=100)

    tk.Label(login_frame, text="Instagram Yükleyici", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=(0, 5))
    
    # LINKEDIN BAĞLANTISI BURADA
    author_label = tk.Label(login_frame, text="by Tamer Yavuz (LinkedIn)", font=("Segoe UI", 10, "italic", "underline"), bg=BG_COLOR, fg=ACCENT_COLOR, cursor="hand2")
    author_label.pack(pady=(0, 40))
    author_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.linkedin.com/in/tamer-yavuz-73628084/"))
    
    entry_frame = tk.Frame(login_frame, bg=BG_COLOR)
    entry_frame.pack()

    tk.Label(entry_frame, text="Kullanıcı Adı", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).grid(row=0, column=0, sticky="w", pady=5)
    username_entry = ttk.Entry(entry_frame, width=35, font=FONT_MAIN)
    username_entry.grid(row=1, column=0, pady=(0, 15), ipady=3)

    tk.Label(entry_frame, text="Şifre", bg=BG_COLOR, fg=FG_COLOR, font=FONT_LABEL).grid(row=2, column=0, sticky="w", pady=5)
    password_entry = ttk.Entry(entry_frame, show="*", width=35, font=FONT_MAIN)
    password_entry.grid(row=3, column=0, pady=(0, 30), ipady=3)

    login_button = create_modern_button(login_frame, "Giriş Yap", login, ACCENT_COLOR, ACCENT_HOVER, width=30)
    login_button.pack()

    login_status_canvas = tk.Canvas(login_frame, width=60, height=60, bg=BG_COLOR, highlightthickness=0)
    root.after(0, lambda: check_existing_session(login_status_canvas, login_button))

    # --- UPLOAD FRAME ---
    upload_frame = tk.Frame(root, bg=BG_COLOR)
    
    header_frame = tk.Frame(upload_frame, bg=BG_COLOR)
    header_frame.pack(fill="x", pady=(0, 15))
    tk.Label(header_frame, text="Yönetim Paneli", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
    create_modern_button(header_frame, "Çıkış Yap", logout, DANGER_COLOR, DANGER_HOVER, width=12).pack(side="right")

    notebook = ttk.Notebook(upload_frame)
    notebook.pack(fill="x", pady=10)

    reel_tab = tk.Frame(notebook, bg="white", padx=20, pady=25)
    story_tab = tk.Frame(notebook, bg="white", padx=20, pady=25)
    post_tab = tk.Frame(notebook, bg="white", padx=20, pady=25)
    
    notebook.add(reel_tab, text="🎥 Reel")
    notebook.add(story_tab, text="⏱ Hikaye")
    notebook.add(post_tab, text="🖼 Gönderi")

    media_file_var = tk.StringVar()
    cover_file_var = tk.StringVar()

    def build_tab_content(tab, is_story=False):
        tk.Label(tab, text="Medya Dosyası:", bg="white", font=FONT_LABEL).grid(row=0, column=0, pady=10, sticky="w")
        media_label = tk.Label(tab, text="Dosya seçilmedi", bg="white", fg="#8e8e8e", font=FONT_MAIN)
        media_label.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        btn_frame = tk.Frame(tab, bg="white")
        btn_frame.grid(row=0, column=2, sticky="e")
        
        create_modern_button(btn_frame, "Dosya Seç", lambda: select_file(media_file_var, [("Medya", "*.mp4;*.jpg;*.png")], media_label), "#6C757D", "#5A6268", 10).pack(side="left", padx=5)
        if not is_story:
            create_modern_button(btn_frame, "Çoklu Seç", lambda: select_multiple_files(media_file_var, [("Medya", "*.mp4;*.jpg;*.png")], media_label), "#6C757D", "#5A6268", 12).pack(side="left")

        if not is_story:
            tk.Label(tab, text="Kapak Görseli:", bg="white", font=FONT_LABEL).grid(row=1, column=0, pady=15, sticky="w")
            cover_label = tk.Label(tab, text="İsteğe bağlı", bg="white", fg="#8e8e8e", font=FONT_MAIN)
            cover_label.grid(row=1, column=1, padx=15, pady=15, sticky="w")
            create_modern_button(tab, "Kapak Seç", lambda: select_file(cover_file_var, [("Görsel", "*.jpg;*.png")], cover_label), "#6C757D", "#5A6268", 10).grid(row=1, column=2, sticky="w", padx=5)

    build_tab_content(reel_tab)
    build_tab_content(story_tab, is_story=True)
    build_tab_content(post_tab)

    # --- METİN VE ETİKET KUTULARI ---
    caption_frame = tk.Frame(upload_frame, bg=BG_COLOR)
    caption_frame.pack(fill="both", expand=True, pady=(15, 5))
    
    tk.Label(caption_frame, text="Açıklama (Hikayeler için geçersizdir):", font=FONT_LABEL, bg=BG_COLOR).pack(anchor="w")
    caption_text_widget = tk.Text(caption_frame, height=4, font=FONT_MAIN, relief="flat", highlightthickness=1, highlightbackground="#CED4DA", highlightcolor=ACCENT_COLOR)
    caption_text_widget.pack(fill="both", expand=True, pady=(5, 15))

    tk.Label(caption_frame, text="Etiketler (Örn: #yazılım #python #kodlama):", font=FONT_LABEL, bg=BG_COLOR).pack(anchor="w")
    tags_entry_widget = ttk.Entry(caption_frame, font=FONT_MAIN)
    tags_entry_widget.pack(fill="x", pady=(5, 5), ipady=4)

    # --- YÜKLEME BUTONU ---
    bottom_frame = tk.Frame(upload_frame, bg=BG_COLOR)
    bottom_frame.pack(fill="x")
    
    upload_button = create_modern_button(bottom_frame, "🚀 Yüklemeyi Başlat", upload, ACCENT_COLOR, ACCENT_HOVER, width=25)
    upload_button.pack(pady=15)
    
    status_canvas = tk.Canvas(bottom_frame, width=60, height=60, bg=BG_COLOR, highlightthickness=0)

    root.mainloop()

if __name__ == "__main__":
    create_gui()