// Funzione per ottenere la data corrente formattata
function ottieniDataOggi() {
    let dataOggi = new Date();
    let giorno = dataOggi.getDate();
    let mese = dataOggi.getMonth() + 1; // I mesi sono indicizzati da 0, quindi aggiungiamo 1
    let anno = dataOggi.getFullYear();

    // Aggiungi uno zero iniziale al giorno e al mese se sono minori di 10
    if (giorno < 10) {
        giorno = '0' + giorno;
    }

    if (mese < 10) {
        mese = '0' + mese;
    }

    // Combina i valori in una stringa formattata
    return giorno + '/' + mese + '/' + anno;
}

// Funzione per aggiornare il contenuto del tag <p> con la data corrente
function aggiornaData() {
    document.getElementById('data').textContent = ottieniDataOggi();
}

// Aggiorna la data all'avvio della pagina
aggiornaData();
