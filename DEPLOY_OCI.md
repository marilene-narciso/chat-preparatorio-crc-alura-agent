# Checklist de Deploy na Oracle Cloud Infrastructure (OCI)

Este roteiro é um **checklist de planejamento** — nenhum comando aqui foi executado.
Ele serve para você seguir passo a passo quando estiver pronta para fazer o deploy de
verdade. Assume uma instância **OCI Compute** com **Ubuntu** (mais simples para
iniciantes; se escolher Oracle Linux, troque `apt`/`ufw` por `dnf`/`firewalld`, indicado
nos pontos onde isso importa).

**Nunca cole sua chave da API em nenhum lugar deste checklist, em comandos, ou em
qualquer arquivo que possa ir para o Git.** Ela só deve existir dentro do arquivo
`.env` na instância.

## Resumo (checklist rápido)

- [ ] Instância Compute criada na OCI (shape Always Free, imagem Ubuntu)
- [ ] Conexão SSH funcionando
- [ ] Python 3, `venv`, `pip` e `git` instalados na instância
- [ ] Repositório clonado do GitHub
- [ ] Ambiente virtual criado e `requirements.txt` instalado
- [ ] Arquivo `.env` criado na instância com `GOOGLE_API_KEY` preenchida
- [ ] Índice vetorial disponível (construído na instância ou copiado do seu computador)
- [ ] Aplicação testada manualmente dentro da instância (`streamlit run`)
- [ ] Porta liberada na regra de rede da OCI (Security List / NSG)
- [ ] Porta liberada no firewall do sistema operacional (se estiver ativo)
- [ ] Aplicação rodando de forma persistente (serviço systemd)
- [ ] Acesso público testado a partir do seu computador
- [ ] Print da aplicação funcionando salvo em `screenshots/`

---

## Fase 1 — Criar a instância Compute (console web da OCI, sem comandos)

1. No console da OCI: **Compute → Instances → Create Instance**.
2. Nome da instância (ex.: `chat-crc-agent`).
3. Imagem: **Canonical Ubuntu 22.04** (ou mais recente disponível no Always Free).
4. Shape: **VM.Standard.E2.1.Micro** (Always Free, arquitetura x86_64 — recomendado,
   porque é a mesma arquitetura usada em todos os testes locais deste projeto). A opção
   Ampere A1 (ARM) também é Always Free, mas como nunca testamos os pacotes do projeto
   em ARM, prefira x86_64 para evitar surpresas com pacotes sem versão pronta para essa
   arquitetura.
5. Adicione sua chave pública SSH (ou deixe a OCI gerar um par de chaves e baixe a
   chave privada — guarde-a com segurança, ela dá acesso à instância).
6. Crie a instância e anote o **IP público** gerado.

## Fase 2 — Conectar na instância via SSH

```bash
chmod 400 caminho/para/sua-chave-privada.pem
```
**O que faz:** ajusta a permissão do arquivo da chave privada para leitura só pelo seu
usuário. O SSH recusa se a chave estiver com permissão aberta demais.

```bash
ssh -i caminho/para/sua-chave-privada.pem ubuntu@SEU_IP_PUBLICO
```
**O que faz:** conecta ao terminal da instância remota, usando a chave privada. Em
imagens Ubuntu da OCI, o usuário padrão é `ubuntu`. Troque `SEU_IP_PUBLICO` pelo IP
anotado na Fase 1.

A partir daqui, todos os comandos rodam **dentro da instância** (via SSH), exceto onde
eu avisar o contrário.

## Fase 3 — Preparar o sistema

```bash
sudo apt update && sudo apt upgrade -y
```
**O que faz:** atualiza a lista de pacotes disponíveis e aplica atualizações de
segurança do sistema operacional.

```bash
sudo apt install -y python3 python3-venv python3-pip git
```
**O que faz:** instala o Python 3, o módulo para criar ambientes virtuais, o
gerenciador de pacotes `pip` e o `git` (necessário para clonar o repositório).

```bash
python3 --version
```
**O que faz:** confirma a versão do Python instalada. Ponto de atenção já vivido neste
projeto: versões muito novas do Python podem não ter pacote pronto para o
`cryptography` (uma das dependências), exigindo compilação. O projeto foi desenvolvido
e testado com Python 3.9; versões um pouco mais novas (3.10–3.12) tendem a funcionar
bem também.

