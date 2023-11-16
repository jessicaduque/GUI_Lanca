from customtkinter import *
import manageSubprocess
from PIL import Image
import _pickle as pickle
import ctypes
import cv2
import os

class App(CTk):
    def __init__(self):
        super().__init__()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        #x = (screen_width - APP_WIDTH ) / 2
        #y = (screen_height - APP_HEIGHT ) / 2

        ##### Configure window
        self.title("DashMedidor")
        #self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
        #self.wm_attributes('-fullscreen', True)
        self.minsize(screen_width, screen_height)
        self.resizable(1, 1)

        ##### Interface creation

        ### Configure grid layout 
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ### Configure header
        self.frameHeader = CTkFrame(self, height=100, fg_color='#a4a8ad', corner_radius=0)
        self.frameHeader.grid(row=0, column=0, sticky='nsew')

        self.frameHeader.columnconfigure(0, weight=1)
        self.frameHeader.columnconfigure(1, weight=1)
        self.frameHeader.columnconfigure(2, weight=1)

        ### Configure logo images into header
        # Defining image variables and sizes
        image_ifes_logo = CTkImage(light_image=Image.open('./imagens/IFES_horizontal_logo.png'), size=(215.46, 86.184))
        #image_empresa_logo = CTkImage(light_image=Image.open('./imagens/ArcelorMittal_logo.png'), size=(168, 69.12))

        image_empresa_logo = CTkImage(light_image=Image.open('./imagens/LumarMetals_Logo.jpg'), size=(265, 56))

        image_oficinas_logo = CTkImage(light_image=Image.open('./imagens/Oficinas4-0_logo.png'), size=(163.84, 33.6))

        # Configuring images

        self.image_ifes_logo_label = CTkLabel(self.frameHeader, image=image_ifes_logo, text="")
        self.image_ifes_logo_label.grid(row=0, column=0, padx=(20, 0))
        
        self.image_empresa_logo_label = CTkLabel(self.frameHeader, image=image_empresa_logo, text="")
        self.image_empresa_logo_label.grid(row=0, column=1)
        
        self.image_oficinas_logo_label = CTkLabel(self.frameHeader, image=image_oficinas_logo, text="")
        self.image_oficinas_logo_label.grid(row=0, column=2, padx=(0, 20))

        ### Configure main frame
        self.primary_frame = CTkFrame(self, fg_color='#4f7d71', corner_radius=0)
        self.primary_frame.grid(row=1, column=0, sticky='nsew')

        self.primary_frame.rowconfigure(0, weight=1)
        self.primary_frame.rowconfigure(1, weight=1)
        self.primary_frame.columnconfigure(0, weight=2)
        self.primary_frame.columnconfigure(1, weight=1)

        # Configure top widgets
        self.video_frame = CTkFrame(self.primary_frame, fg_color="#a4a8ad", corner_radius=15)
        self.video_frame.grid(row=0, column=0, padx=(30, 10), pady=(10, 10), sticky='nsew')
        
        image_video = CTkImage(light_image=Image.open('./imagens/IFES_logo.png'), size=(400 * 0.7, 400 * 0.7))
        self.video_widget = CTkLabel(self.video_frame, image=image_video, text="")
        self.video_widget.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.gaugeGraph_frame = CTkFrame(self.primary_frame, fg_color="#a4a8ad", corner_radius=15)
        self.gaugeGraph_frame.grid(row=0, column=1, padx=(0, 30), pady=(10, 10), sticky='nsew')

        gaugeGraph_image = CTkImage(Image.open('./imagens/IFES_logo.png'), size=(400 * 0.7, 400 * 0.7))

        self.button = CTkButton(self.gaugeGraph_frame, text="PARAR APITO", width=240, text_color="black", hover_color="#bdc3c9", 
                                border_width=2, border_color="black", fg_color='white', command=self.button_event_reset_diametro_gauge)

        self.button.pack(pady=(0,20), anchor='s')


        self.gaugeGraph_label = CTkLabel(self.gaugeGraph_frame, image=gaugeGraph_image, text="")
        self.gaugeGraph_label.pack(padx=10, pady=10, anchor='n')
       
        # Configure bottom widgets
        self.lineGraph_frame = CTkFrame(self.primary_frame, fg_color="#a4a8ad", corner_radius=15)
        self.lineGraph_frame.grid(row=1, columnspan=2, padx=30, pady=(0, 10), sticky='nsew')

        lineGraph_image = CTkImage(Image.open('./imagens/IFES_horizontal_logo.png'), size=(600 * 0.7, 250* 0.7))
        self.lineGraph_label = CTkLabel(self.lineGraph_frame, image=lineGraph_image, text="")
        self.lineGraph_label.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Continuously run methods updating the image, plots segmentation and graphs
        self.update_image()
        self.update_plot_gauge()
        self.update_plot_line()

        # Bind to resize the images if the screen size changes
        self.gaugeGraph_label.bind("<Configure>", lambda event:self.resize_image(event, "Gauge"))
        self.lineGraph_label.bind("<Configure>", lambda event:self.resize_image(event, "Line"))
        self.video_widget.bind("<Configure>", lambda event:self.resize_image(event, "Video"))


    def button_event_reset_diametro_gauge(self):
        manageSubprocess.KillSubprocess_All()

        #self.gaugeGraph_label.configure(image=gaugeGraph_image) 
        #self.gaugeGraph_label.image = gaugeGraph_image

        #self.lineGraph_label.configure(image=lineGraph_image) 
        #self.lineGraph_image.image = self.lineGraph_image

        #self.video_widget.configure(image=self.image_video) 
        #self.video_widget.image = image_video


        processDone = manageSubprocess.ChecarSubprocessesDone()
        while(not processDone):
            processDone = manageSubprocess.ChecarSubprocessesDone()
            time.sleep(1)

        manageSubprocess.StartSubprocess_All()

    # Resize function
    def resize_image(self, event, extra):
        newSize = (event.width, event.height)
        #if(extra == "Gauge"):
        #    gaugeGraph_image = CTkImage(Image.open('./imagens/gaugeDiametro.png'),
        #        size=newSize
        #        )
        #    self.gaugeGraph_label = CTkLabel(self.gaugeGraph_frame, image=gaugeGraph_image, text="")
        #    self.gaugeGraph_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Function to update the segmented video
    def update_image(self):
        try:
            # Load pickled PIL image
            f = open('./pickle_data/frame_pickle.pkl', 'rb')
            img_data = pickle.load(f)
            f.close()
            del f
            img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
            # Convert numpy array to PIL image
            frame = Image.fromarray(img_data)
            #img_data = None
            del img_data
            self.image_video = CTkImage(light_image=frame, size=(840, 420))
            self.video_widget.configure(image=self.image_video)
            self.video_widget.pack(padx=10, pady=10, fill=BOTH, expand=True)

        except Exception as e:
            print(e)
        finally:
            self.after(30, self.update_image)

    # Funcion to update the gauge graph
    def update_plot_gauge(self):
        try:

            f = open('./pickle_data/gaugeGraph_pickle.pkl', 'rb')
            img_data_gauge_graph = pickle.load(f)
            f.close()
            del f
            gaugeGraph_frame = Image.fromarray(img_data_gauge_graph)
            self.gaugeGraph_image = CTkImage(light_image=gaugeGraph_frame, size=(750 * 0.7, 500 * 0.7))
            self.gaugeGraph_label.configure(image=self.gaugeGraph_image)
            self.gaugeGraph_label.pack(fill=BOTH, expand=True, padx=10, pady=10)

        except Exception as e:
            print(e)

        finally:
            self.after(1000, self.update_plot_gauge)

    # Function to update the line graph
    def update_plot_line(self):
        try:

            f = open('./pickle_data/lineGraph_pickle.pkl', 'rb')
            img_data_line_graph = pickle.load(f)
            f.close()
            del f
            lineGraph_frame = Image.fromarray(img_data_line_graph)
            self.lineGraph_image = CTkImage(light_image=lineGraph_frame, size=(1300, 350))
            self.lineGraph_label.configure(image=self.lineGraph_image)
            self.lineGraph_label.pack(fill=BOTH, expand=True, padx=10, pady=10)

        except Exception as e:
            print(e)

        finally:
            self.after(1000, self.update_plot_line)
    
