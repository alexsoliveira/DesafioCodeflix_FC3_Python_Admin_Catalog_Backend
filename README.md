# codeflix-catalog-admin
Administração de Catálogo - Codeflix - Python

## Regras Category
- Nome da categoria deverá ser obrigatório.
- Ao criar uma nova categoria um identificador deve ser gerado no formato (uuid).
- Ao criar uma categoria os campos id, descrição e isActive não serão obrigatórios.
- Caso a propriedade isActive não seja informada, deverá receber como default o valor true.
- Teste __str__
- Teste __repr__