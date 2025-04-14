# Criptografia Híbrida
Implementação de criptografia híbrida usando AES (modo GCM) e RSA com PyCryptodome

Este projeto implementa um sistema de criptografia híbrida utilizando os algoritmos AES (Advanced Encryption Standard) e RSA (Rivest–Shamir–Adleman), aliando a velocidade da criptografia simétrica com a segurança da criptografia assimétrica.
A mensagem é criptografada de forma rápida e eficiente com AES, enquanto a chave utilizada no AES é protegida com RSA, garantindo segurança na transmissão da chave.

# Tabela do fluxo de criptografia híbrida

| Etapa                            | Algoritmo         | Chave usada                    | Quem executa   |
|----------------------------------|-------------------|--------------------------------|----------------|
| Criptografar a mensagem          | AES (simétrico)   | Chave simétrica gerada         | Remetente      |
| Criptografar a chave simétrica   | RSA (assimétrico) | Chave pública do destinatário  | Remetente      |
| Descriptografar a chave simétrica| RSA (assimétrico) | Chave privada do destinatário  | Destinatário   |
| Descriptografar a mensagem       | AES (simétrico)   | Chave simétrica recuperada     | Destinatário   |

# Bibliotecas utilizadas
A principal biblioteca utilizada para criptografia neste projeto é a PyCryptodome

#🔒 Modo GCM: segurança e integridade
Neste projeto, utilizamos o modo GCM (Galois/Counter Mode) do AES. Esse modo fornece confidencialidade e integridade/autenticidade dos dados, pois além de criptografar o conteúdo da mensagem, verifica se este foi alterado durante a transmissão da mensagem por meio de um código de autenticação (tag). 

# Tabela resumo do algoritmo de criptografia híbrida

| Etapa                       | Descrição                                                                 |
|----------------------------|---------------------------------------------------------------------------|
| 1. Geração do texto        | Geração de texto aleatório para ser criptografado                        |
| 2. Geração da chave AES    | Geração de uma chave simétrica para encriptação com AES                  |
| 3. Encriptação com AES     | Uso do modo GCM para garantir confidencialidade e integridade            |
| 4. Encriptação da chave AES| A chave AES é encriptada com RSA (chave pública do destinatário)         |
| 5. Criação do payload      | Agrupamento de `ciphertext`, `nonce`, `tag` e `aes_key_encrypted`        |
| 6. Armazenamento em JSON   | O payload é salvo em um arquivo `.json` com codificação base64           |
| 7. Decriptação RSA         | O destinatário usa sua chave privada para decriptar a chave AES          |
| 8. Decriptação AES         | Uso da chave AES recuperada para decriptar o conteúdo original           |
| 9. Verificação da tag      | Verificação de autenticidade da mensagem via `tag` do modo GCM           |

# 💾 Armazenamento do Payload
Após a criptografia, o remetente salva as informações necessárias para a descriptografia em um arquivo JSON. 

O conteúdo do arquivo JSON inclui:

ciphertext: mensagem criptografada
tag: código de autenticação gerado pelo GCM
nonce: valor aleatório necessário para descriptografar no modo GCM
aes_key_encrypted: chave AES criptografada com RSA
