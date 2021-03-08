from tkinter import *
from tkinter.ttk import *
from tkcalendar import *
import csv
import pandas
import os
from datetime import datetime


class Client:
    def __init__(self, kind, name, id_client, address, surname="", birth="", phone="", e_mail=""):
        self.name = name
        self.surname = surname
        self.id_client = id_client
        self.phone = phone
        self.e_mail = e_mail
        self.address = address
        self.birth = birth
        self.kind = kind

    def saving_new_client(self):
        if self.kind == 'patient':
            path = f"{self.config_files()['path_save_client']}/{self.id_client}_{self.name}_{self.surname}"
            with open(path, 'w') as files:
                files.write(str(self))
                files.close()
            with open(self.config_files()['path_client_list'], 'a', newline='') as id_files:
                id_reg = csv.writer(id_files)
                id_reg.writerow([self.id_client, self.name, self.surname, str(self.phone)])
                id_files.close()
            print("register donne")
        if self.kind == 'structure':
            path = f"{self.config_files()['path_save_client']}/{self.id_client}_{self.name}"
            with open(path, 'w') as files:
                files.write(str(self))
                files.close()
            with open(self.config_files()['path_client_list'], 'a', newline='') as id_files:
                id_reg = csv.writer(id_files)
                id_reg.writerow([self.id_client, self.name, str(self.phone)])
                id_files.close()
            print("register donne")

    @staticmethod
    def config_files():
        dic_conf = {}
        with open("config.txt", 'r') as config_files:
            config = config_files.readlines()
            for row in config:
                conf = row.split("=")
                dic_conf[conf[0]] = conf[1].replace("\n", "")
            return dic_conf

    def __str__(self):
        if self.kind == 'patient':
            return f"GENERAL \n\nPrenom : {self.name} \nNom : {self.surname} \nNumero client : {self.id_client}\nDate "\
                   f"de naissance : {self.birth} \n\nCONTACT\n\nNumero de telephone : {self.phone} \nE-" \
                   f"Mail : {self.e_mail} \n\nADDRESS\n\nRue : {self.address['street']}\nCode Postal : " \
                   f"{self.address['post_code']}     Ville : {self.address['city']} "
        elif self.kind == 'structure':
            return f"GENERAL \n\n\nNom : {self.surname} \nNumero client : {self.id_client} \n" \
                   f"\nCONTACT\n\nNumero de telephone : {self.phone} \nE-Mail : {self.e_mail} \n\nADDRESS\n\n" \
                   f"Rue : {self.address['street']}\nCode Postal : {self.address['post_code']}     Ville : " \
                   f"{self.address['city']} "


