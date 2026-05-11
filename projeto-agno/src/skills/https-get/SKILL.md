---
name: "https-get"
description: "Esta skill verifica se a url é valida e retorna o conteudo. Funciona com urls http:// e https://"
---

#  Esta skill verifica se a url é valida e retorna o conteudo. 
#  Porem ela só funciona com urls http:// e https:// 

#  Ela recebe como parametro a url

E ela verifica se o ollama esta funcionando.

Buscando no browser pelo link: [http: ](http://localhost:11434/)

# HTTP GET SKILL

## USO

```powershell
uv run .\src\skills\https-get\scripts\get_http.py <url>
```

## EXEMPLO DE USO

```powershell
uv run .\src\skills\https-get\scripts\get_http.py http://localhost:11434/
```