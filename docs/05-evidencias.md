# Seleção das evidências

**Autor:** Anderson Junior  
**Fontes:** fotos.zip e aff.zip, enviados pelo participante; organização em 25/11/2026.

Foram recebidos **24 PNGs**: 19 em fotos.zip e cinco em aff.zip. A seleção contém **13 imagens**: dez do primeiro ZIP e três do segundo, cobrindo ambiente, FTP, DVWA, SMB e uma dificuldade de inicialização. Os arquivos não receberam recortes, retoques ou alterações de conteúdo. O [manifesto](../images/manifesto.csv) registra o ZIP de origem, os nomes originais, as dimensões, o SHA-256 e as legendas; os hashes foram conferidos contra os respectivos arquivos recebidos.

## Imagens incluídas de fotos.zip

Neste ZIP, os nomes originais seguem o formato `Captura de tela 2026-11-23 HHMMSS.png`. O horário do nome identifica o arquivo e não substitui o relógio exibido na VM.

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

O arquivo `09-smb-spray.png` já inclui tanto ACCOUNT FOUND quanto o primeiro erro de assinatura RPC. O arquivo `10-smb-validacao.png` mostra a consulta posterior bem-sucedida. A numeração dos arquivos preserva os nomes anteriormente definidos; os intervalos não indicam arquivos perdidos da entrega. O arquivo `12-kernel-panic.png` é complementar e não comprova qual ajuste resolveu o boot.

## Imagens de fotos.zip não selecionadas

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

## Imagens do DVWA incluídas de aff.zip

Os nomes abaixo são os arquivos recebidos no segundo ZIP. O nome e a data de salvamento do arquivo não substituem o horário exibido dentro da VM.

| Nome recebido | Imagem no projeto | Finalidade |
| --- | --- | --- |
| Imagem do ChatGPT 25 de nov. de 2026, 15_24_32.png | [07a-dvwa-falha-manual.png](../images/07a-dvwa-falha-manual.png) | admin/123456 recusado; mensagem de erro e nível Low visíveis. |
| Imagem do ChatGPT 25 de nov. de 2026, 15_24_23.png | [07-dvwa-validacao.png](../images/07-dvwa-validacao.png) | admin/password aceito; mensagem da área protegida e nível Low visíveis. |
| Imagem do ChatGPT 25 de nov. de 2026, 15_24_06.png | [06-dvwa-tentativas.png](../images/06-dvwa-tentativas.png) | Duas falhas e sucesso na terceira candidata; erro anterior de entrada de PHPSESSID também preservado. |

As outras duas imagens de aff.zip mostram o formulário vazio nos níveis Low (`15_24_40.png`) e High (`15_24_46.png`). Foram mantidas fora da seleção porque não mostram resultados; a configuração Low aparece nas capturas de falha e sucesso. A configuração inicial High permanece descrita no relatório.

## Integridade e limites

As três imagens do DVWA estão incorporadas à seção correspondente do [relatório](03-relatorio.md). Nenhuma imagem foi reconstruída ou gerada para substituir evidência. Os logs brutos das VMs não foram recebidos.

Os hashes demonstram que as imagens selecionadas são idênticas às recebidas; não certificam por si só a autenticidade da execução. As senhas visíveis são credenciais públicas de laboratório. Não há evidência de aplicação de defesas ou reteste porque essas etapas não foram executadas.
