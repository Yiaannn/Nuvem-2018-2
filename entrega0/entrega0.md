# Computação em Nuvem

## Public Cloud Intro

### Grupo
* #### Alexandre Young
* #### Paulo Tozzo

***

## Explorando a AWS

### 1. Descreva o passo a passo utilizado

Para criar os grupos e usuários, procurou-se nas "Regras de Preenchimento dos Roteiros" as informações do usuário raiz. Uma vez acessado o site de sign-in com as informações de usuário, acessamos o submenu "My Security Credentials" contido no menu com o nome do usuário raiz, redirecionando a página para o menu IAM (Identity and Access Management) e uma vez nesse menu acessou-se a opção "Groups" no painel exibido.

Um novo grupo nomeado "Integrantes" foi criado, habilitado com a permissão de "AdministratorAccess".

Para criar os usuários, utilizou-se da opção "Users" no painel, fez-se usuários de nome "alexandre" e "paulo" de acordo com os respectivos integrantes do grupo. Para ambos foram habilitadas as opções "Programmatic access" e "AWS Management Console access", em seguida adcionaram-se ambos os usuários para o grupo "Integrantes" gerado anteriormente, por fim, concluiu-se o processo de criação dos usuários

### 2. O que são Policies? Por que elas são importantes e devem ser bem definidas?

Policies, no contexto da computação, são as regras que definem e gerenciam as permissões dos objetos em um sistema, incluindo usuários e processos, regendo o escopo de acesso que eles podem seguir.

Ter policies bem definidas mantém seu ambiente operacionalmente seguro ao reger uma hierarquia bem definida de limites do que cada objeto pode ou não fazer.

***

## Primeira Instância

### 1. Descreva passo a passo o processo utilizado.

Primeiramente, acessou-se o painel *Region* e selecionou-se a região *US East (N. Virginia)*, depois, no painel Services, selecionou-se a opção *EC2* no menu *Compute*, nessa tela acessou-se a opção *Instances* no painel lateral, onde clicou-se na opção *Launch Instance* para iniciar o processo de deployment da instância.

Selecionou-se primeiro a AMI a ser utilizada, que de acordo com o roteiro foi a *Ubuntu Server 16.04 LTS (HVM), SSD Volume Type* de 64 bits. No menu *Choose Instance Type* por default a opção *t2.micro* já estava selecionada, e no menu *Add Storage* por default o tamanho de memória em disco já estava configurada como 8Gb.

Confirmou-se que no menu *Configure Security Group* a porta SSH estava aberta para uso, por fim ao selecionar a opção *Review and Launch* criou-se uma nova key pair, em que a chave privada foi salva cuidadosamente,

### 2. Dentro do contexto de Cloud Computing, defina os termos: instance, image, region, VPC, subnet, securitygroup.

- **instance** se refere a um servidor virtual que pode ser requisitado de um serviço cloud.

- **image** é o termo que descreve um estado salvo de uma instância, o termo referencia a ideia de tirar uma "foto" do estado da instância em um determinado momento que pode ser carregada e copiada em diferentes máquinas.

- **region** Se refere à qual região do globo se encontram as máquinas físicas de um dado serviço de Cloud Computing.

- **VPC** do inglês Virtual Private Cloud, se refere a um serviço de Cloud Computing em que seu administrador tem controle dos seus mecanismos internos sendo a rede privada para sí, ainda que não tenha controle das máquinas físicas que à compõe.

- **subnet** descreve uma rede de networking que interfaceia com uma rede externa maior (como por exemplo uma rede domiciliar regida por um roteador interfaceiando com a internet).

- **securitygroup** rege o controle de acesso de packets para as instâncias de uma dada rede, definindo quais portas podem ser usadas e por quais IPs.

### 3. O poder computacional das instâncias é medido em vCPU. O que é vCPU?

vCPU, literalmente virtual CPU, representa uma alocação de processamento disponível em um CPU físico. Para instâncias de mesmas especificações, podemos atribuir para elas a mesma vCPU ainda que o processador físico seja outro.

***

## Primeiro Deploy - Ghost Blog Platform

### 1. Quantas instâncias foram criadas automaticamente? Criar instâncias automaticamente é um atributo positivo ou negativo?

Foram criadas 4 instâncias, uma do tipo *t2.medium* e três do tipo *m3.medium*.

