# Computação em Nuvem

## Cloud Outtro

### Grupo
* #### Alexandre Young
* #### Paulo Tozzo

***

## Questões Finais

### 1. Qual o conceito por trás de *Edge Computing*? (Obs: Não é a rede de celular 2G)

Edge Computing é um paradigma de computação que utiliza o conceito de sistemas distribuídos em nuvem de forma descentralizada, a ideia é aproximar os serviços de cloud dos dispositivos usuários por meio de cloudlets intermediários, "aproximando" o serviço do usuário. No caso de Mobile Edge Computing, cloudlets são implantados nos pontos de saída de internet, como provedores ISPs, chamados de "Edge of the Internet" para pré-processar e cachear dados diminuindo a latência de serviços e a comunicação com o servidor principal.

***

### 2. Você é o CTO (*Chief Technology Officer*) de uma grande empresa com sede em várias capitais no Brasil e precisa implantar um sistema crítico, de baixo custo e com dados sigilosos para a área operacional. Você escolheria Public Cloud ou Private Cloud?

É impossível ter um serviço em Cloud que é ao mesmo tempo de baixo custo,
alta disponibilidade e seguro, dito isso implementar o sistema em uma Private
Cloud parece ser a melhor opção dado que a sigilosidade dos dados é uma questão
de preocupação, em tese existe a possibilidade do provedor de uma nuvem pública
capturar os dados. Por outro lado, perderíamos a vantagem de uma Public Cloud em questão de custo, já que se formos fazer um serviço extremamente robusto e com potencial de alta disponibilidade gastaríamos muito mais em equipamento, infraestrutura e profissionais qualificados quando se é possível alugar instâncias e serviços por um custo muito menor na Public Cloud.

***

### 3. Agora explique para ao RH por que você precisa de um time de DevOps.

Um time de DevOps permitira a todos os participantes do projeto saber como as diferentes áreas de um dado projeto funcionam e se comunicam, permitindo reduzir o custo de produção ao projetar os serviços em base das necessidades
de cada membro. Cada integrante do time tem uma maior "visão do todo" do projeto, sabendo a funcionalidade fundamental de cada bloco assim reduzindo a formação de "caixas pretas" e permitindo ao código uma maior manutenibilidade.

A filosofia de DevOps também tem vários paralelos com a criação de sistemas baseados em microsserviços, o que se adequa muito bem para o desenvolvimento de sistemas distribuídos.

***

### 4. Junte o seu time e monte um plano para DR e HA da empresa. Explique o que é SLA e onde se encaixa nesse contexto.

DR, do inglês Disaster Recovery, pode ser planejado por meio de políticas de redundância de informação crítica, como no caso das informações contidas em banco de dados, por meio de ferramentas de monitoramentos e prevenção de situações de risco, por exemplo vistoriando a carga e memória de instâncias que podem cair, ou fazendo testes de confiabilidade da memória de storage usada, e em geral planejar para os piores cenários concebíveis

Para manter uma Alta Disponibilidade (de HA: High Availability), podem-se usar ferramentas de escalabilidade horizontal elástica, com o uso de um Autoscaling Group, e ferramentas de distribuição de carga, como o Load Balancer que protege um node de ficar sobrecarregado.

SLA (Service-level agreement) é um contrato entre um prestador de serviço e um client que rege as responsabilidades do prestador do serviço quanto à sua qualidade, por exemplo  um provedor de websites pode especificar que garante que sua página ficará de pé 99.99% do tempo ma sua SLA, o que também remete à manutenção de uma boa disponibilidade do serviço (HA).

***

## Projeto Final

### 1. Última questão: dos requisitos de projeto acima, quais são funcionais e quais são não funcionais?

Requisitos funcionais:
* [Cada aluno deverá implementar um microserviço que] Seja distribuído. Pode Utilizar uma infraestrutura de Cloud pública e/ou privada.
* [Cada aluno deverá implementar um microserviço que] Implemente uma API REST.
* Implementar uma aplicação cliente para consumir o serviço via API
* Possuir um script de implantação do projeto (charm, image ou script)

Requisitos não funcionais:
* O projeto é estritamente individual
* [Cada aluno deverá implementar um microserviço que] Seja elástico. Ter a capacidade de criar e destruir instâncias de forma assíncrona.
* O aluno terá livre escolha sobre as funcionalidades propostas.
* Tem que ser migrável para outra nuvem (Não pode usar soluções proprietárias – lock-in).
* Utilizar uma linguagem de programação de livre escolha, embora seja sugerido usar uma que tenha bibliotecas para manipulação de Cloud prontas.
* O prazo final para a entrega é a última aula do semestre. A data de entrega é Improrrogável.
