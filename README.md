# Cornice Digitale

Cornice digitale smart basata su **Raspberry Pi**, sviluppata in **Python + Kivy**, progettata per funzionare come dispositivo dedicato sempre acceso, con avvio automatico e interfaccia full screen.

Il progetto nasce con l'obiettivo di realizzare una cornice fotografica da parete con slideshow animato, overlay informativi e integrazione con servizi esterni come **Google Calendar** e **Google Drive**, mantenendo un'architettura semplice, robusta e senza dipendere da un desktop environment completo.

---

## Caratteristiche del progetto

- esecuzione su **Raspberry Pi**
- applicazione sviluppata in **Python 3**
- interfaccia grafica realizzata con **Kivy**
- avvio automatico tramite **systemd**
- esecuzione senza desktop environment tradizionale
- architettura pensata per uso embedded / appliance
- cache locale per foto, configurazioni e dati calendario

---

## Stato attuale

Il progetto è già avviato e dispone di una base tecnica funzionante.

### Funzioni attualmente implementate

- avvio corretto dell'applicazione principale `main.py`
- test di rendering Kivy completati con successo
- esecuzione verificata sul Raspberry Pi
- predisposizione dell'ambiente Python tramite virtual environment
- installazione dei prerequisiti di sistema e delle dipendenze Python
- struttura del progetto già organizzata per dati, configurazioni e contenuti locali
- predisposizione all'avvio automatico tramite servizio `systemd`

In questa fase il focus è stato soprattutto sulla **messa in piedi dell'infrastruttura software**, sulla compatibilità del Raspberry Pi e sulla corretta esecuzione dell'applicazione in un ambiente minimale.

---

## Funzioni previste nella versione finale

La versione finale della cornice digitale includerà le seguenti funzionalità.

### Slideshow fotografico
- visualizzazione foto a schermo intero
- rotazione automatica delle immagini
- transizioni con dissolvenza
- effetto Ken Burns con zoom e movimento lento
- parametri configurabili per durata, zoom, pan e fade

### Overlay informativi
- data e ora in sovrimpressione
- visualizzazione dei prossimi appuntamenti
- eventuali messaggi o widget informativi

### Integrazione con Google Calendar
- sincronizzazione eventi da Google Calendar
- salvataggio locale degli eventi in JSON
- visualizzazione dei prossimi appuntamenti direttamente nella cornice

### Integrazione con Google Drive
- sincronizzazione automatica delle foto da una cartella cloud
- cache locale sul Raspberry Pi
- funzionamento anche offline con i contenuti già sincronizzati

### Interfaccia touch
- supporto touch screen
- accesso a menu e impostazioni
- attivazione/disattivazione di overlay e opzioni
- modifica rapida dei parametri principali

### Gestione contenuti locali
- archivio foto locale persistente
- fallback automatico in caso di assenza rete
- struttura dati semplice e facilmente manutenibile

### Importazione foto da USB
- rilevamento supporti USB
- importazione immagini nella libreria locale
- possibile procedura automatica o guidata

### Configurazione persistente
- file di configurazione separati dal codice
- salvataggio delle preferenze utente
- riapplicazione automatica delle impostazioni al riavvio

---

## Roadmap

### Fase 1 - Base tecnica
- [x] impostazione ambiente Python
- [x] installazione dipendenze
- [x] primi test Kivy
- [x] avvio applicazione sul Raspberry Pi
- [x] predisposizione esecuzione automatica

### Fase 2 - Viewer fotografico
- [x] caricamento immagini da directory locale
- [x] visualizzazione full screen
- [ ] rotazione automatica
- [ ] transizioni fade
- [ ] animazione Ken Burns

### Fase 3 - Overlay e UI
- [x] overlay data e ora
- [x] elementi grafici minimali
- [ ] supporto touch
- [ ] schermata impostazioni

### Fase 4 - Sincronizzazione esterna
- [ ] integrazione Google Calendar
- [ ] integrazione Google Drive
- [ ] gestione cache locale
- [ ] aggiornamento periodico dei dati

### Fase 5 - Funzioni accessorie
- [ ] importazione da USB
- [ ] gestione errori e recovery
- [ ] rifinitura grafica
- [ ] stabilizzazione finale per uso continuativo

---

## Struttura directory

Struttura logica prevista per il progetto:

```text
/opt/digital_frame/                  # codice applicativo
/var/lib/digital-frame/photos/       # archivio locale foto
/var/lib/digital-frame/calendar/     # eventi sincronizzati
/var/lib/digital-frame/config/       # configurazioni locali
```
