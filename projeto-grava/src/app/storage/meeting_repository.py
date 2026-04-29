"""
MeetingRepository — acesso a dados de reuniões.

Encapsula toda leitura/escrita de arquivos de reunião,
desacoplando main.py dos detalhes de armazenamento.
"""
from pathlib import Path
from utils import le_arquivo, salva_arquivo, PASTA_ARQUIVOS


class MeetingRepository:
    """CRUD simples sobre pastas de reunião em data/."""

    def __init__(self, base_path: Path = PASTA_ARQUIVOS):
        self._base = base_path
        self._base.mkdir(exist_ok=True)

    # ── Listagem ────────────────────────────────────────────────────────────

    def listar(self) -> dict[str, str]:
        """
        Retorna dict {folder_name: label_formatado} ordenado mais recente primeiro.
        Compatível com a função listar_reunioes() de utils.py.
        """
        pastas = sorted(
            [p for p in self._base.glob("*") if p.is_dir()],
            reverse=True,
        )
        result = {}
        for pasta in pastas:
            stem = pasta.stem
            try:
                ano, mes, dia, hora, minuto, seg = stem.split("_")
                label = f"{ano}/{mes}/{dia} {hora}:{minuto}:{seg}"
            except ValueError:
                label = stem
            titulo = le_arquivo(pasta / "titulo.txt")
            if titulo:
                label += f" — {titulo}"
            result[stem] = label
        return result

    # ── Leitura ─────────────────────────────────────────────────────────────

    def pasta(self, reuniao_id: str) -> Path:
        return self._base / reuniao_id

    def titulo(self, reuniao_id: str) -> str:
        return le_arquivo(self.pasta(reuniao_id) / "titulo.txt")

    def transcricao(self, reuniao_id: str) -> str:
        return le_arquivo(self.pasta(reuniao_id) / "transcricao.txt")

    def resumo(self, reuniao_id: str) -> str:
        return le_arquivo(self.pasta(reuniao_id) / "resumo.txt")

    # ── Escrita ─────────────────────────────────────────────────────────────

    def salvar_titulo(self, reuniao_id: str, titulo: str) -> None:
        salva_arquivo(self.pasta(reuniao_id) / "titulo.txt", titulo)

    def salvar_transcricao(self, reuniao_id: str, texto: str) -> None:
        salva_arquivo(self.pasta(reuniao_id) / "transcricao.txt", texto)

    def salvar_resumo(self, reuniao_id: str, texto: str) -> None:
        salva_arquivo(self.pasta(reuniao_id) / "resumo.txt", texto)

    # ── Busca (para RAG futuro) ──────────────────────────────────────────────

    def todas_transcricoes(self) -> list[dict]:
        """Retorna lista de {id, titulo, transcricao} para indexação no FAISS."""
        result = []
        for pasta in self._base.glob("*"):
            if not pasta.is_dir():
                continue
            transcricao = le_arquivo(pasta / "transcricao.txt")
            if transcricao:
                result.append({
                    "id": pasta.stem,
                    "titulo": le_arquivo(pasta / "titulo.txt"),
                    "transcricao": transcricao,
                })
        return result
