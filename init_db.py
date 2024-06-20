from main import app,db
from main.models import Prodotto

# Creazione e popoplamento del database
with app.app_context():
    if not db.inspect(db.engine).has_table('Prodotto'):
        db.create_all()
        serv1 = Prodotto(servizio="Perspiciatis", codice="7dc41462e51f", prezzo = 10, descrizione="Quis autem vel eum iure")
        serv2 = Prodotto(servizio="Millit Anim", codice="b131a4b9ebad", prezzo = 50, descrizione="Sed ut perspiciatis unde")
        serv3 = Prodotto(servizio="Voluptate", codice="e2a951d12241", prezzo = 150, descrizione="Duis aute irure dolor")
        serv4 = Prodotto(servizio="Magnam Aliquam", codice="525878e529dc", prezzo = 20, descrizione="Cursus eget dapibus ac")
        serv5 = Prodotto(servizio="Lamalesuada ", codice="c4daa3a2677c", prezzo = 100, descrizione="Duis non maximus mauris")
        db.session.add(serv1)
        db.session.add(serv2)
        db.session.add(serv3)
        db.session.add(serv4)
        db.session.add(serv5)
        db.session.commit()