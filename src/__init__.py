from main_thread import MainThread

def __init__():

    mainThread = None

    while True:
        
        print ("""
        [1] Iniciar Sensores
        [2] Iniciar Amostragem
        [3] Finalizar Amostragem
        [4] Visualizar Amostra Corrente
        [5] Visualizar Configurações
        [6] Resetar Configurações Sensores
        [0] Sair
        """)

        option = input("Opção: ")

        if option == "0": 
            break
        
        if option == "1": 
            mainThread = MainThread()
            mainThread.startSensors()
            print("Sensores Iniciados")

        else:

            if mainThread is None:
                print("Sensores não iniciados.")

            elif option == "2":
                mainThread.startSampling()
                print("Amostragem iniciada.")

            elif option == "3":
                mainThread.stopSampling()
                print("Amostragem finalizada.")

            elif option == "4":
                mainThread.showSamplingCurrent()

            elif option == "5":
                mainThread.showSamplingSettings()

            else:
                print("Opção inválida.") 

if __name__ == "__main__":

    try:
        __init__()
    except KeyboardInterrupt:
        print("Exit")