if __name__ == "__main__":
    ### Variables
    # Defining original DPI being used
    ORIGINAL_DPI = 96.09458128078816
    APP_WIDTH = 1000
    APP_HEIGHT = 720
    w_img, h_img = 30, 30

    #manageSubprocess.StartSubprocess_All()   
    
    # Starting the app
    app = App()
    # Setting up all subprocesses
    manageSubprocess.StartSubprocess_All()   
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    
    # Function that stops the subprocesses when closing the app
    def on_closing():
        try:
            manageSubprocess.KillSubprocess_All()  
        except Exception as e:
            print(e)

        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'pickle_data/diameter_pickle.pkl'))
        except Exception as e:
            print(e)

        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'pickle_data/date_pickle.pkl'))
        except Exception as e:
            print(e)

        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'pickle_data/time_pickle.pkl'))
        except Exception as e:
            print(e)

        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'pickle_data/frame_pickle.pkl'))
        except Exception as e:
            print(e)
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'pickle_data/gaugeGraph_pickle.pkl'))
        except Exception as e:
            print(e)   
          
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'pickle_data/lineGraph_pickle.pkl'))
        except Exception as e:
            print(e)   

        # Deleting app window
        app.destroy()

    # Protocol to execute on_closing function when the X is clicked on the app
    app.protocol("WM_DELETE_WINDOW", on_closing)    
    app.mainloop()