## Fase 4 — Clonar o repositório do GitHub

```bash
git clone https://github.com/marilene-narciso/chat-preparatorio-crc-alura-agent.git
cd chat-preparatorio-crc-alura-agent
```
**O que faz:** baixa o código-fonte público do GitHub para dentro da instância e entra
na pasta do projeto.

## Fase 5 — Ambiente virtual e dependências

```bash
python3 -m venv venv
source venv/bin/activate
```
**O que faz:** cria um ambiente virtual isolado (`venv`) e o ativa, para as
dependências do projeto não se misturarem com pacotes do sistema operacional.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
**O que faz:** atualiza o instalador de pacotes e instala exatamente as dependências
necessárias para **rodar** a aplicação (use `requirements.txt`, não
`requirements-dev.txt` — o `pytest` não é necessário em produção).

## Fase 6 — Configurar a variável GOOGLE_API_KEY (sem expor a chave)

```bash
cp .env.example .env
```
**O que faz:** copia o modelo de configuração (sem valores reais) para um novo arquivo
`.env`, que é o único lugar onde a chave real deve existir.

```bash
nano .env
```
**O que faz:** abre um editor de texto simples no terminal para você preencher o
arquivo. Edite as duas linhas para ficarem assim (substituindo pela sua chave real,
só aqui dentro):

```
GOOGLE_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-flash-latest
```

No `nano`: `Ctrl+O` para salvar, `Enter` para confirmar, `Ctrl+X` para sair.

```bash
chmod 600 .env
```
**O que faz:** restringe a permissão do arquivo `.env` para que só o seu usuário na
instância consiga lê-lo.

```bash
git status
```
**O que faz:** confirma que o `.env` **não** aparece como algo pronto para commit (ele
já está no `.gitignore` do projeto) — uma checagem rápida de que a chave não corre o
risco de ser enviada ao GitHub por engano.

## Fase 7 — Base de conhecimento (índice vetorial)

O índice vetorial (`data/indice_vetorial/`) não vai para o GitHub (está no
`.gitignore`, pois é gerado a partir dos documentos). Duas opções:

**Opção A — deixar a aplicação construir o índice sozinha:** na primeira pergunta
feita na interface, o sistema lê os PDFs/CSV de `data/documentos/` e monta o índice
automaticamente. Mais simples, mas consome cota da API do Gemini e pode demorar
alguns minutos (já vivemos isso durante o desenvolvimento).

**Opção B (recomendada) — copiar o índice já pronto do seu computador:**

```bash
scp -i caminho/para/sua-chave-privada.pem -r data/indice_vetorial ubuntu@SEU_IP_PUBLICO:~/chat-preparatorio-crc-alura-agent/data/
```
**O que faz:** este comando roda no **seu computador** (não na instância). Copia a
pasta do índice vetorial já construído localmente para dentro da pasta `data/` da
instância, evitando reconstruir tudo do zero e economizando cota da API.

## Fase 8 — Testar a aplicação dentro da instância (antes de expor publicamente)

```bash
streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
```
**O que faz:** inicia a aplicação escutando na porta 8501, aceitando conexões de
qualquer endereço (`--server.address 0.0.0.0`) — sem isso, o Streamlit por padrão só
aceita conexões de dentro da própria máquina, e o tráfego externo nunca chegaria até
ela. Deixe rodando um instante para conferir que sobe sem erro (ex.: aviso de
`GOOGLE_API_KEY não encontrada` indicaria problema na Fase 6). Depois, `Ctrl+C` para
parar — esse é só um teste manual; a forma definitiva de rodar vem na Fase 10.

## Fase 9 — Abrir a porta (duas camadas de firewall)

### Camada 1 — Regra de rede da OCI (console web, sem comando de terminal)

1. **Networking → Virtual Cloud Networks → (sua VCN) → Security Lists** (ou
   **Network Security Groups**, se a instância usar um).
2. **Add Ingress Rules**:
   - Source CIDR: `0.0.0.0/0` (qualquer origem — necessário para acesso público de
     avaliação do Challenge; se quiser restringir, use seu próprio IP)
   - IP Protocol: `TCP`
   - Destination Port Range: `8501`
