from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
import pymysql
import os


class Formulaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire")
        self.root.geometry("1340x700+0+28")

        # les champs du formulaire
        frame1 = Frame(self.root, bg="grey")
        frame1.place(x=300, y=150, width=550, height=450)

        title = Label(frame1, text="Creer un compte", font=("algerian", 17, "bold"), bg="grey", fg="orange").place(x=40,
                                                                                                                   y=20)

        aff_prenom = Label(frame1, text="Prenom", font=("times new roman", 13, "bold"), bg="grey", fg="black").place(
            x=40, y=78)
        self.ecrire_prenom = Entry(frame1, font=("times new roman",), bg="lightgrey")
        self.ecrire_prenom.place(x=40, y=100, width=210)

        aff_nom = Label(frame1, text="Nom", font=("times new roman", 13, "bold"), bg="grey", fg="black").place(x=300,
                                                                                                               y=78)
        self.ecrire_nom = Entry(frame1, font=("times new roman",), bg="lightgrey")
        self.ecrire_nom.place(x=300, y=100, width=210)

        aff_telephone = Label(frame1, text="Telephone", font=("times new roman", 13, "bold"), bg="grey",
                              fg="black").place(x=40, y=137)
        self.ecrire_telephone = Entry(frame1, font=("times new roman",), bg="lightgrey")
        self.ecrire_telephone.place(x=40, y=160, width=210)

        aff_email = Label(frame1, text="Email", font=("times new roman", 13, "bold"), bg="grey", fg="black").place(
            x=300, y=137)
        self.ecrire_email = Entry(frame1, font=("times new roman",), bg="lightgrey")
        self.ecrire_email.place(x=300, y=160, width=210)

        aff_question = Label(frame1, text="Selectionner une Questions", font=("times new roman", 13, "bold"), bg="grey",
                             fg="black").place(x=40, y=200)
        self.ecrire_question = ttk.Combobox(frame1, font=("times new roman", 13), state="readonly")
        self.ecrire_question["values"] = (
            "Select", "Votre Surnom", "Lieu de Naissance", "Nom de Votre Meilleur(e) Ami(e)",
            "Nom de Votre Premier Animal",
            "Nom de Votre Premier amour")
        self.ecrire_question.place(x=40, y=223, width=210)
        self.ecrire_question.current(0)

        aff_reponse = Label(frame1, text="Reponse", font=("times new roman", 13, "bold"), bg="grey", fg="black").place(
            x=300, y=200)
        self.ecrire_reponse = Entry(frame1, font=("times new roman",), bg="lightgrey")
        self.ecrire_reponse.place(x=300, y=223, width=210)

        aff_password = Label(frame1, text="Password", font=("arial", 13, "bold"), bg="grey", fg="black").place(x=40,
                                                                                                               y=262)
        self.ecrire_password = Entry(frame1, show="*", font=("times new roman",), bg="lightgrey")
        self.ecrire_password.place(x=40, y=285, width=210)

        aff_confirmPassword = Label(frame1, text="Confirm Password", font=("arial", 13, "bold"), bg="grey",
                                    fg="black").place(x=300, y=262)
        self.ecrire_confirmPassword = Entry(frame1, show="*", font=("times new roman",), bg="lightgrey")
        self.ecrire_confirmPassword.place(x=300, y=285, width=210)

        self.var_chech = IntVar()
        chk = Checkbutton(frame1, variable=self.var_chech, onvalue=1, offvalue=0,
                          text="J'accepte les conditions et les termes", cursor="hand2", font=("times new roman", 10),
                          bg="grey").place(x=40, y=340)

        btn = Button(frame1, text="Creer", cursor="hand2", command=self.creer, font=("times new roman", 13, "bold"),
                     bg="cyan", fg="black").place(x=170, y=395, width=250)
        btn2 = Button(frame1, text="Connexion", cursor="hand2", font=("times new roman", 13, "bold"), bg="cyan",
                      fg="black").place(x=400, y=50, width=130)

    def creer(self):
        if self.ecrire_prenom.get() == "" or self.ecrire_nom.get() == "" or self.ecrire_email.get() == "" or self.ecrire_question.get() == "" or self.ecrire_confirmPassword.get() == "" or self.ecrire_password.get() == "" or self.ecrire_telephone.get() == "" or self.ecrire_reponse.get() == "":
            messagebox.showerror("Erreur", "Remplir les champs", parent=self.root)
        elif self.ecrire_password.get() != self.ecrire_confirmPassword.get():
            messagebox.showerror("Erreur", "Les mots de passes doivent etre identique", parent=self.root)
        elif self.var_chech.get() == 0:
            messagebox.showerror("Erreur", "Vous devez accepter les termes et conditions", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", port=8090, user="root", password="",
                                      database="buildingmanagement")
                cur = con.cursor()
                cur.execute("SELECT * FROM compte WHERE email=%s", self.ecrire_email.get())
                row = cur.fetchone()

                if row is not None:
                    messagebox.showerror("Erreur", "Cette adresse email existe déjà", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO compte (prenom, nom, telephone, email, question, reponse, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            self.ecrire_prenom.get(),
                            self.ecrire_nom.get(),
                            self.ecrire_telephone.get(),
                            self.ecrire_email.get(),
                            self.ecrire_question.get(),
                            self.ecrire_reponse.get(),
                            self.ecrire_password.get()
                        )
                    )
                    messagebox.showinfo("Success", "Votre compte a été créé", parent=self.root)
                    con.commit()
            except pymysql.Error as e:
                messagebox.showerror("Erreur", f"Erreur de connexion: {e}", parent=self.root)
            finally:
                con.close()


root = Tk()
obj = Formulaire(root)
root.mainloop()
