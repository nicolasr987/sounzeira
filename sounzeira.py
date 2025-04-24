from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from tkinter import Tk, filedialog, messagebox, simpledialog, Label, Entry, Button

def cortar_silencios(input_file, output_file, silence_threshold=-15.2, min_silence_len=550):
    try:
        audio = AudioSegment.from_file(input_file)

        chunks = split_on_silence(
            audio,
            silence_thresh=silence_threshold,
            min_silence_len=min_silence_len,
            keep_silence=500
        )

        combined = AudioSegment.empty()
        for chunk in chunks:
            combined += chunk

        combined.export(output_file, format="mp3")
        messagebox.showinfo("Sucesso", f"Arquivo processado salvo como '{output_file}'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo: {str(e)}")

def selecionar_arquivo():
    return filedialog.askopenfilename(
        title="Selecione o arquivo de áudio",
        filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.ogg *.flac")]
    )

def selecionar_pasta_saida():
    return filedialog.askdirectory(title="Selecione a pasta de saída")

def iniciar_interface():
    root = Tk()
    root.title("Ajustar Parâmetros de Corte de Silêncio")

    Label(root, text="Limiar de Silêncio (dBFS, ex: -15):").pack()
    entrada_threshold = Entry(root)
    entrada_threshold.insert(0, "-15")
    entrada_threshold.pack()

    Label(root, text="Duração Mínima do Silêncio (ms, ex: 500):").pack()
    entrada_min_len = Entry(root)
    entrada_min_len.insert(0, "550")
    entrada_min_len.pack()

    def processar():
        input_file = selecionar_arquivo()
        if not input_file:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
            return

        output_folder = selecionar_pasta_saida()
        if not output_folder:
            messagebox.showerror("Erro", "Nenhuma pasta de saída selecionada.")
            return

        try:
            threshold = float(entrada_threshold.get())
            min_len = int(entrada_min_len.get())
        except ValueError:
            messagebox.showerror("Erro", "Parâmetros inválidos.")
            return

        output_file = os.path.join(output_folder, "output.mp3")
        cortar_silencios(input_file, output_file, silence_threshold=threshold, min_silence_len=min_len)

    Button(root, text="Selecionar Áudio e Processar", command=processar).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
