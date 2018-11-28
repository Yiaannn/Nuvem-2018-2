# Computação em Nuvem

## Private Cloud Stack

### Grupo
* #### Alexandre Young
* #### Paulo Tozzo

***

## Instalando - Canonical Distro

### 1. Faça um desenho de como é a sua arquitetura de solução, destacando o hardware, sistema operacional/container e respectivas alocações dos serviços.

Desenho disponível no arquivo diagrama_1.jpg

## Configurando o Openstack

### 2. Faça um desenho de como é a sua arquitetura de rede, desde a conexão com o Insper até a instância alocada.

Desenho disponível no arquivo diagrama_2.jpg

## Criando Usuários

### 3.  Monte um passo a passo de configuração de rede via Horizon.

Uma vez logado no dashboard com o usuário correspondente, acessou-se o painel
lateral *Project*, sessão *Network*, opção *Network Topology*, deste menu,
selecionou-se a opção *Create Network* para gerar uma nova rede interna
associada ao usuário logado.

Uma vez aberto o painel de criação da rede, primeiro deu-se a ela um nome
arbitrário único para distingui-la das redes dos demais usuários, depois
configurouse-a durante a criação para ter um CIDR **192.169.X.0/24**, em que o
valor X foi diferente para cada rede de cada usuário. Usou-se o IP
**192.169.X.1** para o Gateway e, para o DNS, usaram-se os IPs **192.169.X.2**,
pertencente a própria rede interna, **192.168.0.3** que equivale ao IP do
MaaS e **8.8.8.8** como mais um DNS de fallback, sendo esse o DNS da Google.

Para garantir que os IPs que desejamos fixos não sejam servidos pelo servidor
DHCP, setou-se um range específico de alocação dos IPs. que vão de
**192.169.X.3** até **192.169.X.254**.

Por último, configurou-se o roteador para interfaceiar entre a rede interna e
a rede externa, de volta ao menu *Network Topology*, selecionou-se a opção
*Create Router*. No menu de criação do roteador, deu-se novamente um nome
arbitrário para distinguir o roteador entre os usuários e selecionou-se a rede
externa onde o roteador irá agir (no caso do nosso setup, de nome **ext_net**).
Criado o roteador e seu ícone aparecendo no menu de *Network Topology*, um
submenu foi acessado clicando em seu ícone e a opção *Add Interface* foi
selecionada, em que a rede interna correspondente do usuário foi adicionada ao
roteador, completando o processo.


***

## Protótipo II

### Usuários/Repositórios:

* #### Alexandre Young
  https://github.com/Yiaannn/Nuvem-2018-2
* #### Paulo Tozzo
  https://github.com/Formulos/charm_prototype_2

***

## Deja-vu (Juju Reborn)

### 4. Escreva as configurações utilizadas para incluir o Openstack como Cloud Provider no Juju.

Uma vez o Juju instalado na instância em que se vai trabalhar, incluiu-se o
Openstack como Cloud Provider pelo comando *juju add-cloud*, esse comando abre
um contexto de configuração de cloud em que vários parâmetros são pedidos,
sendo esses o tipo de cloud, para o qual se passou *openstack*. um nome para
a cloud, ao qual foi dado *roteiro-small-openstack*, O endpoint da API da
cloud, ao qual se passou *http://192.168.0.247:5000/v3*, o tipo de autenticação,
para o qual se escolheu o tipo *userpass*, a região, para o qual se passou a
região padrão *RegionOne*, uma possível endpoint de API dedicada para a região,
para o qual se usou o mesmo endpoint da cloud, e a opção de criar uma nova
região, que foi recusada.

### 5. Escreva o comando de bootstrap.
```
juju bootstrap roteiro-small-openstack --metadata-source ~/simplestreams/images
```

## Escalando o Kubernetes

### 6. O que é um Hypervisor? Qual o hypervisor do Openstack, da AWS e da Azure?

Hypervisor é o software que orquestra, gerencia e monitora as máquinas virtuais,
por padrão o Openstack utiliza o KVM como seu hypervisor, mas outros podem ser
configurados. A AWS atualmente usa um hypervisor próprio construído a partir do
KVM chamado Nitro, enquanto a Azure usa o Azure Hypervisor, construído a partir
do Hyper-V.

***

## Questões Complementares

### 2. . Dado que vocês trabalharam com Nuvem Pública e com Nuvem Privada, descreva com detalhes como você montaria uma Nuvem Híbrida. Como seria a troca de dados?

Uma nuvem híbrida poderia ser montada criando uma nuvem privada virtual dentro
de uma nuvem pública. Por exemplo, utilizando-se os serviços de uma nuvem
pública como a AWS, pode-se fazer um deployment do openstack e usar as
instâncias fornecidas pela Amazon como fonte de criação para novas instâncias
pertencentes a uma nuvem virtual privada, fragmentando-se as instâncias
similarmente à como as máquinas físicas são fragmentadas.

A troca de dados teria que passar da instância da nuvem virtual privada, para
a instância da nuvem pública para enfim atingir a máquina física.

