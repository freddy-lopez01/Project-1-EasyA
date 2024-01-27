def log_input(message, file):
    with open(file, 'a') as log_file:
        log_file.write(message + '\n')

def main():
    log_input("Script started.", "miseryReel.txt")
    user_name = input("Please enter your name: ")
    log_input(f"User name: {user_name}", "miseryReel.txt")

    miffed_up = input("You must be here because you done miffed up? y/n: ")
    if miffed_up.lower() == 'y':
        reason = input("Please state the reason: ")
        log_input(f"Reason for miffed up: {reason}", "miseryReel.txt")

    rebase_db = input("Do you need to rebase the database? y/n: ")
    if rebase_db.lower() == 'y':
        year = input("Enter the year (14 or 16): ")
        if year == '14':
            with open("FacData.txt", 'w') as fac_file:
                with open("Facdata1415.txt", 'r') as data_file:
                    fac_file.write(data_file.read())
            log_input("Overwrote FacData.txt with Facdata1415.txt", "miseryReel.txt")
            with open("url.txt", 'w') as url_file:
                url_file.write("url14.txt")
            log_input("Overwrote url.txt with url14.txt", "miseryReel.txt")
        elif year == '16':
            with open("FacData.txt", 'w') as fac_file:
                with open("Facdata1516.txt", 'r') as data_file:
                    fac_file.write(data_file.read())
            log_input("Overwrote FacData.txt with Facdata1516.txt", "miseryReel.txt")
            with open("url.txt", 'w') as url_file:
                url_file.write("url16.txt")
            log_input("Overwrote url.txt with url16.txt", "miseryReel.txt")
        else:
            print("Invalid year.")
            log_input("Invalid year entered.", "miseryReel.txt")
    elif rebase_db.lower() == 'n':
        need = input("What do you need then? ")
        log_input(f"User needs: {need}", "miseryReel.txt")
        print("THIS is a LIFELINE not a LIFEBOAT. you are SOL here. : |")
    else:
        print("Ok suit yourself struggle in the backrooms then.")

if __name__ == "__main__":
    main()