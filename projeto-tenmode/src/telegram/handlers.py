import logging
import os
import uuid
from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from src.agent.controller import AgentController
from src.media.pdf import PdfService
from src.media.audio import AudioService

logger = logging.getLogger(__name__)

router = Router()
controller = AgentController()

TMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tmp"))
os.makedirs(TMP_DIR, exist_ok=True)

@router.message(F.text)
async def process_text_message(message: Message):
    await _handle_input(message, message.text)


@router.message(F.document)
async def process_document_message(message: Message):
    doc = message.document
    if doc.mime_type == "application/pdf" or doc.file_name.endswith(".md"):
        file_ext = ".pdf" if doc.mime_type == "application/pdf" else ".md"
        local_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}{file_ext}")
        
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            try:
                # Download using aiogram
                await message.bot.download(doc, destination=local_path)
                
                # Extract text
                if file_ext == ".pdf":
                    extracted_text = PdfService.extract_text(local_path)
                else:
                    with open(local_path, "r", encoding="utf-8") as f:
                        extracted_text = f.read()

                final_text = message.caption or ""
                final_text += f"\n\n[System: Attached Document Context]\n{extracted_text}"
                
                await _handle_input(message, final_text.strip())
            except Exception as e:
                logger.error(f"Error processing document: {e}")
                await message.answer("⚠️ Falha ao ler o documento enviado.")
            finally:
                if os.path.exists(local_path):
                    os.remove(local_path)
    else:
        await message.answer("⚠️ No momento, só consigo processar texto estruturado (.md) e PDF.")


@router.message(F.voice | F.audio)
async def process_audio_message(message: Message):
    audio = message.voice or message.audio
    local_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.ogg")
    
    async with ChatActionSender.record_voice(bot=message.bot, chat_id=message.chat.id):
        try:
            # Download audio
            await message.bot.download(audio, destination=local_path)
            
            # STT Extraction
            transcription = await AudioService.speech_to_text(local_path)
            if not transcription or not transcription.strip():
                await message.answer("Áudio vazio ou ininteligível captado. Pode reenviar?")
                return
                
            # As per requirements, we append a system instruction indicating audio
            # reply preference because the user sent a voice clip
            final_text = transcription.strip()
            final_text += "\n\n[System Notification: The user sent this via Voice Note. Reply dynamically but preferably respond briefly, because your final response will be synthesized to Audio TTS.]"
            
            await _handle_input(message, final_text)
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            await message.answer("⚠️ Falha ao processar o áudio. Arquivo muito grande ou erro no serviço.")
        finally:
            if os.path.exists(local_path):
                os.remove(local_path)


async def _handle_input(message: Message, text: str):
    user_id = message.from_user.id
    
    if not text:
        await message.answer("Please send text or caption with media.")
        return

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        try:
            response = await controller.handle_user_input(str(user_id), text)
            
            MAX_LEN = 4000
            for i in range(0, len(response), MAX_LEN):
                chunk = response[i:i+MAX_LEN]
                try:
                    await message.answer(chunk, parse_mode="Markdown")
                except Exception as parse_err:
                    logger.warning(f"Markdown parse error: {parse_err}. Sending as plain text.")
                    await message.answer(chunk)
        except Exception as e:
            logger.error(f"Error handling input text: {e}")
            await message.answer("Ocorreu um erro interno ao processar sua requisição.")
