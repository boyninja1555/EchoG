
def parse_html(tk, window, html_viewer, lines, open_url):
    for line in lines:
            line = line.strip()
            
            if line.startswith("<p>"):
                text = line.replace("<p>", "").replace("</p>", "")
                label = tk.Label(html_viewer, text=text, background="#222222", foreground="#cccccc", font=("Consolas", 16))
                label.pack(anchor="w", padx=10, pady=5)
            elif line.startswith("<h1>"):
                text = line.replace("<h1>", "").replace("</h1>", "")
                label = tk.Label(html_viewer, text=text, background="#222222", foreground="#cccccc", font=("Consolas", 32, "bold"))
                label.pack(anchor="w", padx=10, pady=10)
            elif line.startswith("<h2>"):
                text = line.replace("<h2>", "").replace("</h2>", "")
                label = tk.Label(html_viewer, text=text, background="#222222", foreground="#cccccc", font=("Consolas", 24, "bold"))
                label.pack(anchor="w", padx=10, pady=10)
            elif line.startswith("<a href="):
                href = line.split('"')[1]
                text = line.split("\">")[1].split("</a>")[0]
                link = tk.Label(html_viewer, text=text, background="#222222", foreground="blue", font=("Consolas", 16), cursor="hand2")
                link.pack(anchor="w", padx=10, pady=5)
                link.bind("<Button-1>", lambda event, href=href: open_url(href))
            elif line.startswith("<hr />"):
                line_height = 1
                line = tk.Label(html_viewer, text="", background="#cccccc", font=("Consolas", 1), width=int(window.winfo_screenwidth()), height=line_height)
                line.pack(anchor="w", padx=10, pady=5)
            elif line.startswith("<pyscript>"):
                code = line.replace("<pyscript>", "").replace("</pyscript>", "")
                label = tk.Label(html_viewer, text=f"Python Script:\n{code}", background="#222222", foreground="#cccccc", font=("Consolas", 16))
                label.pack(anchor="w", padx=10, pady=5)
