import oracledb
from faker import Faker
import random
import tkinter as tk
import os

with oracledb.connect(user="", password="", dsn="") as connection:
    with connection.cursor() as cursor:
        faker = Faker()
        jaka_tabela = "x"
        lose = 1

        for r in cursor.execute("""SELECT * from zamowienia"""):
            print(r)

        table_names = ['Wszystkie']
        for table in cursor.execute('SELECT table_name FROM user_tables'):
            table_names.append(table[0])

        def on_click():
            selected_table = entry.get()
            jaka_tabela = selected_table
            ilosc_zap = int( num_rows_entry.get())
            print(f"Selected table: {selected_table} {ilosc_zap}")
            pole=''
            global last_date
            last_date = '-10y'

            if jaka_tabela == "ADRES" or jaka_tabela == "Wszystkie":
                cursor.execute("SELECT MAX(id_adres) FROM adres")
                max_id = cursor.fetchone()[0]
                if max_id is None:
                    max_id = 0
                for x in range(ilosc_zap):
                    max_id = int(max_id + 1)
                    id_adres = max_id
                    miejscowosc = faker.city()
                    kod_pocztowy = faker.postcode()
                    ulica = faker.street_name()
                    nr_domu = random.randint(1, 100)
                    sql = f"INSERT INTO adres (id_adres, miejscowosc, kod_pocztowy, ulica, nr_domu) VALUES ({id_adres}, '{miejscowosc}', '{kod_pocztowy}', '{ulica}', {nr_domu})"
                    pole = pole + sql + "\n"
                    print(sql)
                    cursor.execute(sql)
                connection.commit()

            try:
                # magazyn insert
                if jaka_tabela == "MAGAZYN" or jaka_tabela == "Wszystkie":


                    cursor.execute("SELECT MAX(id_magazyn) FROM magazyn")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(ilosc_zap):
                        max_id = int(max_id + 1)
                        id_magazyn = int(max_id)
                        nazwa = faker.uuid4()[:8].upper()
                        powierzchnia = random.randint(500, 5000)
                        ilosc = random.randint(1, 10)
                        adres_id_adres = id_magazyn
                        sql = f"INSERT INTO magazyn (id_magazyn, nazwa, powierzchnia, ilosc, adres_id_adres) VALUES ({id_magazyn}, '{nazwa}', {powierzchnia}, {ilosc}, {adres_id_adres})"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli adres")

            try:
            # klient insert
                if jaka_tabela == "KLIENT" or jaka_tabela == "Wszystkie":
                    cursor.execute("SELECT MAX(id_klient) FROM klient")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(ilosc_zap):
                        max_id = int(max_id + 1)
                        id_klient = int(max_id)
                        imie = faker.first_name()
                        nazwisko = faker.last_name()
                        telefon = str(random.randint(1000000, 999999999))
                        adres_id_adres = id_klient
                        sql = f"INSERT INTO klient (id_klient, imie, nazwisko, telefon, adres_id_adres) VALUES ({id_klient}, '{imie}', '{nazwisko}', '{telefon}', {adres_id_adres})"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli adres")

            try:
            # insert karta
                if jaka_tabela == "KARTA" or jaka_tabela == "Wszystkie":
                    cursor.execute("SELECT MAX(id_karta) FROM karta")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(ilosc_zap):
                        max_id = int(max_id + 1)
                        id_karta = int(max_id)
                        punkty = random.randint(100, 1000)
                        data_zalozenia = faker.date_between(start_date=last_date, end_date="today")
                        last_date= data_zalozenia
                        klient_id_klient = id_karta
                        sql = f"INSERT INTO karta (id_karta, punkty, data_zalozenie, klient_id_klient) VALUES ({id_karta}, {punkty}, TO_DATE('{data_zalozenia.strftime('%Y-%m-%d')}', 'YYYY-MM-DD'), {klient_id_klient})"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli klienci")

            # insert dzial
            if jaka_tabela == "DZIAL" or jaka_tabela == "Wszystkie":

                cursor.execute("SELECT MAX(id_dzial) FROM dzial")
                czy_puste = cursor.fetchone()[0]
                print(czy_puste)
                if czy_puste is None:
                    dzial_table = ['biuro', 'infolinia', 'zarzad', 'pakowanie']
                    cursor.execute("SELECT MAX(id_dzial) FROM dzial")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(len(dzial_table)):
                        max_id = int(max_id + 1)
                        id_dzial = int(max_id)
                        idx = random.randint(0, 3)
                        nazwa = dzial_table[idx]
                        sql = f"INSERT INTO dzial (id_dzial, nazwa) VALUES ({id_dzial}, '{nazwa}')"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                connection.commit()

            # insert status
            if jaka_tabela == "STATUS" or jaka_tabela == "Wszystkie":

                cursor.execute("SELECT MAX(id_status) FROM status")
                czy_puste = cursor.fetchone()[0]
                print(czy_puste)
                if czy_puste is None:
                    status_table = ['przyjete', 'w przygotowaniu', 'ukończone', 'wysłane']
                    cursor.execute("SELECT MAX(id_status) FROM status")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(len(status_table)):
                        max_id = int(max_id + 1)
                        id_status = int(max_id)
                        idx = random.randint(0, 3)
                        nazwa = status_table[idx]
                        sql = f"INSERT INTO status (id_status, nazwa) VALUES ({id_status}, '{nazwa}')"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                connection.commit()

            try:
            # insert pracownik
                if jaka_tabela == "PRACOWNIK" or jaka_tabela == "Wszystkie":
                    cursor.execute("SELECT MAX(id_pracownik) FROM pracownik")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(ilosc_zap):
                        max_id = int(max_id + 1)
                        id_pracownik = int(max_id)
                        imie = faker.first_name()
                        nazwisko = faker.last_name()
                        dzial_id_dzial = random.randint(1, 4)
                        sql = f"INSERT INTO pracownik (id_pracownik, imie, nazwisko, dzial_id_dzial) VALUES ({id_pracownik}, '{imie}', '{nazwisko}', {dzial_id_dzial})"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli dział")

            # insert towar
            if jaka_tabela == "TOWAR" or jaka_tabela == "Wszystkie":
                cursor.execute("SELECT MAX(id_towar) FROM towar")
                max_id = cursor.fetchone()[0]
                if max_id is None:
                    max_id = 0

                for x in range(ilosc_zap):
                    max_id = int(max_id + 1)
                    id_towar = int(max_id)
                    nazwa = faker.random.choice(['róża', 'tulipan', 'lilia', 'słonecznik', 'chryzantema'])
                    cena = round(random.uniform(10.0, 1000.0), 2)
                    kraj = faker.country()
                    kraj = kraj.replace("'", "")
                    sql = f"INSERT INTO towar (id_towar, nazwa, cena, kraj) VALUES ({id_towar}, '{nazwa}', {cena}, '{kraj}')"
                    pole = pole + sql + "\n"
                    print(sql)
                    cursor.execute(sql)
                connection.commit()
            last_date='-10y'

            try:
                # insert zamowienia
                if jaka_tabela == "ZAMOWIENIA" or jaka_tabela == "Wszystkie":
                    cursor.execute("SELECT MAX(id_zamowienia) FROM zamowienia")
                    max_id = cursor.fetchone()[0]
                    if max_id is None:
                        max_id = 0

                    for x in range(ilosc_zap):
                        max_id = int(max_id + 1)
                        id_zamowienia = int(max_id)
                        data_zlozenia = faker.date_between(start_date=last_date, end_date='today')
                        last_date = data_zlozenia
                        koszt = round(random.uniform(10.0, 1000.0), 2)
                        pracownik_id_pracownik = random.randint(1, ilosc_zap)
                        klient_id_klient = random.randint(1, ilosc_zap)
                        status = random.randint(1, 3)

                        sql = f"INSERT INTO zamowienia (id_zamowienia, data_zlozenia, koszt, pracownik_id_pracownik, klient_id_klient,status_id_status) VALUES ({id_zamowienia},TO_DATE('{data_zlozenia.strftime('%Y-%m-%d')}', 'YYYY-MM-DD'), {koszt}, {pracownik_id_pracownik}, {klient_id_klient}, '{status}')"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli status, pracownik, klient")

            try:
                # insert relation1
                if jaka_tabela == "RELATION_1" or jaka_tabela == "Wszystkie":

                    for x in range(ilosc_zap):
                        magazyn_id_magazyn = random.randint(1, ilosc_zap)
                        towar_id_towar = x+1
                        sql = f"INSERT INTO relation_1 (magazyn_id_magazyn, towar_id_towar) VALUES ({magazyn_id_magazyn}, {towar_id_towar})"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli magazyn, towar")
            try:
                # insert relation10
                if jaka_tabela == "RELATION_10" or jaka_tabela == "Wszystkie":
                    for x in range(ilosc_zap):
                        zamowienia_id_zamowienia = random.randint(1, ilosc_zap)
                        towar_id_towar = x+1
                        sql = f"INSERT INTO relation_10 (zamowienia_id_zamowienia, towar_id_towar) VALUES ({zamowienia_id_zamowienia}, {towar_id_towar})"
                        pole = pole + sql + "\n"
                        print(sql)
                        cursor.execute(sql)
                    connection.commit()
            except:
                label.config(text="Najpierw dodaj dane do tabeli zamowienia, towar")

            with open("pliczek.txt", "w") as plik:
                plik.write(pole)
            print("ende")
            if label["text"] == "":
                label.config(text="Dane zostały wysałne")

        def on_select(event):
            value = lb.get(lb.curselection())
            entry.delete(0, tk.END)
            entry.insert(0, value)
            label.config(text="")

        def on_closing():
            cursor.close()
            connection.close()
            root.destroy()

        def delete_data():
            cursor.execute("DELETE FROM karta")
            cursor.execute("DELETE FROM relation_1")
            cursor.execute("DELETE FROM relation_10")
            cursor.execute("DELETE FROM towar")
            cursor.execute("DELETE FROM zamowienia")
            cursor.execute("DELETE FROM dzial")
            cursor.execute("DELETE FROM klient")
            cursor.execute("DELETE FROM adres")
            cursor.execute("DELETE FROM magazyn")
            cursor.execute("DELETE FROM pracownik")
            cursor.execute("DELETE FROM status")
            connection.commit()
            label.config(text="Dane zostały usunięte")
            print("Dane zostały usunięte")

        root = tk.Tk()
        root.title("Generator")
        root.geometry("800x600")

        listbox = tk.Listbox(root)
        lb = tk.Listbox(root, height=12, font=("Helvetica", 14))
        for table_name in table_names:
            lb.insert(tk.END, table_name)
        lb.pack(pady=10)

        entry = tk.Entry(root, width=30, font=("Helvetica", 14))
        entry.pack()

        num_rows_entry = tk.Entry(root, width=30, font=("Helvetica", 14))
        num_rows_entry.pack()

        button = tk.Button(root,width=30, text="Wybierz", command=on_click)
        button.pack(pady=10)

        delete_button = tk.Button(root, width=30, text="Usuń dane",command=delete_data)
        delete_button.pack(pady=10)

        label = tk.Label(root, text="", font=("Verdana", 14), fg="green")
        label.pack()

        lb.bind('<<ListboxSelect>>', on_select)

        root.mainloop()


