from main import app
from flask import render_template, redirect, url_for, flash, request
from main.models import Prodotto, Utente, Acquisto
from main.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from main import db
# import classe login user
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_

# Route pagina home

@app.route('/')
@app.route('/home')
def home():
    #return render_template('home.html')
    return render_template('home.html')

# Route della pagina di acquisto
# lettura del DB e rendering nella pagina abilitazione di GET e POST

@app.route('/market', methods=['GET', 'POST'])

# Requisito del login per accedere al market

@login_required
def market():

    # Creazione del form per acquistare
    purchase_form = PurchaseItemForm()
    
    # Creazione form per rimozione prodotto dal carrello
    selling_form = SellItemForm()

    
    if request.method == "POST":

        control = 0 # Controllo caricamento e rilascio

        # Logica caricamento nel carrello

        purchased_item = request.form.get('purchased_item')
        p_item_object = Prodotto.query.filter_by(servizio=purchased_item).first()
        if p_item_object:
            control = 1  
            if current_user.can_purchase(p_item_object):
                p_item_object.carrello(current_user)
                flash(f"Aggiunto al carrello: {p_item_object.servizio} per {p_item_object.prezzo} Euro", category='success')
            else:
                flash(f"Superato il limite di acquisto !!! {p_item_object.servizio}!", category='danger')
        
       
        # Logica rimozione dei prodotti dal carrello
        sold_item = request.form.get('sold_item') # id del prodotto che voglio rilasciare

        if control==0:
            # Prodotto che proviene dal carrello
            prodotto_da_rilasciare = Prodotto.query.filter_by(id=sold_item).first() 

            # Aggiornamento totale
            current_user.budget -= prodotto_da_rilasciare.prezzo
            
            # Eliminazione del prodotto dal carrello    
            Acquisto.query.filter(
                and_(
                    Acquisto.prodotto_id == sold_item,
                    Acquisto.utente_id == current_user.id,
                    )
                ).delete()

            db.session.commit()  
  
            flash(f"Prodotto rilasciato e totale aggiornato", category='success')
            
        control=0
        return redirect(url_for('market'))


    # Filtro del carrello acquisizione prodotti nel carrello

    if request.method == "GET":
        items = Prodotto.query.all()

        #join delle tre tabelle per filtrare i prodotti nel carrello dell'id corrente

        query = db.session.query(Prodotto) \
            .join(Acquisto, Acquisto.prodotto_id == Prodotto.id) \
            .join(Utente, Utente.id == Acquisto.utente_id) \
            .filter(Utente.id == current_user.id)

        owned_items = query.all()

        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)
    

# Route di login dell'utente

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Verifica credenziali corrette
    if form.validate_on_submit():
        attempted_user = Utente.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Benvenuto! Utente loggato nel sistema: {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Nome utente e/o password sbagliati!', category='danger')

    return render_template('login.html', form=form)


# Route registrazione nuovo utente

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # Validazione dei dati corretta e registrazione dell'utente
    if form.validate_on_submit():
        utente_da_registrare = Utente(username=form.username.data,
                                     email_address=form.email_address.data,
                                     password=form.password1.data)
        db.session.add(utente_da_registrare)
        try:
          db.session.flush()
          # Se flush() non genera eccezioni, il record è stato salvato
          # ... codice per gestire il record salvato ...
        except Exception as e:
          # Se flush() genera un'eccezione, il record non è stato salvato
          # ... codice per gestire l'errore di salvataggio ...
          print("Errore durante la registrazione dell'utente.")
        db.session.commit()

        # Dopo la registrazione dell'utente appare la pagina di login
        return redirect(url_for('login'))
    
    if form.errors != {}: # Se vengono rilevati errori
        for err_msg in form.errors.values():
            flash(f'Errore nella creazione nuovo utente: {err_msg}', category='danger')
       
    
    return render_template('register.html', form=form)

# Route di logout dell'utente

@app.route('/logout')
def logout():
    logout_user()
    flash("Logout avvenuto correttamente!", category='info')
    return redirect(url_for("home"))