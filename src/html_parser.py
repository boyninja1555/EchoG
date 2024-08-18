import config
import html
import http.client
from bs4 import BeautifulSoup
from lupa import LuaRuntime

tags = []

def get_by_id(id):
    for tag in tags:
        if tag["id"] == id:
            return tag["label"]
        
    return None

def fetch_from_url(url, subpath):
    client = http.client.HTTPSConnection(url)
    client.request("GET", f"/{subpath or ""}")
    response = client.getresponse()
    return response

def log(msg):
    print(msg)

def update_element(id, property_name, value):
    element = get_by_id(id)
    
    if element:
        if property_name == "text":
            element.config(text=value)

def execute_lua_script(script):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        function getById(id)
            return _G.get_by_id(id)
        end
        
        function fetchFromURL(url, subpath)
            return _G.fetch_from_url(url, subpath)
        end
                
        function log(msg)
            return _G.log(msg)
        end

        function setText(id, value)
            _G.update_element(id, "text", value)
        end
    ''')
    lua.globals().get_by_id = get_by_id
    lua.globals().fetch_from_url = fetch_from_url
    lua.globals().log = log
    lua.globals().update_element = update_element

    try:
        lua.execute(script)
    except Exception as e:
        print(f"Error executing Lua script: {e}")

def parse_html(tk, window, html_viewer, html_content, open_url):
    soup = BeautifulSoup(html_content, "html.parser")
    
    for element in soup:
        if element.name == "p":
            text = element.get_text()
            label = tk.Label(
                html_viewer,
                text=text,
                background=config.BACKGROUND_PRIMARY,
                foreground=config.FOREGROUND_PRIMARY,
                font=(config.DEFAULT_FONT, 16),
            )
            label.pack(anchor="w", padx=10, pady=5)
            tags.append({
                "id": element.get("id", None),
                "label": label
            })
        elif element.name == "h1":
            text = element.get_text()
            label = tk.Label(
                html_viewer,
                text=text,
                background=config.BACKGROUND_PRIMARY,
                foreground=config.FOREGROUND_PRIMARY,
                font=(config.DEFAULT_FONT, 32, "bold"),
            )
            label.pack(anchor="w", padx=10, pady=10)
            tags.append({
                "id": element.get("id", None),
                "label": label
            })
        elif element.name == "h2":
            text = element.get_text()
            label = tk.Label(
                html_viewer,
                text=text,
                background=config.BACKGROUND_PRIMARY,
                foreground=config.FOREGROUND_PRIMARY,
                font=(config.DEFAULT_FONT, 24, "bold"),
            )
            label.pack(anchor="w", padx=10, pady=10)
            tags.append({
                "id": element.get("id", None),
                "label": label
            })
        elif element.name == "a":
            href = element.get("href", "#")
            text = element.get_text()
            link = tk.Label(
                html_viewer,
                text=text,
                background=config.BACKGROUND_PRIMARY,
                foreground="blue",
                font=(config.DEFAULT_FONT, 16),
                cursor="hand2",
            )
            link.pack(anchor="w", padx=10, pady=5)
            link.bind("<Button-1>", lambda event, href=href: open_url(href))
            tags.append({
                "id": element.get("id", None),
                "label": link
            })
        elif element.name == "hr":
            line_height = 1
            line = tk.Label(
                html_viewer,
                text="",
                background=config.FOREGROUND_SECONDARY,
                font=(config.DEFAULT_FONT, 1),
                width=int(window.winfo_screenwidth()),
                height=line_height,
            )
            line.pack(anchor="w", padx=10, pady=5)
            tags.append({
                "id": element.get("id", None),
                "label": line
            })
        elif element.name == "lua":
            code = element.get_text()
            
            execute_lua_script(code)
        elif element.name == "pre":
            text = element.get_text()
            escaped_text = html.escape(text)
            label = tk.Label(
                html_viewer,
                text=escaped_text,
                background=config.BACKGROUND_PRIMARY,
                foreground=config.FOREGROUND_PRIMARY,
                font=(config.DEFAULT_FONT, 16),
                wraplength=window.winfo_screenwidth() - 20,
                justify="left"
            )
            label.pack(anchor="w", padx=10, pady=5)
            tags.append({
                "id": element.get("id", None),
                "label": label
            })
