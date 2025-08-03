#!/usr/bin/env python3
"""
Teste de Vozes Masculinas - Edge TTS
Lista e testa vozes masculinas disponíveis em português
"""

import asyncio
import edge_tts

async def list_voices():
    """Lista todas as vozes disponíveis"""
    voices = await edge_tts.list_voices()
    
    print("🎤 VOZES DISPONÍVEIS EM PORTUGUÊS:")
    print("=" * 60)
    
    portuguese_voices = []
    for voice in voices:
        if "pt-BR" in voice["ShortName"] or "pt-PT" in voice["ShortName"]:
            portuguese_voices.append(voice)
    
    for voice in portuguese_voices:
        gender = "👨 Masculina" if "Male" in voice["Gender"] else "👩 Feminina"
        print(f"🎤 {voice['ShortName']} - {gender}")
        print(f"   Nome: {voice['FriendlyName']}")
        print(f"   Idioma: {voice['Locale']}")
        print(f"   Gênero: {voice['Gender']}")
        print()
    
    return portuguese_voices

async def test_male_voice(voice_name, text="Olá, esta é uma voz masculina em português brasileiro."):
    """Testa uma voz masculina específica"""
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        output_file = f"test_{voice_name.replace('-', '_')}.wav"
        await communicate.save(output_file)
        print(f"✅ Voz testada: {voice_name} -> {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Erro ao testar {voice_name}: {e}")
        return None

async def main():
    """Função principal"""
    print("🎤 TESTE DE VOZES MASCULINAS - EDGE TTS")
    print("=" * 60)
    
    # Listar vozes
    voices = await list_voices()
    
    # Filtrar vozes masculinas
    male_voices = [v for v in voices if "Male" in v["Gender"]]
    
    print(f"\n🎯 ENCONTRADAS {len(male_voices)} VOZES MASCULINAS:")
    print("=" * 60)
    
    for voice in male_voices:
        print(f"🎤 {voice['ShortName']} - {voice['FriendlyName']}")
    
    # Testar vozes masculinas
    print(f"\n🧪 TESTANDO VOZES MASCULINAS:")
    print("=" * 60)
    
    for voice in male_voices:
        await test_male_voice(voice["ShortName"])
    
    print("\n✅ TESTE CONCLUÍDO!")

if __name__ == "__main__":
    asyncio.run(main()) 