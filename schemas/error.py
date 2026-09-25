from pydantic import BaseModel

class ErrorSchema(BaseModel):
   """ Estrutura padrão de retorno para mensagens de erro """
   message: str