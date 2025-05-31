import tkinter as tk
from tkinter import messagebox
import requests
import folium
import webbrowser
import os

# --- Dark Mode Colors ---
BG_COLOR = "#23272e"
FG_COLOR = "#f5f6fa"
ENTRY_BG = "#2d323b"
ENTRY_FG = "#f5f6fa"
BTN_BG = "#3a3f4b"
BTN_FG = "#f5f6fa"
HIGHLIGHT = "#7289da"

# --- Placeholder Handling ---
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self['fg'] = self.placeholder_color
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

    def foc_in(self, *args):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self['fg'] = ENTRY_FG

    def foc_out(self, *args):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def get_value(self):
        value = self.get()
        if value == self.placeholder:
            return ""
        return value

def get_location():
    try:
        response = requests.get('http://ip-api.com/json/').json()
        if response['status'] != 'success':
            raise Exception("IP Geolocation failed.")
        display_location_info(response, "Your IP Location")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def use_custom_coordinates():
    try:
        lat = lat_entry.get_value()
        lon = lon_entry.get_value()
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("Latitude must be -90 to 90 and longitude -180 to 180.")
        output_label.config(text=f"Custom Location:\nLatitude: {lat}\nLongitude: {lon}")
        show_map(lat, lon, "Custom Coordinates")
    except ValueError as ve:
        messagebox.showerror("Invalid Input", f"{ve}")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")

def locate_ip_address():
    try:
        ip = ip_entry.get_value().strip()
        if ip == "":
            raise ValueError("Please enter an IP address.")
        response = requests.get(f'http://ip-api.com/json/{ip}').json()
        if response['status'] != 'success':
            raise Exception("Invalid or unreachable IP address.")
        display_location_info(response, f"Location for IP: {ip}")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")

def display_location_info(response, title):
    city = response.get("city", "Unknown")
    region = response.get("regionName", "Unknown")
    country = response.get("country", "Unknown")
    lat = response.get("lat")
    lon = response.get("lon")
    if lat is None or lon is None:
        raise ValueError("Latitude or Longitude not found.")
    location_text = f"{title}\nCity: {city}\nRegion: {region}\nCountry: {country}\nLatitude: {lat}\nLongitude: {lon}"
    output_label.config(text=location_text)
    show_map(lat, lon, city)

def show_map(lat, lon, popup="Location"):
    # Show map using folium
    map = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon], popup=popup).add_to(map)
    map_file = "map.html"
    map.save(map_file)
    webbrowser.open('file://' + os.path.realpath(map_file))

    # Open Google Earth at the location
    google_earth_url = f"https://earth.google.com/web/@{lat},{lon},1000a"
    webbrowser.open(google_earth_url)

# --- GUI Setup ---
root = tk.Tk()
root.title("📍 Geolocator")
root.geometry("450x520")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

def style_widget(widget):
    widget.configure(bg=BG_COLOR, fg=FG_COLOR)

header = tk.Label(root, text="📍 Geolocator", font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=HIGHLIGHT)
header.pack(pady=10)

btn1 = tk.Button(root, text="Get My Location (Your IP)", font=("Helvetica", 12), command=get_location,
                 bg=BTN_BG, fg=BTN_FG, activebackground=HIGHLIGHT, activeforeground=FG_COLOR, bd=0)
btn1.pack(pady=10)

lbl1 = tk.Label(root, text="OR Enter Custom Coordinates", font=("Helvetica", 11), bg=BG_COLOR, fg=FG_COLOR)
lbl1.pack(pady=5)

lat_entry = PlaceholderEntry(root, placeholder="Enter Latitude", color="grey",
                            font=("Helvetica", 10), width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, bd=1, relief="flat")
lat_entry.pack(pady=3)

lon_entry = PlaceholderEntry(root, placeholder="Enter Longitude", color="grey",
                            font=("Helvetica", 10), width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, bd=1, relief="flat")
lon_entry.pack(pady=3)

btn2 = tk.Button(root, text="Show Custom Location", font=("Helvetica", 11), command=use_custom_coordinates,
                 bg=BTN_BG, fg=BTN_FG, activebackground=HIGHLIGHT, activeforeground=FG_COLOR, bd=0)
btn2.pack(pady=10)

lbl2 = tk.Label(root, text="OR Enter an IP Address", font=("Helvetica", 11), bg=BG_COLOR, fg=FG_COLOR)
lbl2.pack(pady=5)

ip_entry = PlaceholderEntry(root, placeholder="Enter IP Address", color="grey",
                           font=("Helvetica", 10), width=30, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR, bd=1, relief="flat")
ip_entry.pack(pady=3)

btn3 = tk.Button(root, text="Find Location of IP", font=("Helvetica", 11), command=locate_ip_address,
                 bg=BTN_BG, fg=BTN_FG, activebackground=HIGHLIGHT, activeforeground=FG_COLOR, bd=0)
btn3.pack(pady=10)

output_label = tk.Label(root, text="", font=("Helvetica", 10), justify="left", bg=BG_COLOR, fg=FG_COLOR, wraplength=400)
output_label.pack(pady=15)

root.mainloop()

# --- End of locator.py ---
