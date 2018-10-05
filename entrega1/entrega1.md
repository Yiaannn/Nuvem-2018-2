# Computação em Nuvem

## Bare Metal

### Grupo
* #### Alexandre Young
* #### Paulo Tozzo

***

## Material

### 1. Como foi feito para identificar as NUCs corretamente sem um sistema operacional?

Para identificar os NUCs, a estratégia tomada foi a de procurar as informações relevantes na BIOS dos sistemas.

Primeiro conectou-se o NUC a um display HDMI e a um teclado wireless via USB, durante o boot acessou-se o painel principal de controle da BIOS pela tecla F2.

Uma vez na BIOS, a informação sobre a quantidade de memória disponível foi encontrada no menu *Main*, dentro da aba *Memory Information*, a informação quanto ao endereço MAC foi encontrada no menu *Devices*, no submenu *Add-In Config* em que um dos dispositivos listados tinha o nome *Intel(R) Ethernet Connection I219-LM XX:XX:XX:XX:XX:XX*, que revela o endereço MAC do dispositivo ethernet do NUC.

Um dos NUCs é diferente que os outros, aquele identificado como *MaaS*, sua BIOS tradicional apresentou a memória no menu principal *Main*, no item *Total Memory*, e o endereço MAC do dispositivo ethernet no item *LAN MAC Address*.

***

## Rede

### 1. Quais IPs são fixos e quais são flutuantes? Qual a subrede?

A subrede é aquela isolada pelo roteador agindo como gateway, Em que os IPs flutuantes são aqueles que os NUCs utilizam para se conectar ao roteador, e o fixo são o do roteador que mantém seu IP para poder aceitar novos hosts dentro da sua rede e o do switch, que também tem um IP fixo que precisa ser alterado manualmente.

### 2. Existe um DHCP server na sua rede? Aonde?

Existe um servidor DHCP providenciado pelo roteador. Quando ligado ao switch o roteador faz pelo DHCP um broadcast procurando por dispositivos interessados em se conectar à rede, que é capaz de atingir as NUCs através do switch.

### 3. Existe um DNS server na sua rede? Aonde?

Existe um DNS utilizado internamente, quando inicializado o roteador busca uma lista DNS da rede externa, que é utilizado como DNS interno. Na prática, o DNS utilizado é aquele associado à rede do Insper, a subnet criada apenas copia esse mesmo DNS.

### 4. Existe um gateway? Aonde?

Sim! O roteador age como um gateway ao interfaceiar com as duas redes (a do Insper e a subnet criada), sendo capaz de endereçar cada NUC por um IP independente associado.

### 5. Qual a topologia da sua rede?

Funcionalmente, ela está estruturada como uma estrela, com o roteador como o centro da subnet, servindo cada dispositivo (os NUCs) isolados entre sí.

Na teoria, a rede também apresenta características de BUS dizendo respeito à capacidade de cada NUC endereçar outro pelo switch, mas essa é mais uma observação sobre a capacidade de endereçamento do switch que uma análise da rede montada de fato.

***

## Lapidando o projeto

### 1. Quantos IPs utilizáveis estão disponíveis na subrede 192.168.0.0/20? Todos os IP são utilizáveis?

Estão disponíveis 4094 IPs, a nomenclatura __*x.x.x.x/20*__ indica que 20 dos 32 bits disponíveis em IPv4 são fixos na subrede e os 12 bits finais podem ser usados para configurar um IP, totalizando 4096 possibilidades, no entanto existem dois valores reservados que não podem ser utilizados normalmente, o IP na rede, em que os 12 bits finais são todos 0 e o IP de broadcast, em que os 12 bits finais são todos 1.

### 2. Qual a diferença entre um IP público e um IP privado?

Um IP público é aquele utilizado no nível mais alto de rede para se comunicar diretamente com a internet e o qual pode ser usado para se comunicar com outros IPs públicos arbitrários. IPs privados são aqueles que não são diretamente visíveis da internet, como por exemplo os IPs de uma subrede. A comunicação de IPs privados com a Internet ainda pode ocorrer, mas não diretamente, é necessário a passagem por um gateway conectado diretamente à ela.

### 3. Qual a classe utilizada na rede interna do Insper? E na sua rede? Quantas classes existem?

A rede do Insper aparenta ser uma rede de classe B, dada que sua máscara de subrede é 255.255.0.0. Nossa rede é mista entre B e C dado que o name field do nosso network ocupa 20 bits, entre os 16 do B e os 24 do C. existem 4 classes definidas, (A, B, C e D, da qual a D é para networking em multicast) e uma reservada (E).

***

## MaaS

### 1. Descreva como foram evitados ou resolvidos os problemas de roteamento e resolução de nomes.

