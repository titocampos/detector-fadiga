## Detector de Fadiga

Projeto do curso de Visão Computacional do [Sigmoidal](https://sigmoidal.ai/). Trata-se de uma aplicação prática de Visão Computacional e Aprendizado de Máquina. O programa desenvolvido é capaz de identificar sinais de fadiga em tempo real, como o fechamento prolongado dos olhos, a partir de um fluxo de vídeo. Nessa versão foi utilizado o detector de marcos faciais do pacote **mediapipe** para determinar a posição dos olhos e calcular a Relação de Aspecto dos Olhos (EAR). Quando a EAR está abaixo de um limiar definido durante um número específico de quadros consecutivos, o programa considera que a pessoa está com sinais de fadiga e aciona um alarme.

### Estrutura do Projeto 
A estrutura do projeto é a seguinte: 

    |-- arquivos/alarm.wav
    |-- src/main.py
    |-- src/detector.py 
    |-- src/utils.py 
    |-- src/requirements.txt


### Descrição dos arquivos:

- alarm.wav: som de alarme que será tocado quando sinais de fadiga são detectados. 
- main.py: script Python principal que contém a lógica da aplicação.
-  detector.py: script Python com a classe para uso do pacote mediapipe. 
- uteis.py: script Python com funções utilitárias. 
- requirements.txt: arquivo que lista as dependências necessárias para executar o programa.

### Referências Bibliográficas: 
SOUKUPOVA, Tereza; CECH, Jan. [Real-time eye blink detection using facial landmarks.](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf) In: 21st computer vision winter workshop, Rimske Toplice, Slovenia. 2016.