Criar instãncias automaticamente não é um atributo inerentemente ruim, mas a forma com que foi feita foi pouco transparente quanto ao que seria criado e em que quantidade. Um processo automatizado que esclarecesse melhor sua rotina seria mais bem-vindo.

### 2. Quanto custou o protótipo? Assuma que usou uma hora de cada instância.

Uma hora dessas 4 instâncias, requisitadas *On-Demand* custariam 26 centavos de dólar segundo o *Simple Monthly Calculator* disponibilizado pela AWS.

***

## Limpando a bagunça (força bruta)

### 1. Dada a quantidade de computadores apontada na questão anterior, descreva como você montaria um ambiente Ghost em um Datacenter próprio. Assuma que você ainda não possui nenhum hardware disponível, apenas um orçamento aprovado.

Um core de vCPUs da Amazon roda a cerca de 2GHz. Tendo em mente que cada uma das instâncias usam 3.75 Gb de RAM no caso da *m3.medium* ou 4 Gb de RAM no caso da *t2.medium* e não estamos apenas um pouco de storage adicional na forma de 4 Gb SSD. Podemos facilmente passar essas especificações utilizando 4 NUCs da Intel.

As versões mais baratas disponíveis na Amazon que não são usadas estão a cerca de 300 dólares sem taxa de entrega. Com 4 deles seriam gastos pelo menos 1200 dólares, mais um pequeno custo por memória adicional.

### 2. Agora, somando o fato de que hardware deprecia com o tempo e possui um custo mensal de manutenção, compare em termos de custo uma Public Cloud e um Datacenter próprio.


O preço de manter esse ambiente na Public Cloud seria de 193,44 dólares se ele rodasse 24/7 por um mês consecutivo, ou cerca de 100 dólares se ele fosse reservado por um ano. A princípio isso pareceria significar que o Datacenter físico compensaria depois de 6 meses, mas não estamos considerando o custo de um especialista para a manutenção do hardware físico, o custo da eletricidade que será consumida, o custo por um seguro para o Datacenter, etc.
***

## Escalabilidade

### 1. O que faz o crontab?

Crontab é um arquivo que seta instruções para rodar um comando arbitrário em um período específico que pode ser periódico ou não. Essas instruções são lidas pelo daemon *cron* que é quem de fato executa as instruções.

***

## Montando o Autoscaling Groups

### 1. O que é uma AMI?

AMI, ou Amazon Machine Image, é a interface providenciada pela AWS para utilizar imagens de instâncias. Imagens sendo estados salvos das instâncias, como explicado anteriormente no item 2 da sessão *Primeira Instância*.

### 2. O que faz o LoadBalancer? Explique o algoritmo utilizado.

Um LoadBalancer tem o intuito de garantir um acesso homogêneo dos clientes para a rede cloud formada por várias instâncias.

 O LoadBalancer Classic oferecido pela AWS performa *health checks* regulares nas instâncias na forma de pings, levando em consideração o tempo de resposta utilizado para decidir quais instâncias estão mais aptas a receberem tráfego de entrada dos clientes procurando acessar a rede. Para isso o acesso à rede é feito pelo IP (ou nome de endereço traduzido pelo DNS) do LoadBalancer, que rapidamente redireciona o usuário para o IP da instância escolhida.

***

## Fazendo uso da Escalabilidade Horizontal

### 1. Enfim, como funciona o Autoscalling Group da AWS?

O Autoscalling group monitora a carga de cada instância por uma métrica pré-definida, como pelo uso da vCPU, e automaticamente gerencia a criação de novas instâncias quando a carga é alto e a desativação de instâncias quando baixa, seguindo policies setadas pelo seu administrador.

### 2. Qual a diferença entre escalabilidade horizontal e escalabilidade vertical?

Escalabilidade horizontal se refere a capacidade de um serviço de poder ser gerenciado por múltiplos de um mesmo sistema (físico ou virtual) cujo número pode variar dinamicamente agindo como um mesmo bloco lógico.

Escalabilidade vertical se refere a quando a escalabilidade de um dado serviço ocorre alterando a performance das partes que compõe seu sistema (por exemplo, aumentando a quantidade de RAM disponível em um dado servidor), em contrapartida de como na escalabilidade horizontal o que varia é o número de sistemas.

### 3. Qualquer serviço pode fazer uso desse modelo?