3. Salvar.

**Por que:** sem essa regra, mesmo com tudo certo dentro da instância, ninguém de fora
consegue alcançar a porta — a OCI bloqueia por padrão qualquer porta além da 22 (SSH).

### Camada 2 — Firewall do sistema operacional

```bash
sudo ufw status
```
**O que faz:** mostra se o firewall do Ubuntu (`ufw`) está ativo. Em muitas imagens
padrão da OCI ele vem desativado por padrão (a filtragem já é feita pela regra de rede
da Fase 9.1), mas é importante conferir.

Se aparecer "Status: active":
```bash
sudo ufw allow 8501/tcp
```
**O que faz:** libera a porta 8501 para conexões TCP no firewall do próprio sistema
operacional. *(Em Oracle Linux, o equivalente seria `sudo firewall-cmd --permanent --add-port=8501/tcp && sudo firewall-cmd --reload`.)*

## Fase 10 — Rodar a aplicação de forma persistente (systemd)

Se você rodar `streamlit run` direto no terminal SSH, a aplicação para assim que você
fechar a conexão. Para ficar no ar de verdade — inclusive sobrevivendo a reinícios da
instância — o recomendado é criar um serviço do sistema (`systemd`).

```bash
sudo nano /etc/systemd/system/chat-crc.service
```
**O que faz:** abre o editor para criar o arquivo de definição do serviço. Cole este
conteúdo (ajustando o caminho se o nome de usuário/pasta for diferente):

```ini
[Unit]
Description=Chat Preparatorio para Aprovacao do CRC
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/chat-preparatorio-crc-alura-agent
ExecStart=/home/ubuntu/chat-preparatorio-crc-alura-agent/venv/bin/streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
```
**O que faz:** avisa o `systemd` que um novo serviço foi definido.

```bash
sudo systemctl enable chat-crc
```
**O que faz:** configura o serviço para iniciar automaticamente sempre que a instância
ligar ou reiniciar.

```bash
sudo systemctl start chat-crc
```
**O que faz:** inicia a aplicação agora, rodando em segundo plano através do systemd
(continua rodando mesmo depois que você sair do SSH).

```bash
sudo systemctl status chat-crc
```
**O que faz:** mostra se o serviço está rodando corretamente — deve aparecer
`active (running)`.

```bash
sudo journalctl -u chat-crc -f
```
**O que faz:** mostra os logs da aplicação em tempo real — útil para diagnosticar
qualquer erro (ex.: chave de API ausente, porta ocupada). `Ctrl+C` para sair do modo
de acompanhamento (não derruba a aplicação).

## Fase 11 — Testar o acesso público

No navegador do **seu computador** (não da instância):

```
http://SEU_IP_PUBLICO:8501
```
**O que faz:** acessa a aplicação pelo IP público da instância. Se a tela "Chat
Preparatório para Aprovação do CRC" aparecer, o deploy funcionou.

Alternativa, pelo terminal do seu computador:
```bash
curl -I http://SEU_IP_PUBLICO:8501
```
**O que faz:** faz uma checagem rápida sem abrir navegador. Uma resposta com
`HTTP/1.1 200 OK` confirma que o servidor está respondendo publicamente.

## Fase 12 — Guardar evidência para o README

1. Tire um print da aplicação rodando pelo IP público, mostrando uma pergunta real e a
   resposta gerada.
2. Salve em `screenshots/` (ex.: `screenshots/deploy-oci.png`).
3. Depois, atualizamos as seções "Deploy na OCI" e "Evidência da Aplicação" do
   `README.md`, substituindo os marcadores `TODO` pela evidência real.

---

## Notas de segurança

- A chave da API nunca deve ser digitada em nenhum lugar além do arquivo `.env` na
  instância — nunca em comandos `git`, mensagens, ou arquivos versionados.
- Se algum dia desconfiar que a chave vazou, revogue-a em
  [aistudio.google.com/apikey](https://aistudio.google.com/apikey) e gere uma nova.
- A regra de rede `0.0.0.0/0` na porta 8501 expõe a aplicação a qualquer pessoa na
  internet — isso é esperado para o Challenge (avaliação pública), mas não coloque
  informações sensíveis na aplicação.
