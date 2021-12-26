from api.database import db, ma

## 実テーブル
class SisetuMain(db.Model): 
    __tablename__ = "sisetu_main"
    nendo      = db.Column(db.Integer, primary_key=True) 
    bunrui     = db.Column(db.String(), primary_key=False) 
    dantai_cd  = db.Column(db.String(), primary_key=True) 
    tdfk_nm    = db.Column(db.String(), primary_key=False) 
    city_nm    = db.Column(db.String(), primary_key=False) 
    sheet_nm   = db.Column(db.String(), primary_key=True)
    col_index  = db.Column(db.Integer, primary_key=True)  
    col_key1   = db.Column(db.String(), primary_key=False) 
    col_key2   = db.Column(db.String(), primary_key=False) 
    col_key3   = db.Column(db.String(), primary_key=False) 
    col_key4   = db.Column(db.String(), primary_key=False) 
    col_key5   = db.Column(db.String(), primary_key=False) 
    col_key6   = db.Column(db.String(), primary_key=False) 
    col_key7   = db.Column(db.String(), primary_key=False) 
    col_key8   = db.Column(db.String(), primary_key=False) 
    col_key9   = db.Column(db.String(), primary_key=False) 
    col_key10  = db.Column(db.String(),  primary_key=False) 
    col_key11  = db.Column(db.String(),  primary_key=False) 
    col_key12  = db.Column(db.String(),  primary_key=False) 
    tani       = db.Column(db.String(), primary_key=False) 
    val_num    = db.Column(db.Numeric, primary_key=False) 
    val_char   = db.Column(db.String(), primary_key=False) 
    val_kba    = db.Column(db.String(), primary_key=False) 
    val_kbb    = db.Column(db.String(), primary_key=False) 
    val_kbc    = db.Column(db.String(), primary_key=False) 

class SisetuMainSchema(ma.SQLAlchemyAutoSchema):
      class Meta:
            model = SisetuMain
            load_instance = True

class VCity(db.Model): 
    __tablename__ = "v_city"
    tdfk_cd = db.Column(db.String(), primary_key=True) 
    dantai_cd = db.Column(db.String(), primary_key=True) 
    city_nm = db.Column(db.String(), primary_key=False) 

class VCitySchema(ma.SQLAlchemyAutoSchema):
      class Meta:
            model = VCity
            load_instance = True

# class VTokoGroupbySystem(db.Model): 
#     __tablename__ = "v_toko_groupby_system"
#     system_nm = db.Column(db.String(), primary_key=True) 
#     kensu = db.Column(db.Integer, primary_key=True) 
#     rank1_avg = db.Column(db.Float , primary_key=True) 

# class VTokoGroupbySystemSchema(ma.SQLAlchemyAutoSchema):
#       class Meta:
#             model = VTokoGroupbySystem
#             load_instance = True


# #v_tokoradar_groupby_vendor
# class VTokoRadarGroupByVendor(db.Model): 
#     __tablename__ = "v_tokoradar_groupby_vendor"
#     vendor_nm = db.Column(db.String(), primary_key=True) 
#     shubetu1_avg = db.Column(db.Float , primary_key=True) 
#     shubetu2_avg = db.Column(db.Float , primary_key=True) 
#     shubetu3_avg = db.Column(db.Float , primary_key=True) 
#     shubetu4_avg = db.Column(db.Float , primary_key=True) 
#     shubetu5_avg = db.Column(db.Float , primary_key=True) 
#     shubetu6_avg = db.Column(db.Float , primary_key=True) 
#     shubetu7_avg = db.Column(db.Float , primary_key=True) 

# class VTokoRadarGroupByVendorSchema(ma.SQLAlchemyAutoSchema):
#       class Meta:
#             model = VTokoRadarGroupByVendor
#             load_instance = True


# class VBunyaMapGroupbyVendor(db.Model): 
#     __tablename__ = "v_bunyamap_groupby_vendor"
#     vendor_nm = db.Column(db.String(), primary_key=True) 
#     bunya_cd = db.Column(db.Integer, primary_key=True) 
#     bunya_nm = db.Column(db.String(), primary_key=True) 
#     ryaku_nm = db.Column(db.String(), primary_key=True) 
#     kensu = db.Column(db.Integer, primary_key=True) 

# class VBunyaMapGroupbyVendorSchema(ma.SQLAlchemyAutoSchema):
#       class Meta:
#             model = VBunyaMapGroupbyVendor
#             load_instance = True


# class VTodohukenGroupbyVendor(db.Model): 
#     __tablename__ = "v_todohuken_groupby_vendor"
#     vendor_nm = db.Column(db.String(), primary_key=True) 
#     hyoka_value = db.Column(db.String(), primary_key=True) 
#     kensu = db.Column(db.Integer, primary_key=True) 

# class VTodohukenGroupbyVendorSchema(ma.SQLAlchemyAutoSchema):
#       class Meta:
#             model = VTodohukenGroupbyVendor
#             load_instance = True
