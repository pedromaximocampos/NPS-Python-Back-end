from marshmallow import Schema, fields, post_load

class ContactEntitySchema(Schema):
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    telefone = fields.Str(required=True)
    user_id = fields.Int(required=True)

    @post_load
    def make_contact(self, data, **kwargs):
        # Pega o user_id do contexto, se não estiver nos dados
        if 'user_id' not in data and 'user_id' in self.context:
            data['user_id'] = self.context['user_id']
        return data

# Dados de teste
contatos_teste = [
    {
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'telefone': '123456789'
    },
    {
        'nome': 'Maria Santos',
        'email': 'maria@email.com',
        'telefone': '987654321'
    }
]

# Testando o schema
try:
    schema = ContactEntitySchema(many=True)
    schema.context['user_id'] = 1  # Passa o user_id pelo contexto
    contatos_validados = schema.load(contatos_teste, partial=('user_id',))
    
    print("Contatos validados com sucesso!")
    for contato in contatos_validados:
        print(f"Nome: {contato['nome']}")
        print(f"Email: {contato['email']}")
        print(f"Telefone: {contato['telefone']}")
        print(f"User ID: {contato['user_id']}")
        print("---")
except Exception as e:
    print(f"Erro na validação: {str(e)}") 