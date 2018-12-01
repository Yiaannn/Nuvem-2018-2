## Projeto Cloud

### Alexandre Young

***

### Instalação

É um requesito para utilizar a cloud proposta que o ambiente de deployment
seja capaz de passar as credenciais de aws para uma instância do boto3. Uma
forma de garantir isso é rodar o comando __configure__ no client da __aws__

Uma vez baixado o repositório, basta rodar o programa cloud_init.py para
inicializar a cloud, ela recebe de parâmetro quantas instâncias provedoras
do serviço serão criadas (padrão 3), por exemplo, para criar 10 instâncias:

```
python3 cloud_init.py --amount 10
```

A quantidade passada em amount não conta o Load Balancer instanciado para
monitorar e controlar o acesso das instâncias

Dois arquivos serão criados, private_key.pem com a chave de acesso privada
caso se desehe logar por ssh nas instâncias (O que não é necessário para
um uso padrão) e taskrc. É necessário que a variável de ambiente
TASKSERVICE_URL seja setada com a url do Load Balancer, e o taskrc é gerado
para que você possa convenientemente setar a variável por meio do comando:

```
source taskrc
```

### Client

Com a variável de ambiente TASKSERVICE_URL setada, o client __taskclient__
pode ser usado par se comunicar com a cloud, alguns comandos de exemplo:
```
taskclient list
taskclient delete --id=0
```
Para mais informações de como usar o client, utilize a flag --help, ela pode ser tanto usada para listar todos os subcomandos quanto para obter mais informações de um comando específico:
```
taskclient --help
taskclient update --help
```
Para atualizar ou adicionar novas entradas no serviço de Tarefas, é
necessário passar uma tarefa em formato json, para questões de
demonstrações, dois jsons foram inclusos, __add_test.json__ e
__update_test.json__ para demonstrar os _subcomandos_ add e _update_
respectivamente

Passar requests para o load balancer antes das instâncias estarem ativas e estáveis retornará um erro 423 (LOCKED)

### Considerações

No backend as informações são guardados em bucket S3 para garantir a propriedade Stateless das chamadas de serviço. Por isso esta cloud utiliza tanto dos serviços EC2 da AWS quanto de S3
