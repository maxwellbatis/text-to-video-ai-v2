import edge_tts

async def generate_audio(text,outputFilename):
    # Usar velocidade mais lenta (-20%) para fala mais natural
    communicate = edge_tts.Communicate(text,"pt-BR-AntonioNeural", rate="-20%")
    await communicate.save(outputFilename)