Para configurar um IP estático para o maas, um arquivo que representa as opções de configuração de rede do sistema __*/etc/netplan/01-netcfg.yaml*__ foi editado. Nesse arquivo adicionou-se a chave __*addresses: - 192.168.0.3*__ para configurar o IP estátitco assim como __*gateway4: 192.168.0.1*__ para que encontre o IP do roteador que age como gateway.

Como uma garantia adicional, configurou-se nas opções internas do roteador a opção de só servir IPs automáticos a partir do IP *192.168.0.4* para evitar possívveis conflitos futuros.

Após essas configurações, testou-se os pings listados no roteiro depois de um reboot frio, os quais ocorreram com sucesso, salvo uma adaptação sugerida pelo professor Eduardo de substituir o teste pelo *maas.maas* por apenas *maas*, pelo motivo de que um domínio não seria necessário para a nossa aplicação.

***

## Chaveando o DHCP

### Por que Desabilitar o do roteador?

A intenção das ações tomadas até esse ponto são de implementar nossa própria subnet, entendo as partes que compõe o sistema, a intenção do uso do roteador no sistema é que ele sirva apenas como um gateway para a rede externa, enquanto o MaaS de fato faça o roteamento da rede. Dessa forma, faz sentido na nossa disposição que o DHCP seja servido pelo MaaS e não pelo roteador.

Ter dois servidores DHCP ativos na rede poderia causar inconsistências, o DHCP do roteador agiria como um servidor rogue, atribuindo IPs fora do controle do MaaS.

### Como funciona o ataque *DHCP rogue*? Como evitar?

Um ataque DHCP Rogue é aquele em que existe um servidor DHCP na subnet não-legítimo (por isso _Rogue_) servindo IPs fora do controle da máquina esperada (podendo causar colisões entre IPs dentro da rede derrubando usuários legítimos) e também potencialmente apontando as máquinas clientes a gateways ilegítimos com a intenção de realizar ataques man-in-the-middle ou similares para capturar data maliciosamente.

Pode-se evitar essa forma de ataque por meio de um monitor intermediário na comunicação entre a rede (por exemplo um switch) capaz de scanear e bloquear os packets de um tráfego DHCP ilegítimo (ou seja, que não é servido por uma máquina validada). Essa estratégia de defesa chama-se de *DHCP Snooping*.
***

## Comissioning nodes

### 1. Descreva o processo PXE Boot? Qual a sua grande vantagem em um datacenter real?

PXE Boot, do nome *Preboot Execution Environment* refere ao processo de realizar um boot seguindo um standard em que máquinas client recebem imagens pré-configuradas de um servidor, eliminando o necessidade de que seja instalada uma imagem na máquina cliente.

A vantagem de tal processo vem da capacidade de servir em escala massiva imagens de inicialização padronizadas, fáceis de controlar e versionar e sem precisar de manutenção direta passando por máquina a máquina realizando um processo convencional de instalação por mídia física, como por meio de um CD ou drive USB de instalação.

### 2. Analisando em um aspecto mais amplo, quais outras funcionalidades do MaaS pode ser útil no gerenciamento de bare metal?

Algumas das funcionalidades adicionais que poderiam ser usadas para manejar o Bare Metal são: A suíte completa de Hardware Testing, capaz de validar a integridade da memória RAM ou a conectividade das interffaces de rede das máquinas clientes. E Controle direto de disposições mais complexas de storage ( como RAID ).

***

## Finalizando a rede para acesso "externo"

### 1. Qual o nome e como funciona a ferramenta utilizada?

A ferramenta utilizada para redirecionar o tráfego HTTP e SSH para a máquina do MaaS foi a de *Port Forwarding*, em que como o nome implica, tráfego que atinge um gateway por portas específicas são redirecionados na subnet para uma máquina específica. Em outras palavras, *Port Forwarding* permite que uma máquina fora da subnet pode se comunicar "diretamente" com uma máquina da subnet pelo IP do gateway em determinadas portas.

### 2. O que deveria ser feito para você conseguir acessar o Maas da sua casa?

Seria necessário que o gateway mais externo do Insper tivesse regras habilitadas de *Port Forwarding* que redirecionasse o tráfego HTTP e SSH para o gateway da subnet do MaaS, seria necessário também que o gateway da subnet do MaaS tivesse as regras habilitadas para redirecionar o tráfego para a máquina do MaaS.

***

## Questões Complementares

### 1. O que significa LTS? Por que isso importa para uma empresa?

LTS, do inglês Long Term Support, são releases voltados à manutenção e uso a longo-termo com alguma espécie de garantia pelo distribuidor. Mais especificamente para o caso de um sistema operacional, um release LTS é voltado a manter a estabilidade e segurança do sistema acima do interesse de adicionar features novos no sistema que poderiam potencialmente introduzir falhas desconhecidas no sistema.

### 2. O que é IPv6? Qual a importância da migração?

