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



## Installation

## Montage