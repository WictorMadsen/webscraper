from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib

# Et program som leser igjennom en nettside og sender mail når det er spesifikke ord til stede.
# I dette tilfelle www.returbil.no og "Gardermoen". 
# www.returbil.no er dårlig kodet og det må derfor gjøres workarounds for å finne det man trenger i koden.

# find_city søker etter the_one og returnerer en liste med treff.
def find_city(soup,startDestination):
    result = []
    cols = soup.find_all("tr",attrs={"bgcolor": ("#DEE3E7","#EFEFEF")}) # Søker etter div-tagger med spesifikke farger.
    for col in cols:
        # children representerer radene i tabellen.
        children = list(col.contents)
        if len(children) > 8 and startDestination in children[5]:
            date = children[3].text.strip()
            fromCity = children[5].text.strip()
            toCity = children[7].text.strip()
            temp = "\n Ny bil \n"+date+" Fra: "+fromCity+" Til: "+toCity 
            result.append(temp)
    return result


def main():
    html = urlopen ("http://returbil.no/freecar.asp")
    soup = BeautifulSoup (html.read(), "html.parser")
    toAddress = "wictor.madsen@outlook.com"
    startDestination = "Gardermoen" 
    tempResult = find_city(soup,startDestination)
    result = "".join(tempResult)

    # Oppretting av informasjon rundt sending av mail med bruk av smtplib-modulen.
    if result:
        conn = smtplib.SMTP("smtp.gmail.com",587) #smtp adresse og port
        conn.ehlo() #starter connection
        conn.starttls() #tls kryptering på passord
        conn.login("wictor.madsen@gmail.com","djvsjzqpsazjomdm")
        conn.sendmail("wictor.madsen@gmail.com",toAddress,result)
        conn.quit()
        print("Sendt mail til",toAddress)
    else:
        print("Ingen ny, ledig bil fra",startDestination)
    

if __name__ == "__main__":
    main()

    