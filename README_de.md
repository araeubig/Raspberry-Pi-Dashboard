# Über das Projekt

Da der Raspberry als Server im Verteilerschrank betrieben werden soll, benötigt er nicht nur ein DIN-Gehäuse, sondern auch ein Display, um die wichtigsten Systeminformationen anzeigen zu können. Ausserdem war die Anforderung den Raspberry über Knöpfe oder ein Touch-Display neustarten und herunterfahren zu können. Zuguterletzt soll der Raspberry nicht nur über PoE mit Strom versorgt werden, sondern auch einen M.2 Steckplatz für eine NVMe-SSD bieten - denn nur damit ist ein lanfristiger Betrieb - ohne mögliche Ausfälle der SD-Karte - möglich.

Die Suche nach den nötigen Komponenten gestaltete sich schwieriger als gedacht. Der Markt bietet nur wenige DIN-Gehäuse für den Raspberry Pi 5. Es gibt nur wenige Displays mit Touch-Option, die klein genug sind um in das Gehäuse zu passen. Das Angebot an kombinierten PoE-M.2 HATS ist überschaubar, aber mehr als ausreichend.

Während des Tests der möglichen Komponenten habe ich entschieden zwei Varianten für die Montage auf einer DIN-Schiene und eine weitere Variante für den Desktop-Einsatz zu dokumentieren:

1. Konfiguration mit 4TE breitem Gehäuse zur ausschliesslichen Stromversorgung über PoE
2. Konfiguration mit 6TE breitem Gehäuse zu optionalen Stromversorgung über 24V bzw. 220V
3. Konfiguration mit Stabndard-Gehäuse zu Stromversorgung über USB-Steckernetzteil ohne Touch Funktionalität

## Anforderungen

- Raspberry Pi 5
- Touch-Display welches in das DIN-Gehäuse passt (möglichst mit ST7789V2 Ansteuerung)
- 3D Druck des Deckels DIN-Gehäuse / Deckel des Standard-Gehäuses
- DIN-Gehäuse / Standard-Gehäuse
- Python >= 3.9

### Hardware

#### Gehäuse

##### DIN-Gehäuse

- [Waveshare DIN RAIL CASE Pi 5](https://www.waveshare.com/pi5-case-din-rail-b.htm)
    - Status: Getestet
    - Artikelnummer: 26682 / PI5-CASE-DIN-RAIL-B
    - Nutzung mit: Raspberry Pi 5
    - Grösse: 4TE
  
- [Italtronic MODULBOX XTS](https://eng.italtronic.com/accessori/25.0410000.RP5/) ! AKTUELL KEINE LÜFTUNGSÖFFNUNGEN
    - Status: Ungetestet
    - Artikelnumnmer: 25.0410000.RP5
    - Nutzung mit: Raspberry Pi 5
    - Grösse: 4TE

- [Phoenix Contact BC Serie](https://www.phoenixcontact.com/de-ch/produkte/elektronikgehaeuse/elektronikgehaeuse-fuer-raspberry-pi-anwendungen) ! AKTUELL NICHT FÜR RPi 5 OPTIMIERT
    - Status: Ungetestet
    - Artikelnumnmer: 2202874
    - Nutzung mit: Raspberry Pi 5
    - Grösse: 6TE

##### Standard-Gehäuse

- [Argon Neo 5 M.2 NVME](https://argon40.com/products/argon-neo-5-m-2-nvme-for-raspberry-pi-5)
    - Status: Ungetestet
    - Artikelnummer: -
    - Nutzung mit: Raspberry Pi 5
    - Grösse: Standard

#### Displays

#### HAT's

## Installation

## Montage

## Software