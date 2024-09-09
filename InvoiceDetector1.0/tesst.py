import customtkinter


def start_progressbar(value):
    progressbar.set(value)

    if value < 1:
        # after() arguments: time in ms, function to call, arguments to the function
        app.after(1000, start_progressbar, value + 1/10)


app = customtkinter.CTk()

progressbar = customtkinter.CTkProgressBar(master=app)
progressbar.pack(padx=20, pady=20)
progressbar.set(0.0)

start_progressbar(0)

app.mainloop()