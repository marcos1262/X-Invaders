import os

from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSound
from PyQt5.QtWidgets import QApplication


class Audio:
    """
    Responsável por tratar a parte de Áudio
    """

    def __init__(self, app: QApplication, jogo):
        self.jogo = jogo

        self.fundoJogo = "../sounds/fundo_jogo.mp3"
        self.fundoJogoDuracao = 208800

        self.fundoMenu = "../sounds/fundo_menu.mp3"
        self.fundoMenuDuracao = 67200

        self.musicPlayer = QMediaPlayer()
        app.lastWindowClosed.connect(lambda: self.musicPlayer.stop() or self.timerMusicaFundo.stop())

        self.timerMusicaFundo = QTimer()
        self.timerMusicaFundo.timeout.connect(self.toca_musica_fundo)

    def toca_musica_fundo(self):
        dir_raiz = os.getcwd() + "/"

        if self.jogo.iniciaJogo:
            arquivo = self.fundoJogo
            tempo = self.fundoJogoDuracao
        else:
            arquivo = self.fundoMenu
            tempo = self.fundoMenuDuracao

        url = QUrl().fromLocalFile(dir_raiz + arquivo)
        media = QMediaContent(url)

        self.musicPlayer.setMedia(media)
        self.musicPlayer.play()

        self.timerMusicaFundo.start(tempo)

    def toca_som(self, arquivo):
        QSound(arquivo, self.jogo).play()