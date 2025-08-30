import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw
import torch
from torchvision import transforms
from torchvision import models
import os
from tkinter import font as tkFont


# -------------------------
# Load your trained model
# -------------------------
model = models.resnet50(weights=None)
num_classes = 120
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

checkpoint_path = r"D:\[ 0 ]\pawtector_model.pth"
state_dict = torch.load(checkpoint_path, map_location=torch.device('cpu'))
model.load_state_dict(state_dict, strict=False)
model.eval()

# Preprocessing pipeline
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Dog breed classes
class_names = [
    "affenpinscher", "afghan_hound", "african_hunting_dog", "airedale", "american_staffordshire_terrier",
    "appenzeller", "australian_terrier", "basenji", "basset", "beagle", "bedlington_terrier",
    "bernese_mountain_dog", "black-and-tan_coonhound", "blenheim_spaniel", "bloodhound", "bluetick",
    "border_collie", "border_terrier", "borzoi", "boston_bull", "bouvier_des_flandres", "boxer",
    "brabancon_griffon", "briard", "brittany_spaniel", "bull_mastiff", "cairn", "cardigan",
    "chesapeake_bay_retriever", "chihuahua", "chow", "clumber", "cocker_spaniel", "collie",
    "curly-coated_retriever", "dandie_dinmont", "dhole", "dingo", "doberman", "english_foxhound",
    "english_setter", "english_springer", "entlebucher", "eskimo_dog", "flat-coated_retriever",
    "french_bulldog", "german_shepherd", "german_short-haired_pointer", "giant_schnauzer",
    "golden_retriever", "gordon_setter", "great_dane", "great_pyrenees", "greater_swiss_mountain_dog",
    "groenendael", "ibizan_hound", "irish_setter", "irish_terrier", "irish_water_spaniel",
    "irish_wolfhound", "italian_greyhound", "japanese_spaniel", "keeshond", "kelpie",
    "kerry_blue_terrier", "komondor", "kuvasz", "labrador_retriever", "lakeland_terrier", "leonberg",
    "lhasa", "malamute", "malinois", "maltese_dog", "mexican_hairless", "miniature_pinscher",
    "miniature_poodle", "miniature_schnauzer", "newfoundland", "norfolk_terrier", "norwegian_elkhound",
    "norwich_terrier", "old_english_sheepdog", "otterhound", "papillon", "pekinese", "pembroke",
    "pomeranian", "pug", "redbone", "rhodesian_ridgeback", "rottweiler", "saint_bernard", "saluki",
    "samoyed", "schipperke", "scotch_terrier", "scottish_deerhound", "sealyham_terrier",
    "shetland_sheepdog", "shih-tzu", "siberian_husky", "silky_terrier", "soft-coated_wheaten_terrier",
    "staffordshire_bullterrier", "standard_poodle", "standard_schnauzer", "sussex_spaniel",
    "tibetan_mastiff", "tibetan_terrier", "toy_poodle", "toy_terrier", "vizsla", "walker_hound",
    "weimaraner", "welsh_springer_spaniel", "west_highland_white_terrier", "whippet",
    "wire-haired_fox_terrier", "yorkshire_terrier"
]
# -------------------------
# Tkinter Application
# -------------------------
class PawtectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PAWsport Dog Breed Detector")

        # --- Window size ---
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        # --- Background image ---
        bg_image_path = r"D:\[ 0 ]\PAWsport\assets\background.png"
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 🔧 define pixel font (fallbacks to Pillow’s bitmap font)
        try:
            self.pixel_font = ImageFont.truetype("PixelEmulator-xq08.ttf", 20)
        except:
            self.pixel_font = ImageFont.load_default()

                # --- Frame for centered buttons ---
            # --- Frame for buttons on the left side ---
        self.btn_frame = tk.Frame(root, bg="", bd=0, highlightthickness=0, width=180)
        self.btn_frame.place(relx=1.0, rely=0.5, x=-130, anchor="e")

                # === Upload Button Image ===
        raw_upload = Image.open(r"D:\[ 0 ]\PAWsport\assets\1.png").convert("RGBA")
        bg_upload = Image.new("RGBA", raw_upload.size, "#fdf7e6")   # same as app bg
        bg_upload.paste(raw_upload, mask=raw_upload.split()[3])     # preserve transparency
        self.upload_img = ImageTk.PhotoImage(bg_upload)

        # === How To Button Image ===
        raw_howto = Image.open(r"D:\[ 0 ]\PAWsport\assets\2.png").convert("RGBA")
        bg_howto = Image.new("RGBA", raw_howto.size, "#fdf7e6")
        bg_howto.paste(raw_howto, mask=raw_howto.split()[3])
        self.howto_img = ImageTk.PhotoImage(bg_howto)

        # === Upload Button ===
        self.upload_btn = tk.Label(
            self.btn_frame,
            image=self.upload_img,
            bg="#fdf7e6",
            borderwidth=0,
            highlightthickness=0
        )
        self.upload_btn.pack(pady=10)
        self.upload_btn.bind("<Button-1>", lambda e: self.upload_photo())

        # === How To Button ===
        self.howto_btn = tk.Label(
            self.btn_frame,
            image=self.howto_img,
            bg="#fdf7e6",
            borderwidth=0,
            highlightthickness=0
        )
        self.howto_btn.pack(pady=10)
        self.howto_btn.bind("<Button-1>", lambda e: self.show_howto())


   
    def upload_photo(self):
        filetypes = (("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title="Select a photo", filetypes=filetypes)
        if not filepath:
            return
        self.predict_breed(filepath)

    def predict_breed(self, img_path):
        try:
            image = Image.open(img_path).convert("RGB")
            input_tensor = preprocess(image).unsqueeze(0)

            with torch.no_grad():
                output = model(input_tensor)
                predicted_class = torch.argmax(output, dim=1).item()

            breed = class_names[predicted_class]
            self.show_result_window(breed)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict breed:\n{e}")

   
    
    def show_result_window(self, breed):
        # Result window
        result_win = tk.Toplevel(self.root)
        result_win.title("Prediction Result")
        # change window icon
        icon_img = ImageTk.PhotoImage(Image.open(r"D:\[ 0 ]\PAWsport\assets\Untitled (800 x 600 px) (1).png"))
        result_win.iconphoto(False, icon_img)

        # set window size
        w, h = 800, 600
        sw, sh = result_win.winfo_screenwidth(), result_win.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        result_win.geometry(f"{w}x{h}+{x}+{y}")
        result_win.configure(bg="#f0e6d2")
        result_win.resizable(False, False)

        # load background
        self.result_bg = ImageTk.PhotoImage(
            Image.open(r"D:\[ 0 ]\PAWsport\assets\showresults.png").resize((w, h))
        )
        bg_label = tk.Label(result_win, image=self.result_bg, borderwidth=0, highlightthickness=0)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # container frame for text (aligned like buttons)
        text_frame = tk.Frame(result_win, bg="", bd=0)
        text_frame.place(relx=1.0, rely=0.5, x=-110, anchor="e")

        # load custom font (Bakso Sapi)
       
        bakso_font16 = tkFont.Font(family="Bakso Sapi", size=16, weight="bold")
        bakso_font22 = tkFont.Font(family="Bakso Sapi", size=22, weight="bold")
        bakso_font14 = tkFont.Font(family="Bakso Sapi", size=14)

        # breed text
        breed_text = breed.replace("_", " ").upper()

        lbl_title = tk.Label(
            text_frame,
            text="Detected Dog Breed:",
            font=bakso_font16,
            fg="#000000",
            bg="white"  # Set background to white
        )
        lbl_title.pack(pady=(0, 10))

        lbl_breed = tk.Label(
            text_frame,
            text=breed_text,
            font=bakso_font22,
            fg="#002060",
            bg="white"  # Set background to white
        )
        lbl_breed.pack(pady=(0, 10))

        lbl_desc = tk.Label(
            text_frame,
            text="This breed matches your PAWsport photo!",
            font=bakso_font14,
            fg="#402000",
            bg="white"  # Set background to white
        )
        lbl_desc.pack()

    def show_howto(self):
        howto_win = tk.Toplevel(self.root)
        howto_win.title("How to Use PAWsport")

        # change window icon
        icon_img = ImageTk.PhotoImage(Image.open(r"D:\[ 0 ]\PAWsport\assets\Untitled (800 x 600 px) (1).png"))
        howto_win.iconphoto(False, icon_img)
        
        # window size
        w, h = 800, 600
        sw, sh = howto_win.winfo_screenwidth(), howto_win.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        howto_win.geometry(f"{w}x{h}+{x}+{y}")
        
        howto_win.resizable(False, False)

        # load background image
        self.howto_bg = ImageTk.PhotoImage(
            Image.open(r"D:\[ 0 ]\PAWsport\assets\instructions.png").resize((w, h))
        )

        # put image in a label to act as full background
        bg_label = tk.Label(howto_win, image=self.howto_bg, borderwidth=0, highlightthickness=0)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


if __name__ == "__main__":
    root = tk.Tk()
     # --- Set window icon ---
    icon_path = r"D:\[ 0 ]\PAWsport\assets\Untitled (800 x 600 px) (1).png"
    icon_img = ImageTk.PhotoImage(file=icon_path)
    root.iconphoto(False, icon_img)
    app = PawtectorApp(root)
    root.mainloop()