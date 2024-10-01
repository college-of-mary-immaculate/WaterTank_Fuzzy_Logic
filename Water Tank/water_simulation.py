import tkinter as tk
from PIL import Image, ImageTk

class WaterTankSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Tank Simulation")

        self.canvas_width = 400
        self.canvas_height = 400
        self.tank_width = 200
        self.tank_height = 300
        self.faucet_size = 20
        self.water_level = 0
        self.is_filling = False
        self.is_draining = False
        self.droplets = []

       
        self.low_water_threshold = 20
        self.medium_water_threshold = 70
        self.high_water_threshold = 100

        self.low_water_logged = False
        self.refill_logged = False  
        self.tank_full_logged = False 

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.tank_x1 = (self.canvas_width - self.tank_width) // 2
        self.tank_x2 = self.tank_x1 + self.tank_width
        self.tank_y1 = self.canvas_height - self.tank_height
        self.tank_y2 = self.canvas_height
        self.tank = self.canvas.create_rectangle(self.tank_x1, self.tank_y1, self.tank_x2, self.tank_y2, outline="black", width=3)

        self.sensor_line_y = self.tank_y2 - (self.tank_height * 0.2)
        self.sensor_line = self.canvas.create_line(self.tank_x1, self.sensor_line_y, self.tank_x2, self.sensor_line_y, fill="gray", dash=(4, 2))

        self.load_tap_image()
        self.low_sensor = self.canvas.create_rectangle(self.tank_x1 - 20, self.tank_y2 - (self.tank_height * 0.33), self.tank_x1, self.tank_y2, fill="red", outline="black")
        self.medium_sensor = self.canvas.create_rectangle(self.tank_x1 - 20, self.tank_y2 - (self.tank_height * 0.67), self.tank_x1, self.tank_y2 - (self.tank_height * 0.33), fill="orange", outline="black")
        self.high_sensor = self.canvas.create_rectangle(self.tank_x1 - 20, self.tank_y1, self.tank_x1, self.tank_y2 - (self.tank_height * 0.67), fill="green", outline="black")

        self.canvas.create_text(self.tank_x1 - 65, self.tank_y1 + 5, text="High(100-80)", fill="green")
        self.canvas.create_text(self.tank_x1 - 65, self.tank_y1 + (self.tank_height * 0.5), text="Medium(80-30)", fill="orange")
        self.canvas.create_text(self.tank_x1 - 50, self.tank_y2 - 5, text="Low(20-0)", fill="red")

        self.faucet_button = tk.Button(self.root, text="Open/Close Faucet", command=self.toggle_faucet)
        self.faucet_button.pack(pady=5)

        self.psi_label = tk.Label(self.root, text="PSI: 0")
        self.psi_label.pack(pady=5)

        self.log_text = tk.Text(self.root, height=10, width=40)
        self.log_text.pack(pady=5)

        self.update_tank()
        self.update_droplets()

    def load_tap_image(self):
        
        image_path = "pusit.png" 

        tap_image = Image.open(image_path)
        tap_image = tap_image.resize((40, 40), Image.Resampling.LANCZOS)

        self.tap_image_tk = ImageTk.PhotoImage(tap_image)

        self.canvas.create_image(self.tank_x2 - 0, self.tank_y1 + self.tank_height // 2 - 20, image=self.tap_image_tk, anchor=tk.NW)

    def update_tank(self):
        self.canvas.delete("water")

        psi = self.calculate_psi_fuzzy(self.water_level)  
        self.psi_label.config(text=f"PSI: {psi:.1f}")

        if self.water_level < self.low_water_threshold:
            self.start_filling() 

        if self.water_level <= self.low_water_threshold:
            if not self.low_water_logged:
                
                self.log_message("Faucet closed, tank is refilling...")
                self.low_water_logged = True  
        else:
            self.low_water_logged = False  

        
        if self.water_level >= self.high_water_threshold and not self.tank_full_logged:
            self.log_message("Tank is full")  
            self.tank_full_logged = True  

        
        if self.water_level >= self.high_water_threshold:
            self.is_filling = False 

        if self.is_filling and self.water_level < 100:
            self.water_level += 0.7
        elif self.is_draining and self.water_level > 0:
            self.water_level -= 0.2  
            self.create_water_droplet()

        water_height = self.tank_height * (self.water_level / 100)
        water_y1 = self.tank_y2 - water_height

        self.canvas.create_rectangle(self.tank_x1, water_y1, self.tank_x2, self.tank_y2, fill="blue", tags="water")


        self.canvas.itemconfig(self.low_sensor, fill="red")
        self.canvas.itemconfig(self.medium_sensor, fill="orange")
        self.canvas.itemconfig(self.high_sensor, fill="green")


        self.root.after(200, self.update_tank)  

    def update_droplets(self):
        for droplet in self.droplets:
            self.canvas.move(droplet, 0, 2)  
            x1, y1, x2, y2 = self.canvas.coords(droplet)
            if y1 > self.canvas_height:  
                self.canvas.delete(droplet)
                self.droplets.remove(droplet)

        self.root.after(100, self.update_droplets)  

    def create_water_droplet(self):
        droplet_x = self.tank_x2 + 32  
        droplet_y = self.tank_y1 + self.tank_height // 2 + 10  
        droplet = self.canvas.create_oval(droplet_x, droplet_y, droplet_x + 5, droplet_y + 5, fill="blue", outline="blue", tags="droplet")
        self.droplets.append(droplet)

    def calculate_psi_fuzzy(self, water_level):

        if water_level <= 30:
            psi = water_level * 1.5  
        elif 30 < water_level <= 70:
            psi = (water_level - 30) * 2 + 45 
        else:
            psi = (water_level - 70) * 2.5 + 125  
        return psi

    def start_filling(self):
        self.is_filling = True
        self.is_draining = False

    def toggle_faucet(self):
        if self.is_draining:
            self.is_draining = False 
            self.log_message("Faucet closed.")
            self.low_water_logged = False  
        else:
            self.is_draining = True  
            self.is_filling = False  
            self.log_message("Faucet opened. Tank is draining...")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

root = tk.Tk()
app = WaterTankSimulation(root)
root.mainloop()
