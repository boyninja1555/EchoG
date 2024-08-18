from http_handler import send_http_request
from html_parser import parse_html
import sys
import os
import tkinter as tk
import webbrowser
import config

window = ""
url_bar_entry = ""
viewer_frame = ""
plaintext_viewer_text = ""

def resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)

def main():
    if len(sys.argv) > 1:
        open_browser_window(
            send_http_request(config.PROTOCOL, sys.argv[1], None)["body"]
        )
    else:
        open_browser_window(
            send_http_request(config.PROTOCOL, config.HOME_PAGE, None)["body"]
        )

def open_url(url: str):
    if url.startswith("http://") or url.startswith("https://"):
        webbrowser.open(url)
    elif url.startswith(f"{config.PROTOCOL}://"):
        url_parts = url.split(f"{config.PROTOCOL}://")[1].split("/")
        url_bar_entry.delete(0, len(url_bar_entry.get()))
        url_bar_entry.insert(0, url.split(f"{config.PROTOCOL}://")[1])

        if len(url_parts) == 1:
            open_page(
                "text/html",
                send_http_request(config.PROTOCOL, url_parts[0], None)["body"],
            )
        elif len(url_parts) == 2:
            open_page(
                "text/html",
                send_http_request(config.PROTOCOL, url_parts[0], url_parts[1])["body"],
            )

def open_browser_window(page_contents: str):
    global window
    global url_bar_entry
    global viewer_frame
    global plaintext_viewer_text

    window = tk.Tk()
    window.title(config.NAME)
    window.iconphoto(
        False, tk.PhotoImage(file=resource_path(os.path.join("res", "icon.png")))
    )
    window.geometry("850x478")
    window.state("zoomed")
    window.configure(background=config.BACKGROUND_PRIMARY)

    url_bar_frame = tk.Frame(window, background=config.BACKGROUND_SECONDARY)
    url_bar_frame.pack(fill=tk.X)

    back_btn = tk.Button(
        url_bar_frame,
        text="<",
        background=config.BACKGROUND_TERTIARY,
        foreground=config.FOREGROUND_SECONDARY,
        borderwidth=0,
        font=(config.DEFAULT_FONT, 10),
        command=lambda: open_url(url_bar_entry.get())
    )
    back_btn.pack(side=tk.LEFT, padx=5, pady=5)

    home_btn = tk.Button(
        url_bar_frame,
        text="H",
        background=config.BACKGROUND_TERTIARY,
        foreground=config.FOREGROUND_SECONDARY,
        borderwidth=0,
        font=(config.DEFAULT_FONT, 10),
        command=lambda: open_url(f"echog://{config.HOME_PAGE}")
    )
    home_btn.pack(side=tk.LEFT, padx=5, pady=5)

    url_bar_entry = tk.Entry(
        url_bar_frame,
        background=config.BACKGROUND_SECONDARY,
        foreground=config.FOREGROUND_PRIMARY,
        borderwidth=0,
        insertbackground=config.FOREGROUND_PRIMARY,
        font=(config.DEFAULT_FONT, 14)
    )
    url_bar_entry.pack(fill=tk.X, padx=5, pady=5, expand=True)
    url_bar_entry.bind(
        "<Return>",
        lambda event: open_page(
            "text/html",
            send_http_request(config.PROTOCOL, url_bar_entry.get(), None)["body"],
        ),
    )
    url_bar_entry.focus()
    url_bar_entry.insert(0, config.HOME_PAGE)

    viewer_frame = tk.Frame(window, background=config.BACKGROUND_PRIMARY)
    viewer_frame.pack(fill=tk.BOTH, expand=True)

    open_page("text/html", page_contents)

    window.mainloop()

def open_page(mime_type: str, page_contents: str):
    global window
    global url_bar_entry
    global viewer_frame
    global plaintext_viewer_text

    for widget in viewer_frame.winfo_children():
        widget.destroy()

    if mime_type == "text/plain":
        if plaintext_viewer_text:
            plaintext_viewer_text.config(state=tk.NORMAL)
            plaintext_viewer_text.delete(1.0, tk.END)
        else:
            plaintext_viewer_text = tk.Text(
                viewer_frame,
                background=config.BACKGROUND_PRIMARY,
                foreground=config.FOREGROUND_PRIMARY,
                font=(config.DEFAULT_FONT, 16),
            )
            plaintext_viewer_text.pack(fill=tk.BOTH, expand=True)
        
        plaintext_viewer_text.insert(tk.END, page_contents)
        plaintext_viewer_text.config(state=tk.DISABLED)
        plaintext_viewer_text.focus()

        window.title(f"{url_bar_entry.get()} - {config.NAME}")
    elif mime_type == "text/html":
        if plaintext_viewer_text:
            plaintext_viewer_text.destroy()
            plaintext_viewer_text = None

        html_viewer = tk.Frame(viewer_frame, background=config.BACKGROUND_PRIMARY)
        html_viewer.pack(fill=tk.BOTH, expand=True)
        html_viewer.focus()

        window.title(
            f"{page_contents.split('<title>')[1].split('</title>')[0]} - {config.NAME}"
        )

        body = page_contents.split("<body>")[1].split("</body>")[0]

        parse_html(tk, window, html_viewer, body, open_url)
    else:
        if plaintext_viewer_text:
            plaintext_viewer_text.config(state=tk.NORMAL)
            plaintext_viewer_text.delete(1.0, tk.END)
        else:
            plaintext_viewer_text = tk.Text(
                viewer_frame,
                background=config.BACKGROUND_PRIMARY,
                foreground=config.FOREGROUND_PRIMARY,
                font=(config.DEFAULT_FONT, 16),
            )
            plaintext_viewer_text.pack(fill=tk.BOTH, expand=True)
        
        plaintext_viewer_text.insert(tk.END, page_contents)
        plaintext_viewer_text.config(state=tk.DISABLED)
        plaintext_viewer_text.focus()

if __name__ == "__main__":
    main()
