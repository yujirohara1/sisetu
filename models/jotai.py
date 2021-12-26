from api.database import db, ma

## 実テーブル
class Jotai(db.Model): 
    __tablename__ = "jotai"
    document_name = db.Column(db.String(), primary_key=True) 
    chosa_jiten = db.Column(db.String(), primary_key=True)
    dantai_cd = db.Column(db.String(), primary_key=True)
    dantai_nm = db.Column(db.String(), primary_key=False)
    file_url = db.Column(db.String(), primary_key=False)
    jotai_message = db.Column(db.String(), primary_key=False)
    ymdt = db.Column(db.DATETIME, nullable=False,primary_key=False)

class JotaiSchema(ma.SQLAlchemyAutoSchema):
      class Meta:
            model = Jotai
            load_instance = True
