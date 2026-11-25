# Seleção das evidências

**Autor:** Anderson Junior  
**Fonte:** fotos.zip, enviado pelo participante; organização em 25/11/2026.

Dos **19 PNGs recebidos**, foram incluídas **nove evidências principais e uma complementar**. Os arquivos não receberam recortes, retoques ou alterações de conteúdo. O [manifesto](../images/manifesto.csv) registra nomes originais, dimensões, SHA-256 e legendas; os hashes foram conferidos contra o ZIP.

## Imagens incluídas

Todos os nomes originais seguem o formato `Captura de tela 2026-11-23 HHMMSS.png`. O horário do nome identifica o arquivo e não substitui o relógio exibido na VM.

| Horário no nome original | Imagem no projeto | Finalidade |
| --- | --- | --- |
| 133809 | [00-rede-host-only.png](../images/00-rede-host-only.png) | Configuração do alvo com adaptador Host-only. |
| 140248 | [01-meta-ip.png](../images/01-meta-ip.png) | IPv4 do Metasploitable: 192.168.56.103/24. |
| 140957 | [02-kali-conectividade.png](../images/02-kali-conectividade.png) | Kali 192.168.56.101/24 e ping para o alvo com três respostas. |
| 141346 | [03-nmap-servicos.png](../images/03-nmap-servicos.png) | Nmap: portas 21, 80, 139 e 445 abertas. |
| 141625 | [04-ftp-medusa.png](../images/04-ftp-medusa.png) | Medusa FTP: ACCOUNT FOUND para msfadmin/msfadmin. |
| 142527 | [05-ftp-validacao.png](../images/05-ftp-validacao.png) | Login FTP confirmado e diretório /home/msfadmin. |
| 145343 | [08-smb-enumeracao.png](../images/08-smb-enumeracao.png) | Enumeração com msfadmin, service e ftp. |
| 150539 | [09-smb-spray.png](../images/09-smb-spray.png) | Spraying SMB com sucesso e primeira consulta RPC com BAD SIG. |
| 150950 | [10-smb-validacao.png](../images/10-smb-validacao.png) | RPC: Account Name msfadmin; Authority Name VULNERABILITY. |
| 131009 | [12-kernel-panic.png](../images/12-kernel-panic.png) | Registro complementar de kernel panic na preparação. |

A captura 09 já inclui tanto ACCOUNT FOUND quanto o primeiro erro de assinatura RPC. A captura 10 mostra a consulta posterior bem-sucedida. A numeração preserva os nomes anteriormente definidos; os intervalos não indicam arquivos perdidos da entrega. A captura 12 é complementar e não comprova qual ajuste resolveu o boot.

## Imagens descartadas

| Horário no nome original | Motivo |
| --- | --- |
| 125130 | Tela Starting up sem resultado final. |
| 125811 | Edição intermediária do GRUB, sem confirmação da configuração final. |
| 130024 | Mensagens intermediárias de inicialização. |
| 133732 | Referência em vídeo com botão de reprodução, não evidência da execução do participante. |
| 133822 | Outra captura da mesma referência em vídeo. |
| 134024 | Kernel panic repetido; uma única captura documenta a dificuldade. |
| 140049 | Login e comandos de rede incorretos; a saída posterior de ifconfig é mais útil. |
| 140653 | Ping do Metasploitable para si mesmo; não comprova comunicação entre VMs. |
| 142224 | FTP aguardando usuário; a imagem posterior mostra o login concluído. |

## DVWA e limites

Os prints do DVWA foram vistos anteriormente na conversa, mas **não estão no ZIP recebido**. O relatório preserva os resultados transcritos e informa essa ausência. Não foram criadas imagens substitutas nem links para arquivos inexistentes.

Se os originais forem localizados, os nomes previstos são `06-dvwa-tentativas.png`, `07-dvwa-validacao.png` e, opcionalmente, `07a-dvwa-falha-manual.png`. Acrescente os arquivos e links antes de mudar o aviso de ausência.

Os hashes demonstram que as imagens selecionadas são idênticas às recebidas; não certificam por si só a autenticidade da execução. As senhas visíveis são credenciais públicas de laboratório. Não há evidência de aplicação de defesas ou reteste porque essas etapas não foram executadas.