### 3. . É possível somar todo o hardware disponível e disparar uma instância gigante (ex: mais memória do que disponível na melhor máquina)? Discorra sobre as possibilidades.

Não seria impossível fazer uma máquina paralela utilizando diversos computadores,
mas o overhead da passagem de informação entre as máquinas, a dificuldade de
sincronizar os dados entre elas e o gerenciamento de suas partes em geral seriam
dificuldades muito grande para que essa estratégia valesse a pena. A grande
vantagem de programação em nuvem é a capacidade de escalabilidade horizontal
entre os serviços, e ela é mais apropriada para a comunicação entre diferentes
máquinas.

### 4. Como visto é possível rodar o Juju sobre o Openstack e o Openstack sobre o Juju. Quais os empecilhos de ter um Openstack rodando sobre outro Openstack?

Rodar um Openstack sobre um Openstack não parece muito vantajoso, caso por
exemplo um Openstack esteja rodando em uma nuvem pública, pode-se usar uma
segunda instalação do Openstack para configurar sua própria nuvem privada. Mas
em um ambiente controlado, criar nuvens internas umas as outras não parece
melhor que expandir a nuvem de mais alto nível.

***

## Concluindo

### 1. Cite e explique pelo menos 2 circunstâncias em que a Private Cloud é mais vantajosa que a Public Cloud.

Ter uma private cloud local e reduzida para servir de debugging e prototipação
da arquitetura de desenvolvimento pode agilizar o desenvolvimento e reduzir
custos. Adicionalmente, uma nuvem privada pode servir para proteger informação
sensitiva a qual não se deseja arriscar que as empresas que provém nuvens
públicas obtenham.

### 2. Openstack é um Sistema Operacional? Descreva seu propósito e cite as principais distribuições?

Openstack é uma plataforma de desenvolvimento de computação em nuvem, o qual
pode ser referido como "Cloud Operational System", mas não é um sistema
operacional no sentido mais convencional. o Openstack, por exemplo, não contém
um kernel próprio para se comunicar com a máquina a baixo nível e atua por cima
de um sistema operacional convencional. Seu propósito é alocar recursos para criar
ambientes virtuais em que sistemas operacionais podem ser instalados e utilizados
mesmo contidos dentro do contexto de um outro sistema operacional. Existem no
entanto distribuições de openstack integradas em sistemas operacionais que podem
ser consideradas sistemas operacionais como o Canonical Openstack ou Red Hat
Openstack Plataform.

### 3. Quais são os principais componentes dentro do Openstack? Descreva brevemente suas funcionalidades.

Dentro do Openstack vários componentes atuam como serviços semi-independentes
para prover o Openstack como um todo. Alguns deles são:

Horizon: o componente que provém o dashboard do openstack, provém
ferramentas de visualização da informação provida por outros componentes.

Keystone: provém um sistema de autenticação e gerenciamento de múltiplos
usuários, maneja também credenciais de autenticação usados na comunicação com
outros serviços a partir do client do openstack, como a AWS.

Neutron: disponibiliza os mecanismos que manejam networks, ambos físicos e
virtuais, é o componente responsável por criar a subnet virtual utilizada durante
o roteiro e alocar IPs para as instâncias geradas.

Glance: maneja as imagens utilizadas na inicialização de novas VMs, também é
capaz de gerar imagens a partir de VMs e preparar elas para serem
reinicializadas posteriormente

Cinder: Maneja a memória de bloco disponível para ser usada pelas VMs, instancia
memória na forma de volumes que podem ser montados em VMs de forma modular.

Swift: Maneja uma memória de objetos utilizada pelo próprio openstack para
guardar objetos do openstack em REST, diferente do Cinder, sua memória é
"eventualmente consistente" enquanto não é sincronizada por todo o openstack,
mas isso permite seu acesso ser mais ágil.

Nova: é o componente que maneja os recursos disponíveis para de fato criar e
gerenciar as máquinas virtuais, o hypervisor é um componente do Nova, e
considerando sua funcionalidade é o core da funcionalidade do Openstack.

***

## Conclusão

### A arquitetura em nuvem permite diminuir o desperdício de hardware e ganho na mobilidade de recursos. Contudo existem sérios riscos que podem paralizar as operações de uma empresa. Todo equipamento e arquiteturas complexas são passíveis de falhas tanto operacionais quanto de segurança. Como seria possível mitigar esses riscos?

Seria importante desenvolver uma estratégia de pior caso, garantir que os
servidos providos sejam stateless e que sejam capaz de se recuperarem em caso de
falha ajudaria com a robusteza do sistema. Ter uma bom sistema de monitoramento
capaz de prever possíveis cenários de desastre (por exemplo, monitorar que o
espaço disponível para um banco de dados não irá acabar) ou detectá-los
rapidamente e também fazer backups regulares dos dados armazenados durante
a execução dos arquivos preveniria os piores desastres.

Algo importante tanto para a segurança quanto à falhas
é uma boa estrutura de comunicação entre o ponto de entrada do sistema e o mundo
externo, isso inclui sanitizar os inputs, não deixar ferramentas de desenvolvedor
expostas e um bom planejamento considerando usuários que usem a API disponível
maliciosamente.