IPv6 é um protocolo de Internet (literalmente a sigla IP) cuja principal distinção em relação ao protocolo atualmente utilizado, o IPv4, é a quantidade de endereços IPs máximos disponíveis em uma mesma rede. Atualmente em IPv4 temos 4*8 bits disponíveis para endereçamento, os quais possibilitariam cerca de 4 bilhões de endereços possíveis (descontando IPs reservados para usos específicos como broadcast ou loopback), ainda assim, existe a possibilidade real da eventual exaustão dos endereços disponíveis com a quantidade de dispositivos conectados à Internet ao considerarmos quantos celulares, computadores e outros dispositivos inteligentes existem e serão criados no futuro próximo,

### 3. A literatura preconiza que o Modelo de Rede Internet possui 5 camadas, quais são elas e quais camadas foram envolvidas nesse capítulo?

As camadas são do menor nível para o maior nível:
* Física
* Data Link
* Internet
* Transporte
* Aplicação

Neste capítulo trabalhamos diretamente na camada mais baixa do modelo, a camada Física.

### 4. A literatura mais antiga discorre sobre o Modelo de Rede OSI de 7 camadas. Explique a diferença entre os dois modelos.

O Modelo OSI separa a rede em mais camadas mais "granuladas" que no Modelo de Rede Internet, as quais são do menor nível para o maior nível:
* Física
* Data Link
* Network
* Transporte
* Sessão
* Apresentação
* Aplicação

As camadas de Sessão e Apresentação não tem uma equivalência direta no Modelo de Rede Internet, nele eles são entendidos como parte da camada de Aplicação. O uso do Modelo de Rede Inter sobre o modelo OSI acontece porque essa distinção adicional é considerada pouco interessante para o estudo de networking geral.

***

## Concluindo

### 1. O que é e para que serve um gerenciador de Bare Metal?

Serve para, de uma forma escalável, manejar diversas máquinas dentro de um datacenter de forma escalável e semiautomática, manejando o boot, inicialização e conexão das máquinas associadas e ele.

### 2. O que é um MAC address?

MAC addres (Media Access Control address) é um endereço identificador para um hardware que (em tese) deveria ser único e imutável. Esse endereço pode ser usado por exemplo para identificar uma máquina específica dentro de uma rede quando se deseja atribuir um IP específico a ela.

### 3. O que é um IP address? Como ele difere do MAC address?

O endereço IP, diferentemente do MAC, é um endereço que não é absoluto para a máquina, ela depende do contexto de uma rede e pode ser mudado com frequência. Esse é o endereço utilizado para se comunicar com outro dispositivos dentro de uma rede e identificá-los.

### 4. O que é CIDR? Qual o papel da subrede?

CIDR (Classless Inter-Domain Routing) é a forma usada atualmente de definir como está estruturada a disponibilidade de endereços IPs dentro de uma subnet, separando os bits destinados aos hosts dos bits que descrevem o network. Ela substituí a denominação classful de rede (A a D) usada também para descrever o endereçamento de networks.

Por exemplo, na rede construída no roteiro, foi utilizado uma rede cujo endereço CIDR é *192.168.0.0/20*, o que significa que os 20 primeiros bits são fixos no nome da rede e os demais 12 estão disponíveis para serem usados por hosts que pertencem à rede.

### 5. O que é são DHCP, DNS e gateway?

DHCP, Dynamic Host Configuration Protocol é o servidor destinado a servir IPs válidos para máquinas que querem se conectar a uma determinada rede.

DNS, Domain Name Server é um nome mnemônico associado a um IP dentro de uma determinada rede. Por exemplo, o nome de servidor __*Insper.edu.br*__ é associado ao IP *186.232.61.148*

Gateway é o dispositivo responsável em um network a se comunicar com uma rede externa, comunmente em redes domiciliares usam-se roteadores que, entre outros papéis, assume também o papel de gateway.

***

## Conclusão

### Descreva como o MaaS poderia ser utilizado em um datacenter real (com muitos servidores) e como seria um processo alternativo sem essa ferramenta. Ainda, é possível e SIMPLES realizar a implantação de uma aplicação usando o MaaS?

O MaaS pode ser utilizado, como foi observado durante este roteiro, para gerenciar não só o versionamento dos sistemas operacionais contido nas máquinas de um datancenter, mas também o seu boot e gerenciar a integridade desses hardwares. Sem um gerenciador em larga-escala como MaaS seria necessário manejar cada máquina individualmente ou utilizar algum outro gerenciador de bare metal distino do MaaS.

É sim possível realizar a implementação de uma aplicação somente o MaaS, pode-se fazer isso por meio da escrita de imagens que contenham a aplicação desejada, no entanto tal méotodo não seria simples, seria necessário para cada máquina do sistema reescrever a imagem desejada toda vez que alguma alteração for feita na aplicação, isso inclui desligar completamente a máquina e realizar um novo PXE Boot com a imagem adaptada para a arquitetura em questão.
