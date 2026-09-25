# Plano de Acao - Desafio API Cast Member

## Objetivo

Implementar o modulo de `CastMember` seguindo o mesmo padrao arquitetural ja utilizado nos modulos de `category` e `genre`, cobrindo dominio, casos de uso, persistencia Django, API REST e testes.

## Base de referencia no projeto

### Padrao atual identificado

- Camada de dominio em `src/core/<contexto>/domain`
- Casos de uso em `src/core/<contexto>/application/use_cases`
- Repositorio Django em `src/django_project/<app>/repository.py`
- Model Django em `src/django_project/<app>/models.py`
- Serializers DRF em `src/django_project/<app>/serializers.py`
- ViewSet DRF em `src/django_project/<app>/views.py`
- Rotas registradas em `src/django_project/urls.py`
- Testes de dominio e aplicacao em `src/core/.../tests`
- Testes de integracao de API em `src/django_project/<app>/tests`
- Teste end-to-end concentrado em `src/tests_e2e`

### Requisitos funcionais do desafio

- Listar `cast_members`
- Criar `cast_member`
- Atualizar `cast_member`
- Deletar `cast_member`
- Validar `name`
- Validar `type`
- Retornar `400` para payload invalido
- Retornar `404` quando o recurso nao existir
- Cobrir com testes unitarios, integracao e pelo menos um fluxo end-to-end

## Decisoes de implementacao

### Modelagem prevista

- Criar entidade `CastMember` no dominio com `id`, `name` e `type`
- Criar enum `CastMemberType` com valores `ACTOR` e `DIRECTOR`
- Manter `UUID` como identificador da entidade, igual aos demais modulos
- Criar app Django dedicada, espelhando o padrao de `category_app` e `genre_app`

### Padrao de resposta da API

- Seguir o padrao atual do projeto:
  - `GET /api/cast_members/` retorna `{ "data": [...] }`
  - `POST /api/cast_members/` retorna `{ "id": "<uuid>" }`
  - `PUT /api/cast_members/<id>/` retorna `204`
  - `DELETE /api/cast_members/<id>/` retorna `204`

### Observacoes importantes

- O desafio nao pede `retrieve` individual nem `PATCH`, entao nao devem entrar no primeiro escopo
- A serializacao do enum deve ficar no serializer, mantendo a view enxuta
- Os testes devem validar tanto contrato HTTP quanto persistencia no repositorio
- Vale manter a nomenclatura interna consistente com o projeto atual, mesmo que category e genre tenham pequenas variacoes entre `Request/Input` e `Response/Output`

## Backlog de implementacao

### Tarefa 1 - Estruturar o dominio de CastMember

**Descricao**

Criar a entidade de dominio, o enum de tipos e a abstracao de repositorio para `CastMember`.

**Subtarefas**

- Criar `src/core/cast_member/domain/cast_member.py`
- Criar `CastMemberType` como `StrEnum`
- Implementar validacoes de `name` e `type`
- Criar `src/core/cast_member/domain/cast_member_repository.py`

**Criterios de aceite**

- A entidade falha ao ser criada com `name` vazio
- A entidade falha ao ser criada com `name` maior que o limite definido
- A entidade falha ao ser criada com `type` invalido
- A entidade aceita apenas `ACTOR` e `DIRECTOR`
- O contrato do repositorio expõe `save`, `get_by_id`, `list`, `update` e `delete`

### Tarefa 2 - Implementar testes de dominio

**Descricao**

Cobrir comportamento da entidade e do enum com testes unitarios.

**Subtarefas**

- Criar testes em `src/core/cast_member/tests/domain`
- Validar criacao bem-sucedida
- Validar cenarios invalidos
- Validar comparacao e comportamento basico da entidade, se alinhado ao padrao usado no projeto

**Criterios de aceite**

- Os testes de dominio documentam as regras de negocio do desafio
- Existe cobertura para `name` invalido
- Existe cobertura para `type` invalido
- Existe cobertura para criacao com `ACTOR` e `DIRECTOR`

### Tarefa 3 - Implementar os casos de uso da aplicacao

**Descricao**

Criar os casos de uso de listagem, criacao, atualizacao e remocao para `CastMember`.

**Subtarefas**

- Criar `list_cast_member.py`
- Criar `create_cast_member.py`
- Criar `update_cast_member.py`
- Criar `delete_cast_member.py`
- Criar excecoes especificas da aplicacao para dados invalidos e recurso nao encontrado

**Criterios de aceite**

- O caso de uso de listagem retorna todos os `cast_members`
- O caso de uso de criacao persiste um novo `cast_member`
- O caso de uso de criacao traduz erro de dominio em excecao de aplicacao
- O caso de uso de atualizacao retorna erro quando o `id` nao existe
- O caso de uso de atualizacao valida `name` e `type`
- O caso de uso de delecao retorna erro quando o `id` nao existe

### Tarefa 4 - Implementar testes unitarios e de integracao dos casos de uso

**Descricao**

Garantir que a camada de aplicacao esteja coberta com testes, usando o mesmo estilo ja adotado em `category` e `genre`.

**Subtarefas**

