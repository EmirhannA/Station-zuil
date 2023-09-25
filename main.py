naam_reiziger = input("Put your name in?:")

if naam_reiziger =='':
    print("Anoniem")

message_gebruiker = input("What is your message?:")

if len(message_gebruiker) > 140:
    print("Error")
else:
    mijn_bestand = open("message.txt", 'a')
    mijn_bestand.write(naam_reiziger + ' ' + message_gebruiker)
    mijn_bestand.write("\n")
    mijn_bestand.close()