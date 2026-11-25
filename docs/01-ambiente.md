# Montagem do laboratório

Este é um roteiro de reprodução. A configuração efetivamente observada, as diferenças e as dificuldades estão no [relatório](03-relatorio.md).

## Preparação

Use um computador Intel/AMD com virtualização habilitada e memória suficiente para as VMs. Como referência, reserve 4 GB para o Kali e 1 GB para o Metasploitable, ajustando ao hospedeiro. A VM do alvo observada tinha 2 GB. Metasploitable 2 é um sistema x86 antigo; em ARM pode exigir emulação ou adaptação.

Baixe pelas fontes oficiais:

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Kali para máquinas virtuais](https://www.kali.org/get-kali/#kali-virtual-machines)
- [Metasploitable 2 e instruções da Rapid7](https://docs.rapid7.com/metasploit/metasploitable-2/)

Registre versões, origem e hashes disponibilizados pelo fornecedor. A origem exata do disco usado no teste não foi confirmada.

## Configurar as VMs

Para a imagem pronta do Kali, extraia o arquivo baixado e adicione o arquivo .vbox no VirtualBox. Essa imagem não exige instalação por ISO. Revise RAM e CPUs. Confira as credenciais iniciais na documentação da versão.

Para Metasploitable 2, extraia o VMDK e crie uma VM Linux x86 compatível, usando o disco existente. Prefira o perfil Ubuntu 32-bit ou equivalente, uma CPU, BIOS legada e EFI desabilitado. O console observado mostrou i686, embora o Gerenciador exibisse um perfil Ubuntu 64-bit. O login padrão do laboratório é msfadmin/msfadmin.

Os erros antigos de kernel e IO-APIC estão documentados no relatório. Não há comprovação de qual ajuste resolveu definitivamente a inicialização; não se recomenda tratar um parâmetro isolado como solução garantida.

## Rede Host-only

1. Com as VMs desligadas, crie uma rede Host-only no gerenciador de redes do VirtualBox e habilite DHCP.
2. Conecte o Adaptador 1 de ambas à mesma rede Host-only, com o cabo virtual conectado.
3. Desabilite outros adaptadores durante os testes. Não configure Bridge ou encaminhamento de portas.
4. No hospedeiro, não habilite roteamento ou compartilhamento de Internet para esse segmento.

Host-only inclui o hospedeiro; Rede Interna conecta apenas as VMs selecionadas. Mantenha o firewall do hospedeiro e não compartilhe pastas pessoais com o alvo vulnerável.

Se faltarem ferramentas, use NAT temporariamente apenas no Kali, com o alvo desligado:

```bash
sudo apt update
sudo apt install medusa nmap enum4linux smbclient ftp python3
```

Depois remova/desabilite NAT antes de iniciar os testes. Os scripts publicados utilizam somente a biblioteca padrão do Python. Para registrar versões e módulos:

```bash
cat /etc/os-release
nmap --version
smbclient --version
python3 --version
medusa
medusa -d
medusa -M ftp -q
medusa -M smbnt -q
```

Medusa sem argumentos mostra o banner/ajuda. A opção -V não consulta a versão; ela controla mensagens e exige valor.

## Endereços e comunicação

No Kali:

```bash
ip -br a
ip route
```

No console do Metasploitable:

```bash
ifconfig
route -n
```

No laboratório observado, Kali usou 192.168.56.101/24 e Metasploitable 192.168.56.103/24. Confirme os endereços; o DHCP pode alterá-los. De volta ao Kali:

```bash
ping -c 3 192.168.56.103
```

Esse comando só deve usar .103 se ele continuar sendo o endereço confirmado do alvo. O ping do alvo para ele mesmo não comprova comunicação entre VMs. Ausência de resposta ICMP, sozinha, não prova ausência de serviços.

## DVWA e restauração

Abra http://192.168.56.103/dvwa/ no Firefox do Kali, ajustando o IP se necessário. Entre com as credenciais da imagem de laboratório, normalmente admin/password. Em DVWA Security, selecione Low e salve. Depois abra Brute Force.

O login inicial do DVWA e o formulário Brute Force são etapas diferentes: o exercício usa uma sessão já autenticada. Uma versão legada já vem no Metasploitable; não é preciso substituí-la pela versão atual.

Antes de novos testes, é recomendável criar snapshots com as VMs desligadas normalmente. A criação de snapshots não foi confirmada no estudo observado. Tire capturas próprias e registre os resultados reais, inclusive erros. Para encerrar, desligue as VMs pelo sistema convidado ou via ACPI e preserve os discos.