- Criar testes unitarios com repositorio em memoria
- Criar testes de integracao usando a implementacao concreta do repositorio
- Cobrir fluxo feliz e fluxos de erro

**Criterios de aceite**

- Cada caso de uso possui pelo menos um teste de sucesso
- Casos de erro relevantes possuem testes dedicados
- Os testes demonstram o contrato esperado entre aplicacao e repositorio

### Tarefa 5 - Criar persistencia Django para CastMember

**Descricao**

Adicionar a app Django e sua estrutura de persistencia para `CastMember`.

**Subtarefas**

- Criar `src/django_project/cast_member_app`
- Criar `apps.py`, `models.py`, `repository.py`, `admin.py` e pasta `migrations`
- Criar model Django com `UUID`, `name` e `type`
- Criar migracao inicial
- Implementar repositorio Django convertendo ORM <-> dominio

**Criterios de aceite**

- A app Django esta registrada corretamente nas configuracoes do projeto, se necessario
- A migracao cria a tabela de `cast_member`
- O repositorio Django salva, lista, atualiza, busca por `id` e remove corretamente
- O repositorio converte `type` entre banco e dominio sem ambiguidade

### Tarefa 6 - Implementar serializers da API

**Descricao**

Criar serializers de entrada e saida, incluindo um campo customizado para o enum.

**Subtarefas**

- Criar serializer de listagem
- Criar serializer de criacao
- Criar serializer de atualizacao
- Criar serializer de delecao
- Criar `CastMemberTypeField` baseado em `ChoiceField`

**Criterios de aceite**

- O serializer aceita somente `ACTOR` e `DIRECTOR`
- O serializer converte string HTTP para `CastMemberType`
- O serializer converte `CastMemberType` para string na resposta
- Payload com `type` invalido retorna erro `400`
- Payload com `name` invalido retorna erro `400`

### Tarefa 7 - Implementar ViewSet e rotas

**Descricao**

Expor os endpoints REST pedidos no desafio reaproveitando o padrao de `category` e `genre`.

**Subtarefas**

- Criar `views.py` da app
- Instanciar casos de uso com repositorio Django
- Tratar excecoes de validacao e nao encontrado
- Registrar a rota em `src/django_project/urls.py`

**Criterios de aceite**

- `GET /api/cast_members/` responde `200`
- `POST /api/cast_members/` responde `201`
- `PUT /api/cast_members/<id>/` responde `204`
- `DELETE /api/cast_members/<id>/` responde `204`
- `PUT` e `DELETE` retornam `404` quando o recurso nao existe
- Payload invalido retorna `400`

### Tarefa 8 - Implementar testes de API

**Descricao**

Cobrir o contrato HTTP dos endpoints com testes de integracao em Django REST Framework.

**Subtarefas**

- Criar `src/django_project/cast_member_app/tests/test_views.py`
- Testar listagem
- Testar criacao com payload valido
- Testar criacao com payload invalido
- Testar atualizacao com payload valido
- Testar atualizacao com payload invalido
- Testar atualizacao de recurso inexistente
- Testar delecao com `id` invalido
- Testar delecao de recurso inexistente
- Testar delecao bem-sucedida

**Criterios de aceite**

- Os testes validam status code e estrutura de resposta
- Os testes confirmam persistencia correta no repositorio
- Os testes cobrem `400` e `404` conforme o desafio

### Tarefa 9 - Implementar teste end-to-end

**Descricao**

Criar um teste que exercite mais de um endpoint no mesmo fluxo.

**Subtarefas**

- Criar fluxo com criacao, listagem, atualizacao e delecao
- Validar que os dados refletem as mudancas entre as chamadas

**Criterios de aceite**

- O teste usa multiplos endpoints da API
- O fluxo prova que o recurso pode ser criado, alterado e removido
- O teste passa de forma deterministica

### Tarefa 10 - Validacao final e alinhamento com o projeto

**Descricao**

Executar a bateria de testes relevante e revisar consistencia de nomenclatura e estrutura.

**Subtarefas**

- Rodar testes do novo modulo
- Rodar testes relacionados do projeto, se necessario
- Revisar padrao de nomes, imports e estrutura de pastas

**Criterios de aceite**

- Todos os testes do modulo `cast_member` passam
- Os endpoints seguem o mesmo estilo de `category` e `genre`
- Nao ha divergencias estruturais desnecessarias em relacao ao projeto

## Ordem recomendada de execucao

1. Dominio
2. Testes de dominio
3. Casos de uso
4. Testes da aplicacao
5. Persistencia Django
6. Serializers
7. Views e rotas
8. Testes de API
9. Teste end-to-end
10. Validacao final

## Fora do escopo inicial

- Endpoint de detalhe `GET /api/cast_members/<id>/`
- `PATCH /api/cast_members/<id>/`
- Filtros, paginacao e ordenacao
- Ajustes gerais nos modulos antigos, exceto quando forem necessarios para manter consistencia minima

## Resultado esperado ao final

Ao concluir esse plano, o projeto tera um novo modulo `CastMember` funcional e testado, implementado de forma coerente com a arquitetura ja presente no repositorio e aderente ao contrato definido em `docs/desafio-api-cast-member.md`.
