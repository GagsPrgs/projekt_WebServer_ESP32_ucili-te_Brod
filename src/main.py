import socket
import network
import time
from machine import Pin

try:
    from secrets import ssid, password
except Exception:
    ssid = 'TVOJ_SSID'
    password = 'TVOJA_LOZINKA'

# LED pin (on many ESP32 boards the on-board LED is on pin 2)
led = Pin(2, Pin.OUT)

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


def web_page():
    gpio_state = 'UKLJUCENA' if led.value() == 1 else 'ISKLJUCENA'
    html = """<html>
  <head>
    <meta charset='utf-8'/>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>ESP32 WiFi LED</title>
    <style>
      html { font-family: Helvetica, Arial, sans-serif; text-align:center; }
      h1 { color:#0F3376; }
      .button { display:inline-block; background:#e7bd3b; color:#000; padding:12px 28px; margin:8px; border-radius:6px; text-decoration:none; }
      .button.off { background:#4286f4; color:#fff; }
    </style>
  </head>
  <body>
    <h1>ESP32 WiFi LED</h1>
    <p>GPIO stanje: <strong>""" + gpio_state + """</strong></p>
    <p><a href='/?led=on' class='button'>UKLJUCI</a>
    <a href='/?led=off' class='button off'>ISKLJUCI</a></p>
  </body>
</html>"""
    return html


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
            print('Zahtjev:', req.split('\n')[0])

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


def main():
    sta = connect_wifi(ssid, password)
    if not sta:
        print('Nije moguće pokrenuti web server bez Wi-Fi veze.')
        return
    start_server()


if __name__ == '__main__':
    main()
