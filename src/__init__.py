from sensors import Sensors

def __init__():

    sensors = None

    while True:
        
        print ("""
        [1] Iniciar Sensores
        [2] Iniciar Amostragem
        [3] Finalizar Amostragem
        [4] Visualizar Amostra Corrente
        [5] Resetar Sensores
        [0] Sair
        """)

        option = input("Opção: ")

        if option == "0": 
            break
        
        if option == "1": 
            sensors = Sensors()
            print("Sensores Iniciados")

        else:

            if sensors is None:
                print("Sensores não iniciados.")

            elif option == "2":
                sensors.start()
                print("Amostragem iniciada.")

            elif option == "3":
                sensors.stop()
                print("Amostragem finalizada.")

            elif option == "4":
                sensors.showCurrent()

            elif option == "5":
                sensors.reset()
                print("Configurações dos sensores resetadas.")

            else:
                print("Opção inválida.") 

if __name__ == "__main__":

    try:
        __init__()
    except KeyboardInterrupt:
        print("Exit")
