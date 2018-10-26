# Computação em Nuvem

## Deployment Orchestration

### Grupo
* #### Alexandre Young
* #### Paulo Tozzo

***

## Instalando Juju

### 1. Qual o S.O. utilizado na máquina Juju? Quem o instalou?

O sistema operacional instalado foi o Ubuntu 18.04.1 LTS, instalado pelo MaaS
e servido durante o o Boot PXE.

### 2. O programa juju client roda aonde? E o juju service? Como eles integram entre si?

O juju client roda na máquina do MaaS, já o juju service roda na sua própria máquina, o NUC de nome juju. O client cuida de interfacear com os usuários e criar novas instâncias de juju services.

Uma vez que um controller do juju está ativo, que é o serviço do juju, podemos
utilizar o client para realizar o deploy de charms em uma mesma rede, charms
sendo pacotes de inicialização para o juju que realizam o deploy de serviços
arbitrários em uma máquina alvo.

### 3. O que é LXC? e LXD?

LXC é o nome dado para um ferramental de baixo nível para criar containers de Linux, containers são escopos que simulam um contexto de sistema independe  ao da máquina onde ele se encontra implementado, mas ainda compartilhando o mesmo kernel e por consequênccia tendo um overhead bem menor do que associado a uma máquina virtual tradicional.

LXD é um daemon controlador de containers de Linux que implementa uma API REST para manejar o container e comunicar requests externas até mesmo via rede.

***

## Deploying Wordpress com Load Balancing

### 4. Explique o conceito por traz do HAProxy (Reverse Proxy). Vocês já fizeram algo parecido?

HAProxy atua como um Load Balancer, a ideia de Reverse Proxy vem de que um único front pode ser servido por múltiplos servidores diferentes dependendo do contexto, daí vindo o nome de proxy reverso (em um proxy normalmente pensaríamos os fronts como diferentes proxys para um único servidor).

Fizemos o uso de um Load Balancer em um roteiro passado quando requisitamos  os serviços da AWS durante o Roteiro 0, podemos usar o HAProxy com o mesmo propósito, de dividir a carga entre os servidores e por resultado aumentar a disponibilidade do sistema.



### 5. Na instalação, o Juju alocou automaticamente 4 máquinas físicas, duas para o Wordpress, uma para o Mysql e uma para o HAProxy. Considerando que é um Hardware próprio, ao contrário do modelo Public Cloud, isso é uma característica boa ou ruim?

Considerando que temos controle do hardware alvo para deployments, essa característica é muito boa.

Ter um sistema automatizado de deployment de serviços facilita muito o processo
de inicialização e manutenção de um serviço distribuído, com o hardware próprio
em questão temos a garantia adicional de que o juju usará as maquinas que
disponibilizamos para ela não correremos algum risco de sofrer cobranças
inesperadas por máquinas que o juju pode vir a subir silenciosamente em uma
cloud aberta.

### 6. Crie um roteiro de implantação do Wordpress no seu hardware sem utilizar o Juju.

Sem o juju ou outro software similar as máquinas do Wordpress, SQL e HAProxy deveriam ser preparadas manualmente, isso significa que a instalação das imagens de sistema, preparação das dependências de cada servidor e configurações de comunicação entre os servidores deveriam ser todas feitas manualmente.

 * Wordpress

 (Repetir os passos para duas máquinas diferentes para imitar o setup utilizado
 no roteiro)

 Baixar e instalar as dependências via 'apt install wordpress'.
 Baixar e instalar também o apache2 web server por 'apt install apache2'

 Editar um arquivo de configuração '/etc/apache2/sites-available/wordpress.con'
 para fazer a linkagem do servidor apache rodando localmente com o wordpress.

 Habilitar o serviço do apache via 'a2ensite wordpress' e
 'systemctl restart apache2.service'.

 Editar o arquivo de configuração '/etc/wordpress/config-localhost.php' para
 fazer a linkagem com o servidor MySQL, configurando o host do servidor externo
 que irá ser usado.

 Uma vez que todos os outros estiverem operantes, fazer as edições finais da
 página do wordpress pelo dashboard em 'http://hostname/blog/wp-admin/install.php'
 substituindo o hostname pelo valor adequado.

 * HAProxy

 Baixar e instalar as dependências via 'apt install haproxy'.

 Modificar o arquivo de configuração em 'etc/haproxy/haproxy.cfg' com as
 configurações que forem pertinentes para a sua aplicação, definindo as seções
 de frontend e backend com os IPs a serem usados.

 Iniciar o serviço por meio de 'sudo service haproxy restart'.

 * MySQL

 Baixar e instalar as dependências via 'sudo apt install mysql-server'.

 Modificar o arquivo de configuração '/etc/mysql/my.cnf' setando os hosts os
 quais escutar (Ou seja, os hosts de ambos os Wordpress).

 Iniciar o serviço por meio de 'sudo systemctl restart mysql.service'

 Criar um database usando seguinte script de inicialização:
 ```
 CREATE DATABASE wordpress;
 GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER
 ON wordpress.*
 TO wordpress@`hostname`, wordpress@`hostname2`
 IDENTIFIED BY 'yourpasswordhere';
 FLUSH PRIVILEGES;
 ```

 executar 'cat wordpress.sql | sudo mysql --defaults-extra-file=/etc/mysql/debian.cnf'.

