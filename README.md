# cifra-maker

Faz um arquivo PDF com as cifras coletadas.

## Descrição

No arquivo `main.py` tem uma lista de URLs de onde as cifras serão coletadas. O número à direita é a quantidade de semitons que o programa deve adicionar. Ex: no site está em **C** e você coloca o número 4, então o tom no arquivo PDF será **E**.

## Como executar
```bash
docker compose up --build
```

## Bugs conhecidos

- [ ] Onde era pra estar **Em** ficou **D##m**. Para reproduzir teste com estes dados: `('https://www.cifraclub.com.br/anjos-de-resgate-musicas/manda-teus-anjos/', 10),`
