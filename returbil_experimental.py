from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib

# Et program som leser igjennom en nettside og sender mail når det er spesifikke ord til stede.
# I dette tilfelle www.returbil.no og "Gardermoen". 
# www.returbil.no er dårlig kodet og det må derfor gjøres workarounds for å finne det man trenger i koden.

# find_city søker etter the_one og returnerer en liste med treff.
def find_city(soup,the_one):
    result = []
    cols = soup.find_all("tr",attrs={"bgcolor": ("#DEE3E7","#EFEFEF")}) # Søker etter div-tagger med spesifikke farger.
    for col in cols:
        # children representerer radene i tabellen.
        children = list(col.contents)
        if len(children) > 8 and the_one in children[5]:
            date = children[3].text.strip()
            fromCity = children[5].text.strip()
            toCity = children[7].text.strip()
            temp = "\n Ny bil \n"+date+" Fra: "+fromCity+" Til: "+toCity 
            result.append(temp)
    return result

def write_message(filename,tempresult):
    fhand = open(filename,"r+")
    for line in fhand:
        for car in tempresult: #funker dette=
            if line == car:
                quit()
            else:
                #print("temp: ",temp)
                print("Car: ",car)
                fhand.write(car + "\n") #Skriver ikke til fil
    fhand.close()
    # Hvis det er en tilfeldig line, og en line == car, så skrives 3 nye car-lines til filen, og 3 mails blir sendt. 

def main():
    html = urlopen ("http://returbil.no/freecar.asp")
    soup = BeautifulSoup (html.read(), "html.parser")
    toAddress = "wictor.madsen@outlook.com"
    the_one = "Drammen" 
    filename = "returbil_arkiv.txt"
    
   # print(find_city(soup,the_one))
    tempresult = find_city(soup,the_one)
    write_message(filename,tempresult)
    result = "".join(tempresult)
    print(result)
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
        print("Ingen ny, ledig bil fra",the_one)
    

if __name__ == "__main__":
    main()






#Div: 
# http://androidideas.org/taskbomb/tutorials/running-a-script-every-5-minutes/
# Ikke sende samme resultat flere ganger. Skrive hvert funn til fil og sjekke i fil for hver linje om linje == result. Hvis ikke -> .append(result)
# Legge til input på dato
# Legge til input om destinasjon
# Legge til rettskriving-kontroll. Input = trndheim ligner på Trondheim osv.

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kwargs

    