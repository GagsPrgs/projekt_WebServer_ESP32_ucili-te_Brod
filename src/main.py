# ESP32 Wi-Fi LED Web Server

import socket
import network
import time
from machine import Pin

# Pokušaj učitati Wi-Fi podatke iz modula secrets.py, ako ne postoji, koristi zadane vrijednosti.
try:
    from secrets import ssid, password
except Exception:
    ssid = 'TVOJ_SSID'
    password = 'TVOJA_LOZINKA'

# GPIO pin 2 je često povezan s ugrađenom LED diodom na ESP32 pločama, ali provjeri dokumentaciju svoje ploče ako nisi siguran.
led = Pin(2, Pin.OUT)

# Funkcija za povezivanje na Wi-Fi mrežu s timeoutom.
def connect_wifi(ssid, password, timeout=15):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print('Povezivanje na Wi-Fi...')
        sta.connect(ssid, password)

        while not sta.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if sta.isconnected():
        print('Veza uspješna:', sta.ifconfig())
        return sta
    else:
        print('Wi-Fi nije povezan. Provjerite SSID i lozinku.')
        return None

# Funkcija za generiranje HTML stranice s trenutnim stanjem LED-a i gumbima za upravljanje.

def web_page():
    gpio_state = 'UKLJUĆENA' if led.value() == 1 else 'ISKLJUČENA'
    html = """<html>
<head>
    <meta charset='utf-8'/>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>ESP32 WiFi LED</title>
    <style>
      body { 
        font-family: system-ui, -apple-system, sans-serif; 
        text-align:center; 
        /* Fina tamnosiva podloga s radijalnim efektom sjaja u sredini */
        background-color: #12131a;
        background-image: 
          radial-gradient(circle at center, rgba(139, 38, 53, 0.15) 0%, transparent 70%),
          /* CSS uzorak paukove mreže / digitalne mreže poslužitelja */
          linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px),
          linear-gradient(0deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 100% 100%, 25px 25px, 25px 25px;
        color: #fca5a5; 
        margin:0; 
        padding:20px; 
      }
      .container { 
        max-width:400px; 
        margin:40px auto; 
        padding:30px; 
        /* Poluprozirna tamna kartica koja propušta uzorak mreže u pozadini */
        background: rgba(26, 27, 38, 0.85); 
        border-radius: 16px; 
        border: 2px solid #ef4444; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 15px rgba(239, 68, 68, 0.2);
        backdrop-filter: blur(4px);
      }
      h1 { color:#f87171; font-size:24px; margin-bottom:10px; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
      p { font-size:16px; color:#fca5a5; }
      strong { color:#fff; background:#ef4444; padding:4px 10px; border-radius:6px; font-size:14px; text-transform:uppercase; box-shadow: 0 0 8px rgba(239, 68, 68, 0.5); }
      .btn-group { margin-top:25px; }
      .button { display:inline-block; background:#2563eb; color:#fff; padding:14px 28px; margin:8px; border-radius:12px; text-decoration:none; font-weight:600; font-size:15px; letter-spacing:0.5px; transition:0.2s ease; box-shadow:0 4px 15px rgba(37,99,235,0.4); }
      .button:active { transform:scale(0.96); }
      .button.off { background:#dc2626; box-shadow:0 4px 15px rgba(220,38,38,0.4); }
    </style>
  </head>
  <body>
    <div class='container'>
      <h1>ESP32 WiFi LED</h1>
      <p>GPIO stanje: <strong>""" + gpio_state + """</strong></p>
      <div class='btn-group'>
        <a href='/?led=on' class='button'>UKLJUČI</a>
        <a href='/?led=off' class='button off'>ISKLJUČI</a>
      </div>
    </div>
  </body>
</html>"""
    return html

# Funkcija za pokretanje web servera koji je na portu 80 i obrađuje HTTP zahtjeve.

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('Web server pokrenut na', addr)
# Glavna petlja koja prihvaća dolazne HTTP zahtjeve, obrađuje ih i šalje odgovore. Također uključuje osnovno praćenje zahtjeva i rukovanje iznimkama.
    try:
        while True:
            conn, addr = s.accept()
            request = conn.recv(1024)
            if not request:
                conn.close()
                continue
# Dekodiranje HTTP zahtjeva i ispis prve linije (metoda i putanja) u konzolu radi praćenja.
            req = request.decode('utf-8', 'ignore')
            print('Zahtjev:', req.split('\n')[0])

            if '/?led=on' in req:
                led.value(1)
            elif '/?led=off' in req:
                led.value(0)
# Generiranje i slanje HTML stranice kao odgovora na HTTP zahtjev.  
            response = web_page()
            conn.send(b'HTTP/1.1 200 OK\r\n')
            conn.send(b'Content-Type: text/html; charset=utf-8\r\n')
            conn.send(b'Connection: close\r\n\r\n')
            conn.send(response.encode('utf-8'))
            conn.close()
# Rukovanje iznimkama koje mogu nastati tijekom rada web servera, poput problema s mrežom ili neispravnih zahtjeva, i zatvaranje socket veze u slučaju greške.  
    except Exception as e:
        print('Server error:', e)
    finally:
        s.close()
# Glavna funkcija koja povezuje na Wi-Fi i pokreće web server.
def main():
    sta = connect_wifi(ssid, password)
    if not sta:
        print('Nije moguće pokrenuti web server bez Wi-Fi veze.')
        return
    start_server()

# Pokretanje glavne funkcije kada se skripta izvrši.
if __name__ == '__main__':
    main()
