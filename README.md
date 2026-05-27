# projekt_WebServer_ESP32_ucili-te_Brod

Thonny MicroPython web server projekt

## ESP32 WiFi LED — Jednostavan IoT projekt

Ovaj projekt sadrži jednostavan MicroPython web server za ESP32 koji upravlja jednim LED‑om preko web sučelja.

## Sadržaj
- `src/main.py`: Glavni program za ESP32
- `src/secrets.py`: Mjesto za `ssid` i `password`
- `images/`: Mapa za screenshotove iz Thonny i fotografije uređaja
- `.gitignore`: preporučene stavke za ignoriranje

## Kako koristiti
1. Otvorite `src/secrets.py` i unesite svoju Wi‑Fi mrežu:

```python
ssid = 'MOJ_SSID'
password = 'MOJA_LOZINKA'
```

2. Učitajte `src/main.py` i `src/secrets.py` na ESP32 koristeći Thonny ili drugi alat za MicroPython. Preporučeno ime datoteke na uređaju: `main.py`.

3. Pokrenite uređaj. U Thonny konzoli će se pokazati IP adresa uređaja (npr. `192.168.1.42`).

4. Otvorite tu adresu u pregledniku i kliknite gumbe za uključivanje ili isključivanje LED‑a.

## Foto dokumentacija
U mapi `images/` nalaze se screenshotovi iz Thonny, VSC-a, preglednika i GitHub-a koji dokumentiraju:

-Flashanje:

![Thonny prikaz spremanja firmwarea na ESP32](images/Thonny0.png)

![Thonny prikaz pokretanja uređaja nakon spremanja](images/Thonny1.png)

![Thonny prikaz terminala s porukama pokretanja](images/Thonny2.png)

![Thonny prikaz uspješnog spajanja uređaja](images/Thonny3.png)

-Spajanje:

![Thonny kod za spajanje na Wi-Fi](images/Thonny4.png)

![Thonny konzola s IP adresom uređaja](images/Thonny5.png)

![Unošenje WiFi SSID i password u Thonny](images/Thonny-unos.png)

![Thonny uspješno spajanje na Wi-Fi](images/Thonny-uspiješno%20spajanje.png)

-Izgled, upute, ostalo:

![Web sučelje ESP32 na desktopu](images/Web%20Server%20i%20ESP32.jpg)

![Web sučelje ESP32 na desktopu — druga varijanta](images/Web%20Server%20i%20ESP32%201.jpg)

![Web sučelje na mobitelu](images/Web%20Server%20Mob1.jpg)

![LED na uređaju — fotografija 1](images/Web%20Server-LED%20Na%20Ure%C4%91aju%201.jpg)

![LED na uređaju — fotografija 2](images/Web%20Server-LED%20Na%20Ure%C4%91aju.jpg)

![Web sučelje na mobitelu — varijanta](images/Web%20Server%20Mob.jpg)

![Postavljanje i pushanje na GitHub](images/Postavljanje%20i%20pushanje%20na%20GitHub.png)

![Snimka zaslona uređivanja i pripreme za push](images/Snimka%20zaslona%202026-05-27%20172331.png)

![Uređivanje u VSC i commit poruke](images/Ure%C4%91ivanje%20i%20ispravci%20u%20VSC-u,%20commitanja%20i%20pripreme%20za%20pushanje.png)

![Web server na desktop prikazu](images/Web%20Server-%20Desktop.png)

![Završni izgled web sučelja — AI dizajn 1](images/Završni%20izgled%20web%20sučelja%20izra%C4%91en%20uz%20pomo%C4%87%20AI-a%201.png)

![Završni izgled web sučelja — AI dizajn 2](images/Završni%20izgled%20web%20sučelja%20izra%C4%91en%20uz%20pomo%C4%87%20AI-a.png)



## Primjer Git naredbi

```bash
git init
git add .
git commit -m "Initial ESP32 WiFi LED project"
git branch -M main
git remote add origin <VAŠ_GIT_URL>
git push -u origin main
```

## Napomene za profesora
- Projekt koristi MicroPython i ESP32.
- Web server je jednostavan i demonstrira IoT upravljanje LED-om preko lokalnog Wi-Fi web sučelja.
- `src/secrets.py` držite s placeholder vrijednostima prije dijeljenja.
