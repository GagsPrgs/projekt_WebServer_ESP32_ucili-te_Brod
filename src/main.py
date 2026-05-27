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

# GPIO pin 2 je često povezan s ugrađenom LED diodom na ESP32 pločama.
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
    # Dinamičko određivanje stanja, klase statusa i klase za tipku UKLJUČI
    if led.value() == 1:
        gpio_state = 'UKLJUČENA'
        status_class = 'status-on'
        btn_on_class = 'btn-pure-blue'  # Kada je upaljena, tipka UKLJUČI je čista plava
    else:
        gpio_state = 'ISKLJUČENA'
        status_class = 'status-off'
        btn_on_class = 'btn-red'         # Kada je ugašena, tipka UKLJUČI je crvena
        
    html = """<html>
<head>
    <meta charset='utf-8'/>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>Kuća Prgomet - WiFi LED</title>
    <style>
      body { 
        font-family: system-ui, -apple-system, sans-serif; 
        text-align: center; 
        background-color: #0d0e12;
        background-image: 
          radial-gradient(circle at center, rgba(0, 68, 255, 0.12) 0%, transparent 65%),
          linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px),
          linear-gradient(0deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 100% 100%, 30px 30px, 30px 30px;
        color: #e2e8f0; 
        margin: 0; 
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
      }
      .container { 
        width: 100%;
        max-width: 380px; 
        padding: 40px 30px; 
        background: rgba(15, 17, 26, 0.75); 
        border-radius: 24px; 
        border: 2px solid #ef4444; 
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(239, 68, 68, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }
      .container:hover {
        transform: translateY(-4px);
        box-shadow: 0 24px 48px rgba(0, 0, 0, 0.9), 0 0 30px rgba(239, 68, 68, 0.35);
      }
      h1 { 
        color: #fff; 
        font-size: 26px; 
        font-weight: 700;
        margin: 0 0 8px 0; 
        letter-spacing: -0.5px;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
      }
      p { 
        font-size: 15px; 
        color: #94a3b8; 
        margin-bottom: 35px;
      }
      /* Osnovni stil za status značku */
      strong { 
        color: #fff; 
        padding: 5px 12px; 
        border-radius: 8px; 
        font-size: 13px; 
        font-weight: 700;
        text-transform: uppercase; 
        letter-spacing: 0.5px;
        margin-left: 6px;
        display: inline-block;
        transition: all 0.3s ease;
      }
      /* Dinamičke klase za pozadinu stanja */
      .status-on {
        background: #0044ff;
        color: #fff;
        box-shadow: 0 0 15px rgba(0, 64, 255, 0.6);
      }
      .status-off {
        background: #ef4444;
        color: #fff;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
      }
      .btn-group { 
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      /* Osnovni stil za tipke */
      .button { 
        display: block; 
        padding: 16px; 
        border-radius: 14px; 
        text-decoration: none; 
        font-weight: 700; 
        font-size: 15px; 
        letter-spacing: 0.5px; 
        transition: all 0.2s ease; 
        border: 1px solid rgba(255,255,255,0.1);
      }
      .button:active { 
        transform: translateY(1px); 
      }
      /* Klasa za Čistu plavu boju */
      .btn-pure-blue {
        background: #0044ff; 
        color: #fff; 
        box-shadow: 0 4px 15px rgba(0, 68, 255, 0.4);
      }
      .btn-pure-blue:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 68, 255, 0.7);
        background: #0033cc;
      }
      /* Klasa za Crvenu boju */
      .btn-red {
        background: #ef4444;
        color: #fff;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.25);
      }
      .btn-red:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.6);
        background: #dc2626;
      }
    </style>
  </head>
  <body>
    <div class='container'>
      <h1>Prgomet -WiFi-WebServer- LED</h1>
      <p>GPIO stanje: <strong class='""" + status_class + """'>""" + gpio_state + """</strong></p>
      <div class='btn-group'>
        <a href='/?led=on' class='button """ + btn_on_class + """'>UKLJUČI</a>
        <a href='/?led=off' class='button btn-red'>ISKLJUČI</a>
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
    
    try:
        while True:
            conn, addr = s.accept()
            request = conn.recv(1024)
            if not request:
                conn.close()
                continue

            req = request.decode('utf-8', 'ignore')
            print('Zahtjev:', req.split('\n'))

            if '/?led=on' in req:
                led.value(1)
            elif '/?led=off' in req:
                led.value(0)
                
            response = web_page()
            conn.send(b'HTTP/1.1 200 OK\r\n')
            conn.send(b'Content-Type: text/html; charset=utf-8\r\n')
            conn.send(b'Connection: close\r\n\r\n')
            conn.send(response.encode('utf-8'))
            conn.close()
            
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
