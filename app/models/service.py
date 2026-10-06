from app.ext import db


class service(db.Model):
    __tablename__ = "services"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    
    
    def to_dict(self):
        return{
            "id": self.id,
            "nome": self.nome,
            "preço": self.preco,
            "duracao": self.duracao,
            "ativo": self.ativo,
            
    }
    