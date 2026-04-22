import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self):
        # Configurações do ambiente
        self.model_llm = os.getenv("MODEL_LLM", "llama3.2:3b")
        self.model_emb = os.getenv("MODEL_EMBEDDING", "nomic-embed-text")
        
        # Inicialização dos componentes
        self.embeddings = OllamaEmbeddings(model=self.model_emb)
        self.llm = ChatOllama(model=self.model_llm, temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        self.vector_store = None
        self.chain = None

    def load_collection(self, collection_name):
        """Carrega documentos e constrói a chain usando LCEL"""
        path = f"data/collections/{collection_name}"
        if not os.path.exists(path):
            return False
        
        # Carregamento e Split
        loader = DirectoryLoader(
            path, 
            glob="**/*.md", 
            loader_cls=TextLoader, 
            loader_kwargs={'encoding': 'utf-8'}
        )
        docs = loader.load()
        if not docs:
            return False
        
        chunks = self.text_splitter.split_documents(docs)
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        # --- Construção da Chain usando LCEL (O padrão mais moderno) ---
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        template = """
        Você é o Docstóteles, um assistente especializado em documentações técnicas.
        Use os fragmentos de contexto abaixo para responder à pergunta de forma técnica e objetiva.
        Se não souber a resposta com base no contexto, diga apenas que não encontrou essa informação.
        
        CONTEXTO:
        {context}
        
        PERGUNTA: {question}
        
        RESPOSTA:
        """
        prompt = ChatPromptTemplate.from_template(template)

        # Padrão Pipe (|) - Evita dependência de langchain.chains
        self.chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return True

    def ask_question(self, question):
        """Executa a consulta na chain moderna"""
        if not self.chain:
            return "Selecione uma coleção primeiro."
        try:
            return self.chain.invoke(question)
        except Exception as e:
            return f"Erro na consulta: {str(e)}"
