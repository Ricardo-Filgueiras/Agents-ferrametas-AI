import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app.user.models import Clientes, Documentos_clientes
from app.nova.models import InteractionSession, InteractionMessage
from app.nova.services import get_nova_ai_response

@login_required
def start_chat_from_doc(request, doc_pk):
    """
    Creates or retrieves a chat session for a specific document.
    Ensures that the client associated with the document belongs to the active user.
    """
    # Ensure document exists and belongs to client owned by current user
    documento = get_object_or_404(Documentos_clientes, pk=doc_pk, cliente__user=request.user)
    
    # Get or create the session
    session, created = InteractionSession.objects.get_or_create(
        cliente=documento.cliente,
        documento=documento
    )
    
    return redirect('nova:chat_session', session_id=session.id)

@login_required
def chat_session_view(request, session_id):
    """
    Renders the premium glassmorphic chat interface for the active session.
    Lists past message history and active context indicators.
    """
    # Ensure session belongs to client owned by current user
    session = get_object_or_404(InteractionSession, pk=session_id, cliente__user=request.user)
    messages = session.messages.all().order_by('created_at')
    
    # Retrieve other documents from the same client to let user switch if desired
    other_docs = Documentos_clientes.objects.filter(cliente=session.cliente, analise_ia=True).exclude(pk=session.documento_id if session.documento else None)
    
    context = {
        'session': session,
        'messages': messages,
        'other_docs': other_docs,
        'cliente': session.cliente,
        'documento': session.documento,
    }
    return render(request, 'nova/chat.html', context)

@login_required
@require_POST
def send_message_api(request, session_id):
    """
    AJAX endpoint to receive user messages and return AI responses in JSON format.
    Handles RAG logic asynchronously.
    """
    session = get_object_or_404(InteractionSession, pk=session_id, cliente__user=request.user)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except Exception:
        user_message = request.POST.get('message', '').strip()

    if not user_message:
        return JsonResponse({'status': 'error', 'error': 'A mensagem não pode ser vazia.'}, status=400)
        
    try:
        # Get AI response via Ollama RAG pipeline
        assistant_response = get_nova_ai_response(session, user_message)
        return JsonResponse({
            'status': 'success',
            'user_message': user_message,
            'assistant_response': assistant_response
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': f'Falha ao gerar resposta: {str(e)}'
        }, status=500)
