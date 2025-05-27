"""
Text-to-Speech Application with GUI
"""

import os
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import pyttsx3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Initialize TTS engine with preference for SAPI5 on Windows
try:
    engine = pyttsx3.init('sapi5')  # Prefer SAPI5 on Windows
    current_os = "windows"
    
    # Check if female voice is available on Windows
    voices = engine.getProperty('voices')
    has_female = any('female' in voice.name.lower() for voice in voices)
except:
    try:
        engine = pyttsx3.init()  # Fallback for other platforms
        current_os = "linux"
        has_female = False
    except Exception as e:
        messagebox.showerror("Initialization Error", f"Failed to initialize TTS engine: {str(e)}")
        exit()

root = Tk()
root.title("Text to Speech")
root.geometry("900x450+200+200")
root.resizable(False, False)
root.configure(bg="#305065")

def get_voices():
    try:
        voices = engine.getProperty('voices')
        # Prioritize English voices
        return sorted(voices, key=lambda v: 0 if 'english' in v.name.lower() else 1)
    except Exception as e:
        messagebox.showerror("Voice Error", f"Error getting voices: {str(e)}")
        return []

def set_voice(gender):
    try:
        voices = get_voices()
        
        if current_os == "windows" and has_female:
            # Windows voice selection with gender support
            for voice in voices:
                name = voice.name.lower()
                if gender.lower() in name:
                    engine.setProperty("voice", voice.id)
                    return
            # Fallback to first voice if specific gender not found
            if voices:
                engine.setProperty("voice", voices[0].id)
        else:
            # Linux or Windows without female voice - use first available voice
            if voices:
                engine.setProperty("voice", voices[0].id)
    except Exception as e:
        messagebox.showerror("Voice Error", f"Error setting voice: {str(e)}")

def get_unique_filename(directory, base_name="text", extension=".mp3"):
    """Generate a unique filename in the specified directory."""
    try:
        counter = 0
        while True:
            if counter == 0:
                filename = f"{base_name}{extension}"
            else:
                filename = f"{base_name}{counter}{extension}"
            
            full_path = os.path.join(directory, filename)
            if not os.path.exists(full_path):
                return full_path
            counter += 1
    except Exception as e:
        messagebox.showerror("File Error", f"Error generating filename: {str(e)}")
        return os.path.join(directory, f"{base_name}{extension}")

def speaknow():
    """Convert the entered text to speech and play it immediately."""
    text = text_area.get(1.0, END).strip()
    if not text:
        messagebox.showwarning("No Text", "Please enter text to speak")
        return
        
    try:
        gender = gender_combobox.get() if (current_os == "windows" and has_female) else "Male"
        speed = speed_combobox.get()
        
        # Set speed - adjusted values that work better across platforms
        speed_map = {"Fast": 200, "Normal": 150, "Slow": 100}
        engine.setProperty("rate", speed_map.get(speed, 150))
        
        # Set voice
        set_voice(gender)
        
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        messagebox.showerror("Speech Error", f"Error during speech: {str(e)}")


def download():
    """Save the entered text as an audio file."""
    text = text_area.get(1.0, END).strip()
    if not text:
        messagebox.showwarning("No Text", "Please enter text to save")
        return
        
    try:
        gender = gender_combobox.get() if (current_os == "windows" and has_female) else "Male"
        speed = speed_combobox.get()
        
        # Set speed
        speed_map = {"Fast": 200, "Normal": 150, "Slow": 100}
        engine.setProperty("rate", speed_map.get(speed, 150))
        
        # Set voice
        set_voice(gender)
        
        path = filedialog.askdirectory()
        if not path:  
            return
            
        output_file = get_unique_filename(path)
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        # Verify file was created
        if os.path.exists(output_file):
            messagebox.showinfo("File Saved", f"File saved as:\n{os.path.basename(output_file)}")
        else:
            messagebox.showerror("Save Error", "File was not created successfully")
            
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving file: {str(e)}")

# GUI Elements
Top_frame = Frame(root, bg="white", width=900, height=80)
Top_frame.place(x=0, y=0)

try:
    image_icon = PhotoImage(file=BASE_DIR / "assets" / "icons" / "speak.png")
    root.iconphoto(False, image_icon)
    Logo = PhotoImage(file=BASE_DIR / "assets" / "icons" / "mic.png")
    Label(Top_frame, image=Logo, bg="white").place(x=10, y=5)
    imageicon = PhotoImage(file=BASE_DIR / "assets" / "icons" / "speak.png")
    imageicon2 = PhotoImage(file=BASE_DIR / "assets" / "icons" / "download.png")
except:
    pass

Label(Top_frame, text="TEXT TO SPEECH", font="arial 20 bold", bg="white", fg="black").place(x=100, y=30)

# Text Area
text_area = Text(root, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text_area.place(x=10, y=150, width=500, height=250)

# Voice Selection
Label(root, text="VOICE", font="arial 15 bold", bg="#305065", fg="white").place(x=580, y=160)

# Set voice options based on OS and available voices
if current_os == "windows" and has_female:
    voice_options = ["Male", "Female"]
else:
    voice_options = ["Male"]  # Only show Male on Linux or Windows without female voice

gender_combobox = Combobox(root, values=voice_options, font="arial 14", state="readonly", width=10)
gender_combobox.place(x=550, y=200)
gender_combobox.set("Male")

# Speed Selection
Label(root, text="SPEED", font="arial 15 bold", bg="#305065", fg="white").place(x=760, y=160)
speed_combobox = Combobox(root, values=["Fast", "Normal", "Slow"], font="arial 14", state="readonly", width=10)
speed_combobox.place(x=730, y=200)
speed_combobox.set("Normal")

# Buttons
try:
    btn = Button(root, text="Speak", compound=LEFT, image=imageicon, width=130, font="arial 14 bold", command=speaknow)
    save = Button(root, text="Save", compound=LEFT, image=imageicon2, width=130, bg="#39c790", font="arial 14 bold", command=download)
except:
    btn = Button(root, text="Speak", width=130, font="arial 14 bold", command=speaknow)
    save = Button(root, text="Save", width=130, bg="#39c790", font="arial 14 bold", command=download)

btn.place(x=550, y=280)
save.place(x=730, y=280)


# Start the application
root.mainloop()