Não, existem serviços para os quais a paralelização dos seus serviços não é a melhor resposta para seus problemas. Para um servidor bancário por exemplo, garantir a sincronização dos dados e validação deles com múltiplos micro servidores pode não ser viável.

***

## Questões Complementares

### 1. O que é um VPS? Qual a diferença entre uma instância e um VPS?

VPS, do inglês Virtual Private Server, é exatamente o que o nome sugere, um servidor privado, que providencia um serviço remotamente pela internet, que também é virtual, sendo uma virtualização pertencente a um servidor físico. alugar uma VPS implica em alugar uma certa quantia dos recursos de uma máquina física que existe "por baixo"

Similar a uma instância AWS, a diferença está em que instâncias são uma abstração mais distantes dos componentes físicos, por exemplo, uma conta AWS que maneja várias instâncias do mesmo tipo podem ter hardwares diferentes por baixo e ainda serem a mesma instância, podendo ser dinamicamente requisitadas e liberadas.

### 2. Defina Platform as a Service (PaaS) e Software as a Service (SaaS).

SaaS é um serviço que providencia acesso a softwares via um serviço, como pelo acesso da Internet. Um bom exemplo disso é a suíte de serviços da Google, que tem diferentes serviços como de email, geolocalização, manejamento remoto de impressoras, etc.

PaaS é um serviço que providencia uma plataforma capaz de ser usadas para desenvolver e hostear serviços, podendo até mesmo serem usadas para providenciar serviços em SaaS. Diferente de IaaS (Infrastrucutre as a Service), um PaaS não requer que você tenha acesso ou controle da máquina física ou virtual que providencia essa plataforma.

### 3. O modelo LoadBalancer possui um custo fixo elevado. Como você justificaria o uso e a configuração de um LoadBalancer para uma empresa?

Para as empresas, manter o tempo de carregamento da página o mais baixo possível é de grande interesse, já que existe uma correlação de permanência dos usuários nas páginas e responsividade delas. Gerenciar os acessos de forma que um usuário é sempre conectado ao servidor capaz de responder mais rapidamente é portanto uma qualidade muito atraente para uma empresa.

***

## Concluindo

### 1. Defina Public Cloud. Cite a principal vantagem e desvantagem.

Um serviço de Public Cloud providencia os meios pelos quais um público geral pode alocar e utilizar instâncias de Cloud Computing pertencendo a uma dada rede, normalmente disponível por um custo maleável especificado pelo provedor.

A vantagem de usar uma Public Cloud é que a manutenção e gerenciamento do Datacenter físico por trás fica por responsabilidade do provedor do serviço. E a desvantagem é o outro lado de não ter acesso ao datacenter físico, as instâncias são prédefinidas pelo hardware disponível, então customizar o hardware específico por trás não é possível, isso inclui a sua localização física no mundo. Caso por exemplo uma empresa necessite de um servidor de baixa latência em uma região específica não cobrida por uma Public Cloud, pode ser que precise de seu próprio Datacenter.

### 2. Defina Infrastructure as a Service (IaaS).

Infrastructure as a Service descreve um serviço em que o usuário é capaz de utilizar máquinas remotas (físicas ou virtuais) para desenvolver, hostear ou processar dados, sendo possível até usar um IaaS para providenciar um serviço de PaaS. A EC2 da AWS que foi o foco de estudo neste roteiro é um IaaS.

### 3. Defina Escalabilidade.

Escalabilidade é a característica de um serviço de poder facilmente ser adequado a uma quantidade variável de usuários, com um custo próximo a diretamente proporcional de manutenção do serviço para o número de clientes.

***

## Conclusão

### Imagine como é o processo de alocação de uma instância. O que é realmente uma instância? Como você montaria um ambiente similar a AWS em um Datacenter próprio?

Uma instância é uma máquina virtual que abstrai a implementação específica da máquina física que à implementa. Simular a AWS requereria no mínimo uma grande quantidade de computadores de alto custo-benefício, cada um rodando múltiplas possíveis instâncias de características distintas.

Uma grande quantidade de bandwidth também seria necessária, assim como a capacidade de prover diferentes IPs únicos conectados à Internet. Além disso os computadores do Datacenter necessitariam implementar algum software manejamento para a criação e gerenciamento das instâncias, é possível desenvolver a própria, mas soluções abertas existem, como a OpenStack.