***

## Protótipo I

### Usuários/Repositórios:

* #### Alexandre Young
  https://github.com/Yiaannn/Nuvem-2018-2
* #### Paulo Tozzo
  https://github.com/Formulos/charm_prototype

***

## Questões Complementares

### 1. Juju é uma aplicação distribuída? E o MaaS?

O juju haje como um orquestrador capaz de inicializar e monitorar aplicações
distribuídas, no entanto o juju em sí não é uma aplicação distribuída. Quando
utilizamos o controller do juju um único node é dedicado a essa aplicação.

Similarmente, a implementação que fizemos do MaaS para este roteiro também não
tem um caráter de aplicação distribuída, Uma única máquina é usada para hostear
o serviço do MaaS ainda que ele em sí maneje diferentes máquinas.

### 2. Qual a diferença entre REST e RPC?

RPC, do inglês Remote Procedure Call é um protocolo de comunicação dedicado à
possibilitar a chamada de funções remotas entre um client e um server.
Diferentemente de uma API REST, uma comunicação por RPC não tem uma definição
no protocolo que especifica um recurso como alvo primário de suas ações. Uma
função RPC pode ser qualquer alteração arbitrária, como alterar um
conjunto de variáveis globais de um sistema, sem a abstração de recursos usada
em REST.

Ilustrando em mais detalhes, uma função em RPC poderia, sem forçar o protocolo,
realizar operações de escrita e leitura na mesma chamada e mudar alguma espécie
de estado global no servidor, enquanto uma comunicação em REST deveria separar o propósito de suas chamadas através de verbos como GET e POST de forma stateless.

### 3. O que é SOAP?

SOAP (Simple Object Acces Protocol) é ainda outro protocolo de comunicação que
usa XML como o formato para codificar as mensagens entre um client e um
servidor.

***

## Concluindo

### 1. O que é e o que faz um Deployment Orchestrator? Cite alguns exemplos.

Um Deployment Orchestrator como o juju trata de articular, mapear e implantar a diferentes serviços de uma rede. A premissa é que o software seja capaz de servir como uma ferramenta de edição e articulação em alto nível da comunicação
que ocorre entre esses serviços além que seja capaz de cuidar das minúcias da implementação em sí de uma forma automatizada.

Outros Deployment Orchestrators que existem além do juju incluem o Chef, Puppet
e o Ansible da Red Hat.

### 2. Como é o o processo de interação entre o MaaS e o Juju?

MaaS está preocupado com a máquina física e sua disponibilidade no sistema
físico, enquanto o juju está preocupado com os serviços que estão operando em
cada máquina e sua disponibilidade no sistema em um nível mais alto.

Como serviços precisam de máquinas físicas para existir, o juju precisa do MaaS
(ou ao menos outro serviço similar) para disponibilizar essas máquinas e cuidar
das preocupações de baixo nível do sistema. Com o MaaS operando por baixo o
juju pode agir utilizando essas máquinas para disponibilizar seus serviços.

### 3. Defina Aplicação Distribuída, Alta Disponibilidade e Load Balancing?

Uma Aplicação Distribuída é aquela que suas partes são divididas entre
diferentes nodes do nosso sistema. Durante o roteiro levantamos um sistema
utilizando diferentes nodes, utilizando do Haproxy, Wordpress e MySQL para
levantar um servidor de um site, esse sistema foi por exemplo uma aplicação
distribuída

Alta Disponbilidade se refere à capacidade do sistema de se manter estável e
funcional ao longo do tempo, diante de quaisquer pressões que venha a sofrer,
incluindo gasto dos recursos físicos, cargas externas imprevistas, falha de
subsistemas implementados, etc. Utilizando o mesmo exemplo do sistema feito
neste roteiro, nosso sistema apresentou uma boa medida para aumentar a
resiliência do sistema (o que leva á alta disponibilidade) ao implementar dois
nodes servindo o Wordpress manejados pelo HAProxy, garantindo que ainda que
um node do Wordpress esteja indisponível por qualquer motivo, dispomos de uma
redundância que permitirá o sistema continuar funcionando.

Load Balancing é o recurso que permite balancear as requisições externas a um
sistema, de uma forma que vários backends diferentes podem em paralelo processar
e responder adequadamente a essas requisições. Novamente no exemplo descrito o
HAProxy foi utilizado como um Load Balancer entre os dois nodes servindo a
página do Wordpress.

***

## Conclusão

### O Juju utilizou o MaaS como provedor de recursos. O MaaS por sua vez forneceu o que havia disponível no rack. Você acha que seria necessária uma máquina de 32Gb para rodar um Apache Webserver ou um Load Balancer? Extrapole a resposta para um Datacenter real, onde as máquinas possuem configurações muito superiores. Como resolver esse problema?

Nos exemplos do roteiro utilizamos um serviço por máquina, no entanto
poderíamos fazer o uso de containers e máquinas virtuais para encapsular vários
serviços em uma mesma máquina, de forma a melhor alocar os recursos das máquinas
que usamos. Um datacenter real provavelmente iria fragmentar suas máquinas em
diferentes máquinas virtuais capazes de agir no sistema como máquinas
independentes.