class Gui(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Outils de compta du cabinet")
        self.iconbitmap('logo.ico')
        self.start_windget()

    @staticmethod
    def config_files():
        dic_conf = {}
        with open("config.txt", 'r') as config_files:
            config = config_files.readlines()
            for row in config:
                conf = row.split("=")
                dic_conf[conf[0]] = conf[1].replace("\n", "")
            return dic_conf

    def start_windget(self):

        # tab section
        tab = Notebook(self)
        tab.pack()

        new_client = Frame(tab)
        new_client.grid()

        billing = Frame(tab)
        billing.grid()

        client_list = Frame(tab)
        client_list.grid()

        tab.add(billing, text="Facturation")
        tab.add(new_client, text="Nouveau client")
        tab.add(client_list, text="Liste des clients")

        # Widgets
        self.billing_tab(billing)
        self.new_client_tab(new_client, client_list)

        # Type of service

    def billing_tab(self, tab):

        service_type = StringVar()
        service_list = ("Cosultation", "Supervision", "Fornation")
        list_service = Combobox(tab, textvariable=service_type, values=service_list, state='readonly')
        list_service.grid()
        service_type.set(service_list[0])

        # Entry for new client

    def new_client_tab(self, tab, tab2):
        def make_new_client():
            client_address = {"street": new_client_street.get(),
                              "post_code": new_client_post_code.get(),
                              "city": new_client_city.get()}
            client = Client("patient",
                            str(new_client_name.get()).capitalize(),
                            new_client_id.get(),
                            client_address,
                            str(new_client_surname.get()).upper(),
                            str(new_client_birth.get()),
                            str(new_client_phone.get()),
                            str(new_client_mail.get()))
            client.saving_new_client()

            label_client_list_id.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                             usecols=['ID']).to_string(index=False))
            label_client_list_surname.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                  usecols=['NOM']).to_string(index=False))
            label_client_list_name.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                               usecols=['PRENOM']).to_string(index=False))
            label_client_list_phone.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                usecols=['TELEPHONE']).to_string(index=False))
            clear_new_patient()
            clear_new_structure()

        def clear_new_patient():
            new_client_city.set("")
            new_client_id.set(f"c_{self.create_id()}")
            new_client_birth.set("")
            new_client_name.set("")
            new_client_mail.set("")
            new_client_post_code.set("")
            new_client_phone.set("")
            new_client_street.set("")
            new_client_surname.set("")

        def set_id_structure():
            new_structure_id.set(f"s_{self.create_id()}")

        new_client_tab = Notebook(tab)
        new_client_tab.grid()

        new_patient = Frame(new_client_tab)
        new_patient.grid()

        new_structure_tab = Frame(new_client_tab)
        new_structure_tab.grid()

        new_client_tab.add(new_patient, text="Patient")
        new_client_tab.add(new_structure_tab, text="Structure")

        # Type patient
        label_general_data = Label(new_patient, text="INFORMATION GENERALE")
        label_general_data.grid(row=0, columnspan=2)
        label_client_name = Label(new_patient, text="Prenom")
        new_client_name = StringVar()
        entry_client_name = Entry(new_patient, textvariable=new_client_name)
        label_client_name.grid(row=1, column=0, pady=2.5)
        entry_client_name.grid(row=1, column=1, pady=2.5)

        label_client_surname = Label(new_patient, text="Nom ")
        new_client_surname = StringVar()
        entry_client_surname = Entry(new_patient, textvariable=new_client_surname)
        label_client_surname.grid(row=2, column=0, pady=2.5)
        entry_client_surname.grid(row=2, column=1, pady=2.5)

        label_client_id = Label(new_patient, text="Numero Client")
        new_client_id = StringVar()
        entry_client_id = Entry(new_patient, textvariable=new_client_id)
        new_client_id.set(f"c_{self.create_id()}")
        label_client_id.grid(row=3, column=0, pady=2.5)
        entry_client_id.grid(row=3, column=1, pady=2.5)

        label_client_birth_date = Label(new_patient, text="Date de naissance")
        new_client_birth = StringVar()
        entry_client_birth = DateEntry(new_patient, textvariable=new_client_birth)
        label_client_birth_date.grid(row=4, column=0, pady=2.5)
        entry_client_birth.grid(row=4, column=1, pady=2.5)

        label_contact = Label(new_patient, text="CONTACT")
        label_contact.grid(row=5, columnspan=2)

        label_client_phone = Label(new_patient, text="Numero de telephone")
        new_client_phone = StringVar()
        entry_client_phone = Entry(new_patient, textvariable=new_client_phone)
        label_client_phone.grid(row=6, column=0, pady=2.5)
        entry_client_phone.grid(row=6, column=1, pady=2.5)

        label_client_mail = Label(new_patient, text="E-mail")
        new_client_mail = StringVar()
        entry_client_mail = Entry(new_patient, textvariable=new_client_mail)
        label_client_mail.grid(row=7, column=0, pady=2.5)
        entry_client_mail.grid(row=7, column=1, pady=2.5)

        label_address = Label(new_patient, text="ADRESSE")
        label_address.grid(row=8, columnspan=2)

        frame_address = Frame(new_patient)

        label_client_street = Label(frame_address, text="Rue")
        new_client_street = StringVar()
        entry_client_street = Entry(frame_address, textvariable=new_client_street, width='50')
        label_client_street.grid(row=0, column=0, pady=2.5)
        entry_client_street.grid(row=0, column=1, pady=2.5)

        label_client_post_code = Label(frame_address, text="Code Postal")
        new_client_post_code = StringVar()
        entry_client_post_code = Entry(frame_address, textvariable=new_client_post_code)
        label_client_post_code.grid(row=1, column=0, pady=2.5)
        entry_client_post_code.grid(row=1, column=1, pady=2.5)

        label_client_city = Label(frame_address, text="Ville")
        new_client_city = StringVar()
        entry_client_city = Entry(frame_address, textvariable=new_client_city)
        label_client_city.grid(row=1, column=3, pady=2.5)
        entry_client_city.grid(row=1, column=4, pady=2.5)

        frame_address.grid(row=9, columnspan=2, pady=2.5)

        validate_button = Button(new_patient, text="Valider", command=make_new_client)
        validate_button.grid(row=10, column=0, pady=2.5)
        clear_button = Button(new_patient, text="Effacer", command=clear_new_patient)
        clear_button.grid(row=10, column=1, pady=2.5)

        # New Structure
        def create_new_structure():
            structure_address = {"street": new_structure_street.get(),
                                 "post_code": new_structure_post_code.get(),
                                 "city": new_structure_city.get()}
            client = Client('structure',
                            str(new_structure_name.get()).capitalize(),
                            new_structure_id.get(),
                            structure_address,
                            str(new_structure_phone.get()),
                            str(new_structure_mail.get()))
            client.saving_new_client()
            label_client_list_id.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                             usecols=['ID']).to_string(index=False))
            label_client_list_surname.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                  usecols=['NOM']).to_string(index=False))
            label_client_list_name.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                               usecols=['PRENOM']).to_string(index=False))
            label_client_list_phone.config(text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                usecols=['TELEPHONE']).to_string(index=False))
            clear_new_structure()
            clear_new_patient()

        def clear_new_structure():
            new_structure_id.set(f"s_{self.create_id()}")
            new_structure_post_code.set("")
            new_structure_city.set("")
            new_structure_street.set("")
            new_structure_name.set("")
            new_structure_mail.set("")
            new_structure_phone.set("")

        label_structure_generale = Label(new_structure_tab, text="GENERALE")
        label_structure_generale.grid(row=0, columnspan=2, pady=2.5)
        label_structure_name = Label(new_structure_tab, text="Nom structure")
        label_structure_name.grid(row=1, column=0, pady=2.5)
        new_structure_name = StringVar()
        entry_structure_name = Entry(new_structure_tab, textvariable=new_structure_name)
        entry_structure_name.grid(row=1, column=1, pady=2.5)

        label_id_structure = Label(new_structure_tab, text="Numero client")
        new_structure_id = StringVar()
        entry_structure_id = Entry(new_structure_tab, textvariable=new_structure_id)
        self.after(5, set_id_structure)
        label_id_structure.grid(row=3, column=0, pady=2.5)
        entry_structure_id.grid(row=3, column=1, pady=2.5)

        label_structure_contact = Label(new_structure_tab, text="CONTACT")
        label_structure_contact.grid(row=4, columnspan=2, pady=2.5)

        label_structure_phone = Label(new_structure_tab, text="Numero telephone")
        new_structure_phone = StringVar()
        entry_structure_phone = Entry(new_structure_tab, textvariable=new_structure_phone)
        label_structure_phone.grid(row=5, column=0, pady=2.5)
        entry_structure_phone.grid(row=5, column=1, pady=2.5)

        label_structure_mail = Label(new_structure_tab, text="E-Mail")
        new_structure_mail = StringVar()
        entry_structure_mail = Entry(new_structure_tab, textvariable=new_structure_mail)
        label_structure_mail.grid(row=6, column=0, pady=2.5)
        entry_structure_mail.grid(row=6, column=1, pady=2.5)

        label_structure_address = Label(new_structure_tab, text="ADRESSE")
        label_structure_address.grid(row=7, columnspan=2, pady=2.5)
        frame_address_structure = Frame(new_structure_tab)

        label_structure_street = Label(frame_address_structure, text="Rue")
        new_structure_street = StringVar()
        entry_structure_street = Entry(frame_address_structure, textvariable=new_structure_street, width='50')
        label_structure_street.grid(row=0, column=0, pady=2.5)
        entry_structure_street.grid(row=0, column=1, pady=2.5)

        label_structure_post_code = Label(frame_address_structure, text="Code Postal")
        new_structure_post_code = StringVar()
        entry_structure_post_code = Entry(frame_address_structure, textvariable=new_structure_post_code)
        label_structure_post_code.grid(row=1, column=0, pady=2.5)
        entry_structure_post_code.grid(row=1, column=1, pady=2.5)

        label_structure_city = Label(frame_address_structure, text="Ville")
        new_structure_city = StringVar()
        entry_structure_city = Entry(frame_address_structure, textvariable=new_structure_city)
        label_structure_city.grid(row=1, column=3, pady=2.5)
        entry_structure_city.grid(row=1, column=4, pady=2.5)

        frame_address_structure.grid(row=8, columnspan=2, pady=2.5)

        button_structure_validate = Button(new_structure_tab, text="Valider", command=create_new_structure)
        button_structure_clear = Button(new_structure_tab, text="Effacer", command=clear_new_structure)
        button_structure_validate.grid(row=9, column=0)
        button_structure_clear.grid(row=9, column=1)
        # Client List
        container = Frame(tab2)
        canvas = Canvas(container)
        scrollar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scr_frame_client_list = Frame(canvas)

        scr_frame_client_list.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scr_frame_client_list, anchor='nw')
        canvas.configure(yscrollcommand=scrollar.set)
        container.grid(row=0, column=0)
        canvas.grid(row=0, column=0)
        scrollar.grid(row=0, column=1)
        label_client_list_id = Label(scr_frame_client_list, text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                usecols=['ID']).to_string(index=False))
        label_client_list_surname = Label(scr_frame_client_list, text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                     usecols=['NOM']).to_string(index=False))
        label_client_list_name = Label(scr_frame_client_list, text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                  usecols=['PRENOM']).to_string(index=False))
        label_client_list_phone = Label(scr_frame_client_list, text=pandas.read_csv(self.config_files()['path_client_list'],
                                                                   usecols=['TELEPHONE']).to_string(index=False))
        label_client_list_id.grid(row=0, column=0, padx=2.5)
        label_client_list_surname.grid(row=0, column=1, padx=2.5)
        label_client_list_name.grid(row=0, column=2, padx=2.5)
        label_client_list_phone.grid(row=0, column=3, padx=2.5)

    def create_id(self):
        if os.path.exists(self.config_files()['path_client_list']):
            read = pandas.read_csv(self.config_files()['path_client_list'], usecols=['ID'])
            id = str(read.iloc[-1][-1].replace('c_', "").replace('s_', "")).split("_")
            id[-1] = str(int(id[-1])+1)
            return f"{id[0]}_{id[1]}_{id[2]}"
        else:
            with open(self.config_files()['path_client_list'], 'a', newline='') as id_files:
                id_reg = csv.writer(id_files)
                id_reg.writerow(["ID", "PRENOM", "NOM", "TELEPHONE"])
                id_files.close()
                return f"{datetime.now().year}_{datetime.now().month}_1"


def main():
    app = Gui()
    app.mainloop()
    app.create_id()


if __name__ == '__main__':
    main()
