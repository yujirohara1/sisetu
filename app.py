from flask import Flask, render_template, g, request, redirect, url_for, Response, abort, session, jsonify, make_response, send_file
from hamlish_jinja import HamlishExtension
from werkzeug.datastructures import ImmutableDict
import os
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from collections import defaultdict
from datetime import timedelta
import datetime
from flask_bootstrap import Bootstrap
from marshmallow_sqlalchemy import ModelSchema

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from api.database import db, ma
from models.sisetumain import SisetuMain, SisetuMainSchema, VCity, VCitySchema
from sqlalchemy.sql import text
from sqlalchemy import distinct
from sqlalchemy import desc
from sqlalchemy import asc
import json
# from rq import Queue
# from worker import conn
import PyPDF2
# from bottle import route, run
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

DELIMIT = "@|@|@"


class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
app = FlaskWithHamlish(__name__)
bootstrap = Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
mail_address = os.environ.get('MAIL_ADDR')
mail_password = os.environ.get('MAIL_PASS')

class User(UserMixin):
    def __init__(self, id, name, password, tenant_id):
        self.id = id
        self.name = name
        self.password = password
        self.tenant_id = tenant_id

# ログイン用ユーザー作成
users = {
    1: User(1, "yujiro", "yjrhr1102", "demo"),
    2: User(2, "seiya", "seiya7293", "hara"),
    3: User(3, "yasu", "3021", "hara"),
    100: User(100, "demo", "demo", "demo")
}

# ユーザーチェックに使用する辞書作成
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id


def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, my_pwd, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587) # gmail
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, my_pwd)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


@app.route('/AccountToroku',methods=["GET", "POST"])
def SendMail_AccountToroku():
  vals = request.json["data"]
  try:
    msg = create_message(mail_address, mail_address, "", "アカウント登録申請", vals[0] + ", " + vals[1])
    send(mail_address, mail_address, mail_password, msg)
    return "0"
  except:
    # 何もしない
    import traceback  
  return "-1"

@login_manager.user_loader
def load_user(user_id):
  return users.get(int(user_id))

db_uri = "postgresql://postgres:yjrhr1102@localhost:5432/newdb3" #開発用
# db_uri = os.environ.get('DATABASE_URL') #本番用
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
# q = Queue(connection=conn)
        
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")
    
@app.route('/getCustomer_Main/<group_kb>/<yuko_muko>/<nen>/<tuki>')
@login_required
def resJson_getCustomer_Main(group_kb, yuko_muko, nen, tuki):
      # if yuko_muko == "2":
      #   customers = Customer.query.filter(Customer.group_id==group_kb, Customer.tenant_id==current_user.tenant_id).all()
      # elif yuko_muko == "1":
      #   customers = Customer.query.outerjoin(Kakute, Kakute.customer_id==Customer.id).filter(Customer.group_id==group_kb, Customer.list!=None, Customer.tenant_id==current_user.tenant_id, Kakute.nen==2020, Kakute.tuki==3).all()
      # else:
      #   customers = Customer.query.filter(Customer.group_id==group_kb, Customer.list==None, Customer.tenant_id==current_user.tenant_id).all()
      
      sql = " "
      sql = sql + " SELECT "
      sql = sql + "     c.*, "
      sql = sql + "     k.kakute_ymdt "
      sql = sql + " from "
      sql = sql + "    " + TableWhereTenantId("customer") + " c "
      sql = sql + " left join "
      sql = sql + "    (select * from " + TableWhereTenantId("kakute") + " A where nen = " + nen + " and tuki = " + tuki + ") k "
      sql = sql + " on "
      sql = sql + "     c.id = k.customer_id "
      sql = sql + " where "
      sql = sql + "     c.group_id = " + group_kb + " "
      if yuko_muko == "2":
        sql = sql + "     "
      elif yuko_muko == "1":
        sql = sql + "  and   c.list is not null "
      else:
        sql = sql + "  and   c.list is null "
      
      customernentuki = db.session.execute(text(sql))
      customernentuki_schema = CustomerNentukiSchema(many=True)
      return jsonify({'data': customernentuki_schema.dumps(customernentuki, ensure_ascii=False)})

@app.route('/getItem_Daicho/<itemname1>')
@login_required
def resJson_getItem_Daicho(itemname1):
    if itemname1=="すべて":
      items = Item.query.filter(Item.del_flg==0, Item.tenant_id==current_user.tenant_id).all()
    else:
      items = Item.query.filter(Item.del_flg==0,Item.name1==itemname1, Item.tenant_id==current_user.tenant_id).all()

    items_schema = ItemSchema(many=True)
    return jsonify({'data': items_schema.dumps(items, ensure_ascii=False)})

     
@app.route('/getItemGroup_Daicho/')
@login_required
def resJson_getItemGroup_Daicho():
     itemgroup = VItemGroup.query.filter(VItemGroup.tenant_id==current_user.tenant_id).all()
     itemsgroup_schema = VItemGroupSchema(many=True)
     return jsonify({'data': itemsgroup_schema.dumps(itemgroup, ensure_ascii=False)})

     

@app.route('/getVDaichoA_ByCusotmerId/<customerid>')
@login_required
def resJson_getVDaichoA_ByCusotmerId(customerid):
      daicho = VDaichoA.query.filter(VDaichoA.customer_id==customerid, VDaichoA.tenant_id==current_user.tenant_id).all()
      daicho_schema = VDaichoASchema(many=True)
      return jsonify({'data': daicho_schema.dumps(daicho, ensure_ascii=False)})

@app.route('/getVSeikyuA_ByCusotmerIdAndTuki/<customerid>/<nentuki>')
@login_required
def resJson_getVSeikyuA_ByCusotmerId(customerid, nentuki):
      seikyu = VSeikyuA.query.filter(VSeikyuA.customer_id==customerid, VSeikyuA.nen==nentuki[0:4], VSeikyuA.tuki==nentuki[4:6], VSeikyuA.tenant_id==current_user.tenant_id).all()
      seikyu_schema = VSeikyuASchema(many=True)
      return jsonify({'data': seikyu_schema.dumps(seikyu, ensure_ascii=False)})

@app.route('/getCustomer_ById/<customerid>')
@login_required
def resJson_getCustomer_ById(customerid):
      customer = Customer.query.filter(Customer.id==customerid, Customer.tenant_id==current_user.tenant_id).all()
      customer_schema = CustomerSchema(many=True)
      return jsonify({'data': customer_schema.dumps(customer, ensure_ascii=False)})


@app.route('/getItem_ById/<itemid>')
@login_required
def resJson_getItem_ById(itemid):
      item = Item.query.filter(Item.id==itemid, Item.tenant_id==current_user.tenant_id).all()
      item_schema = ItemSchema(many=True)
      return jsonify({'data': item_schema.dumps(item, ensure_ascii=False)})

@app.route('/getDaicho_ByItemId/<itemid>')
@login_required
def resJson_getDaicho_ByItemId(itemid):
      daicho = VDaichoA.query.filter(VDaichoA.item_id==itemid, VDaichoA.tenant_id==current_user.tenant_id).all()
      daicho_schema = VDaichoASchema(many=True)
      return jsonify({'data': daicho_schema.dumps(daicho, ensure_ascii=False)})

@app.route('/getSeikyuNengetuShukei_Main')
@login_required
def resJson_getSeikyuNengetuShukei_Main():
      seikyu = VSeikyuC.query.filter(VSeikyuC.tenant_id==current_user.tenant_id).all()
      seikyu_schema = VSeikyuCSchema(many=True)
      return jsonify({'data': seikyu_schema.dumps(seikyu, ensure_ascii=False)})


@app.route('/getSeikyuNengetuCustomer_Main/<nen>/<tuki>/<groupkb>')
@login_required
def resJson_getSeikyuNengetuCustomer_Main(nen, tuki, groupkb):
      seikyu = VSeikyuB.query.filter(VSeikyuB.nen==nen, VSeikyuB.tuki==tuki, VSeikyuB.group_id==groupkb, VSeikyuB.tenant_id==current_user.tenant_id).all()
      seikyu_schema = VSeikyuBSchema(many=True)
      return jsonify({'data': seikyu_schema.dumps(seikyu, ensure_ascii=False)})



@app.route('/createSeikyu/<customerid>/<nentuki>/<sakujonomi>')
@login_required
def dbUpdate_insSeikyu(customerid, nentuki, sakujonomi):
  y = int(nentuki[0:4])
  m = int(nentuki[4:6])
  
  sql = " "
  sql = sql + " delete from seikyu "
  sql = sql + " where tenant_id = '" + current_user.tenant_id + "' "
  if customerid != '-1' :
    sql = sql + "     and customer_id = " + customerid + " "
  
  sql = sql + "     and cast(to_char(deliver_ymd,'yyyy') as integer) = " + str(y) + " "
  sql = sql + "     and cast(to_char(deliver_ymd,'mm') as integer) = " + str(m) + " "
  db.session.execute(text(sql))
  
  if sakujonomi == 'true' :
    db.session.commit()
    return "1"
  
  blAri = False
  for d in range(1,32):
    if isDate(y, m, d):
      deliverymdstr="%04d/%02d/%02d"%(y,m,d)
      deliverymd=datetime.datetime.strptime(deliverymdstr,"%Y/%m/%d")
      
      sql = " "
      sql = sql + " SELECT "
      sql = sql + "     d.customer_id, "
      sql = sql + "     to_date('" + deliverymdstr + "','yyyy/mm/dd') deliver_ymd, "
      sql = sql + "     d.item_id, "
      sql = sql + "     i.tanka, "
      sql = sql + "     null price_sub, "
      sql = sql + "     d.quantity, "
      sql = sql + "     'dummy' user_id, "
      sql = sql + "     CURRENT_TIMESTAMP "
      sql = sql + " from "
      sql = sql + "    " + TableWhereTenantId("daicho") + " d "
      sql = sql + " inner join "
      sql = sql + "    " + TableWhereTenantId("customer") + " c "
      sql = sql + " on "
      sql = sql + "     d.customer_id =  c.id "
      sql = sql + " inner join "
      sql = sql + "    " + TableWhereTenantId("item") + " i "
      sql = sql + " on "
      sql = sql + "     d.item_id =  i.id "
      sql = sql + " where "
      if customerid != '-1' :
        sql = sql + "     d.customer_id = " + customerid + " and "
      sql = sql + "     d.youbi = " + str(deliverymd.weekday()+1) + " and "
      sql = sql + "     c.list is not null and "
      sql = sql + "     c.list <> 0 "
      # print(sql)
      
      # print(db.session.execute(text(sql)).fetchone())
      
      if db.session.execute(text(sql)).fetchone() is not None:
        # print(db.session.execute(text(sql)).fetchone())
        blAri = True
        data_list = db.session.execute(text(sql))
        seikyus = [{'customer_id':d[0], 'deliver_ymd': d[1], 'item_id': d[2],
                  'price': d[3], 'price_sub': d[4], 'quantity': d[5], 'user_id': current_user.name, 'ymdt': d[7], 'tenant_id': current_user.tenant_id} for d in data_list]
                  
        db.session.execute(Seikyu.__table__.insert(), seikyus)
        db.session.commit()
  
  if blAri :
    return str(customerid)
  else :
    return "-1"
  
def isDate(year,month,day):
    try:
        newDataStr="%04d/%02d/%02d"%(year,month,day)
        newDate=datetime.datetime.strptime(newDataStr,"%Y/%m/%d")
        return True
    except ValueError:
        return False


def TableWhereTenantId(table_nm):
  return " (select * from " + table_nm + " where tenant_id = '" + current_user.tenant_id + "') "



@app.route('/printSeikyu/<customerid>/<customeridB>/<nentuki>/<randnum>')
@login_required
def resPdf_printSeikyu(customerid, customeridB, nentuki, randnum):
  # 
  sql = ""
  sql = sql + "  SELECT to_char(seikyu.deliver_ymd,'yyyy')        nen,                                                                                  " 
  sql = sql + "         to_char(seikyu.deliver_ymd,'mm')         tuki,                                                                                   " 
  sql = sql + "         seikyu.customer_id,                                                                                                             " 
  sql = sql + "         seikyu.deliver_ymd,                                                                                                             " 
  sql = sql + "         seikyu.item_id,                                                                                                                 " 
  sql = sql + "         seikyu.price,                                                                                                                   " 
  sql = sql + "         seikyu.quantity,                                                                                                                " 
  sql = sql + "         item.code                               item_code,                                                                              " 
  sql = sql + "         item.name1                              item_name1,                                                                             " 
  sql = sql + "         item.name2                              item_name2,                                                                             " 
  sql = sql + "         customer.name1                          customer_name1,                                                                         " 
  sql = sql + "         customer.name2                          customer_name2,                                                                         " 
  sql = sql + "         customer.list,                                                                                                                  " 
  sql = sql + "         customer.group_id,                                                                                                              " 
  sql = sql + "         to_char(seikyu.deliver_ymd,'yyyy') || to_char(seikyu.deliver_ymd,'mm') || lpad(seikyu.customer_id::text,6,0::text) SEIKYU_KEY,  " 
  sql = sql + "         customer.harai_kb ,                                                                                                             " 
  sql = sql + "         customer.biko2 zei_kb                                                                                                           " 
  sql = sql + "  FROM   " + TableWhereTenantId("seikyu") + " seikyu                                                                                     " 
  sql = sql + "  inner join " + TableWhereTenantId("item") + " item                                                                                     " 
  sql = sql + "  on                                                                                                                                     " 
  sql = sql + "      seikyu.item_id = item.id                                                                                                           " 
  sql = sql + "  inner join " + TableWhereTenantId("customer") + " customer                                                                             " 
  sql = sql + "  on                                                                                                                                     " 
  sql = sql + "      seikyu.customer_id = customer.id                                                                                                   " 
  sql = sql + "  where                                                                                                                                  " 
  sql = sql + "       to_char(seikyu.deliver_ymd,'yyyy') = '" + nentuki[0:4] + "' and                                                                   " 
  sql = sql + "       to_char(seikyu.deliver_ymd,'mm') = '" + nentuki[4:6] + "' and                                                                     " 
  sql = sql + "       seikyu.customer_id = V_CUSTOMER_ID_V and                                                                                       " 
  sql = sql + "       list IS NOT NULL                                                                                                                  " 
  sql = sql + "  ORDER  BY to_char(seikyu.deliver_ymd,'yyyy'),                                                                                          " 
  sql = sql + "            to_char(seikyu.deliver_ymd,'mm'),                                                                                            " 
  sql = sql + "            customer.list,                                                                                                               " 
  sql = sql + "            seikyu.customer_id,                                                                                                          " 
  sql = sql + "            seikyu.item_id,                                                                                                              " 
  sql = sql + "            seikyu.deliver_ymd;                                                                                                          " 

  sqlA = sql.replace("V_CUSTOMER_ID_V",customerid)
  sqlB = sql.replace("V_CUSTOMER_ID_V",customeridB)
  # sql = " select * from v_seikyu_b where nen = '2021' and tuki = '02' and customer_id = " + customerid

  param_list = MstSetting.query.filter(MstSetting.tenant_id==current_user.tenant_id).all()

  if db.session.execute(text(sqlA)).fetchone() is not None:
    data_listA = db.session.execute(text(sqlA))

    if db.session.execute(text(sqlB)).fetchone() is not None:
      data_listB = db.session.execute(text(sqlB))
    else:
      data_listB = None
    
    timestamp = datetime.datetime.now()
    timestampStr = timestamp.strftime('%Y%m%d%H%M%S%f')
    filename = "file_" + customerid + "_" + customeridB + "_" + timestampStr + "_" + current_user.name
    make(filename, data_listA, data_listB, param_list)

    response = make_response()
    response.data = open("tmp/" + filename + ".pdf", "rb").read()
    response.headers['Content-Disposition'] = "attachment; filename=unicode.pdf"
    response.mimetype = 'application/pdf'
    return filename + ".pdf"
  else:
    return "-1"


@app.route('/binaryTest',methods=["PUT"])
def binaryTest():
  timestamp = datetime.datetime.now()
  timestampStr = timestamp.strftime('%Y%m%d%H%M%S%f')
  if 'excelFile' in request.files:
    fi = request.files['excelFile']
    xl = pd.read_excel(fi, sheet_name=None)
    # data_xls = pd.read_Excel(f)
    dictJuchu = {}
    for sh in xl:
      # dictJuchu[sh]=[]
      for row in xl[sh].itertuples():

        #見出し行から列情報の辞書を作成
        if row.Index <= 11:
          dictJuchu[(sh, "hr" + str(row.Index+1))]=[]
          columnId = 0
          prevCell = ""
          
          for cell in row:
            vcell = str(cell if str(cell) !="nan" else prevCell).replace( '\n' , '' )
            dictJuchu[(sh, "hr" + str(row.Index+1))].append(vcell)
            prevCell = vcell
            columnId += 1
        #データ行
        if row.Index>=12:

          columnId = 0
          for cell in row:
            
            try:
              sisetuMain = SisetuMain()
              sisetuMain.nendo = int(row[1])
              sisetuMain.bunrui = row[2]
              sisetuMain.dantai_cd = row[3]
              sisetuMain.tdfk_nm = row[4]
              sisetuMain.city_nm = row[5]
              sisetuMain.sheet_nm = sh
              sisetuMain.col_key1 = dictJuchu[sh,"hr1"][columnId]
              sisetuMain.col_key2 = dictJuchu[sh,"hr2"][columnId]
              sisetuMain.col_key3 = dictJuchu[sh,"hr3"][columnId]
              sisetuMain.col_key4 = dictJuchu[sh,"hr4"][columnId]
              sisetuMain.col_key5 = dictJuchu[sh,"hr5"][columnId]
              sisetuMain.col_key6 = dictJuchu[sh,"hr6"][columnId]
              sisetuMain.col_key7 = dictJuchu[sh,"hr7"][columnId]
              sisetuMain.col_key8 = dictJuchu[sh,"hr8"][columnId]
              sisetuMain.col_key9 = dictJuchu[sh,"hr9"][columnId]
              sisetuMain.col_key10 = dictJuchu[sh,"hr10"][columnId]
              sisetuMain.col_key11 = dictJuchu[sh,"hr11"][columnId]
              sisetuMain.col_key12 = dictJuchu[sh,"hr12"][columnId]
              sisetuMain.col_index = (columnId)
              if isfloat(str(cell)):
                sisetuMain.val_num = float(cell)
              else:
                sisetuMain.val_char = str(cell)
              db.session.add(sisetuMain)
              db.session.commit()

            except:
              # 何もしない
              import traceback
              traceback.print_exc()
            
            columnId += 1


  return "1"
  # return send_file("tmp/" + timestampStr + ".pdf", as_attachment=True)

        
def isfloat(strval):
  try:
    if strval=="nan" :
      return False
      
    float(strval)  # 文字列をfloatにキャスト
    return True
  except ValueError:
    return False

def null2blank(val):
  if val == "null":
    return ""
  else:
    return val


@app.route('/getCityListByTdfkCd/<tdfkCd>')
def getCityListByTdfkCd(tdfkCd):
    vcitylist = VCity.query.filter(VCity.tdfk_cd==tdfkCd).order_by(asc(VCity.dantai_cd)).all()
    vcitylist_schema = VCitySchema(many=True)
    return jsonify({'data': vcitylist_schema.dumps(vcitylist, ensure_ascii=False)})




@app.route('/getCsvData/<viewnm>/<nentuki>/<groupkb>/<tanto>')
@login_required
def resJson_getCsvData(viewnm, nentuki, groupkb, tanto):

  sqlwhere=" tenant_id = '" + current_user.tenant_id + "' "
  if viewnm == "v_csv_uriage_tantobetu":
    sqlwhere = sqlwhere + " and nen = '" + nentuki[0:4] + "' and tuki = '" + nentuki[4:6] + "' and group_id = " + groupkb + " and tanto_id = '" + tanto + "' " 
  elif viewnm == "v_csv_uriage_groupbetu":
    sqlwhere = sqlwhere + " and nen = '" + nentuki[0:4] + "' and tuki = '" + nentuki[4:6] + "' and group_id = " + groupkb + " and tanto_id = '" + tanto + "' " 
  elif viewnm == "v_csv_uriage_kokyakubetu":
    sqlwhere = sqlwhere + " and nen = '" + nentuki[0:4] + "' and tuki = '" + nentuki[4:6] + "' and group_id = " + groupkb + " and tanto_id = '" + tanto + "' " 
  elif viewnm == "v_csv_hikiotosi":
    sqlwhere = sqlwhere + " and nen = '" + nentuki[0:4] + "' and tuki = '" + nentuki[4:6] + "' and group_id = " + groupkb + " and tanto_id = '" + tanto + "' " 
  elif viewnm == "v_csv_takuhai":
    sqlwhere = sqlwhere + " and group_id = " + groupkb + " and tanto_id = '" + tanto + "' " 
  else:
    None

  sqlA = "select * from " + viewnm + " where " + sqlwhere
  sqlB = "select * from mst_setting where param_id = 'VIEW_COLUMN_NAME' and param_val1 = '" + viewnm + "' and tenant_id = '"+ current_user.tenant_id +"'"

  if db.session.execute(text(sqlA)).fetchone() is not None:
    csvdata = db.session.execute(text(sqlA))

  if db.session.execute(text(sqlB)).fetchone() is not None:
    coldata = db.session.execute(text(sqlB))

  resultset=[]

  for row in coldata:
    resultset.append(row.param_val2.split(","))

  for row in csvdata:
    resultset.append(row)

  timestamp = datetime.datetime.now()
  timestampStr = timestamp.strftime('%Y%m%d%H%M%S%f')
  filename = "file_" + viewnm + "_" + timestampStr + "_" + current_user.name
  
  export_list_csv(resultset, "tmp/" + filename + ".csv")

  # response = make_response()
  # response.data = open("tmp/" + filename + ".pdf", "rb").read()

  # make_list()

  return send_file("tmp/" + filename + ".csv", as_attachment=True)

def export_list_csv(export_list, csv_dir):
  with open(csv_dir, "w", encoding='utf8') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(export_list)




@app.route('/getBunyaMap/<vendornm>')
def resJson_getBunyaMap(vendornm):
    bunyamap = VBunyaMapGroupbyVendor.query.filter(VBunyaMapGroupbyVendor.vendor_nm==vendornm).order_by(asc(VBunyaMapGroupbyVendor.bunya_cd)).all()
    bunyamap_schema = VBunyaMapGroupbyVendorSchema(many=True)
    return jsonify({'data': bunyamap_schema.dumps(bunyamap, ensure_ascii=False)})


@app.route('/getTodohuken/<vendornm>')
def resJson_getTodohuken(vendornm):
    Todohuken = VTodohukenGroupbyVendor.query.filter(VTodohukenGroupbyVendor.vendor_nm==vendornm).order_by(desc(VTodohukenGroupbyVendor.kensu)).all()
    Todohuken_schema = VTodohukenGroupbyVendorSchema(many=True)
    return jsonify({'data': Todohuken_schema.dumps(Todohuken, ensure_ascii=False)})

@app.route('/insertToko/<vendornm>/<systemnm>/<rank1>/<comment1>/<kibo>/<todohuken>')
def insertToko(vendornm, systemnm, rank1, comment1, kibo, todohuken):
  kaito = Kaito()
  kaito.vendor_nm = vendornm
  kaito.system_nm = systemnm
  kaito.situmon_kb = 1
  kaito.hyoka_shubetu = 1
  kaito.hyoka_value = rank1
  kaito.hyoka_comment = comment1
  kaito.ymdt = datetime.datetime.now()
  db.session.add(kaito)
  
  kaito = Kaito()
  kaito.vendor_nm = vendornm
  kaito.system_nm = systemnm
  kaito.situmon_kb = 1
  kaito.hyoka_shubetu = 2
  kaito.hyoka_value = kibo
  kaito.ymdt = datetime.datetime.now()
  db.session.add(kaito)
  
  kaito = Kaito()
  kaito.vendor_nm = vendornm
  kaito.system_nm = systemnm
  kaito.situmon_kb = 1
  kaito.hyoka_shubetu = 3
  kaito.hyoka_value = todohuken
  kaito.ymdt = datetime.datetime.now()
  db.session.add(kaito)
  
  db.session.commit()
  return "1"

@app.route('/insertNanajikuHyoka/<vendornm>/<vals>')
def insertNanajikuHyoka(vendornm, vals):
  vals = vals.split(",")
  for idx in range(0, 7): #0,1,2,3,4,5,6
    if vals[idx].isdecimal():
      kaito = Kaito()
      kaito.vendor_nm = vendornm
      kaito.situmon_kb = 2
      kaito.hyoka_shubetu = idx+1
      kaito.hyoka_value = vals[idx]
      kaito.ymdt = datetime.datetime.now()
      db.session.add(kaito)
  
  db.session.commit()
  return "1"

@app.route('/insertTokuiBunya/<vendornm>/<vals>')
def insertTokuiBunya(vendornm, vals):
  for chk_val in vals.split("|"):
    if len(chk_val.split(",")) == 2:
      cd = chk_val.split(",")[0]
      val = chk_val.split(",")[1]

      kaito = Kaito()
      kaito.vendor_nm = vendornm
      kaito.situmon_kb = 3
      kaito.hyoka_shubetu = cd
      kaito.hyoka_value = val
      kaito.ymdt = datetime.datetime.now()
      db.session.add(kaito)
  
  db.session.commit()
  return "1"

@app.route('/scrapeByVendorNm/<vendornm>')
def scrapeByVendorNm(vendornm):
  # スクレイピング対象の URL にリクエストを送り HTML を取得する
  res = requests.get('https://www.njss.info/bidders/view/' + vendornm + '/')
  # レスポンスの HTML から BeautifulSoup オブジェクトを作る
  soup = BeautifulSoup(res.text, 'html.parser')
  # title タグの文字列を取得する
  title_text = soup.find('title').get_text()
  author_names = [n.get_text() for n in soup.select('div.search_result__list__title search_result__list__title__wmax')]
  # for n in soup.select('div.search_result__list__title search_result__list__title__wmax'):


  # print(author_names)
  # print(title_text)
  # > Quotes to Scrape
  # ページに含まれるリンクを全て取得する
  # links = [url.get('href') for url in soup.find_all('a')]
  dictJuchu = {}
  dictJuchu['aaData']=[]     
  wrappers = soup.find_all(class_="smt_box_wrapper")
  for w in wrappers:
    anken = w.find_all(class_="search_result__list__title search_result__list__title__wmax") # soup.find_all("a", href="sample.pdf")
    if len(anken)==1:
      infos =  w.find_all(class_="search_result__list__information search_result__list__information__wmax")
      dates =  w.find_all(class_="search_result__list__date search_result__list__date__wmax")
      
      for i in infos:
        if len(i.find_all(class_="category"))==3 and len(i.find_all("a"))==3 :
          cates = i.find_all(class_="category")
          vals = i.find_all("a")
          
          d_cate = ""
          d_val = ""
          if len(dates)==1:
            d_cate = dates[0].find_all(class_="category")[0].get_text()
            d_val = dates[0].find_all(class_="category")[0].next_sibling.strip(" ")
          
          dictJuchu["aaData"].append( \
            {"anken":anken[0].get_text().replace("\n",""), \
              "todofuken": vals[0].get_text(), \
              "kikan": vals[1].get_text(), \
                "keisiki": vals[2].get_text(), \
                  "rakusatubi": d_val} 
          )

  # print(links)
  # > ['/', '/login', '/author/Albert-Einstein', '/tag/change/page/1/', '/tag/deep-thoughts/page/1/', '/tag/thinking/page/1/', '/tag/world/page/1/', '/author/J-K-Rowling', '/tag/abilities/page/1/', '/tag/choices/page/1/', '/author/Albert-Einstein', '/tag/inspirational/page/1/', '/tag/life/page/1/', '/tag/live/page/1/', '/tag/miracle/page/1/', '/tag/miracles/page/1/', '/author/Jane-Austen', '/tag/aliteracy/page/1/', '/tag/books/page/1/', '/tag/classic/page/1/', '/tag/humor/page/1/', '/author/Marilyn-Monroe', '/tag/be-yourself/page/1/', '/tag/inspirational/page/1/', '/author/Albert-Einstein', '/tag/adulthood/page/1/', '/tag/success/page/1/', '/tag/value/page/1/', '/author/Andre-Gide', '/tag/life/page/1/', '/tag/love/page/1/', '/author/Thomas-A-Edison', '/tag/edison/page/1/', '/tag/failure/page/1/', '/tag/inspirational/page/1/', '/tag/paraphrased/page/1/', '/author/Eleanor-Roosevelt', '/tag/misattributed-eleanor-roosevelt/page/1/', '/author/Steve-Martin', '/tag/humor/page/1/', '/tag/obvious/page/1/', '/tag/simile/page/1/', '/page/2/', '/tag/love/', '/tag/inspirational/', '/tag/life/', '/tag/humor/', '/tag/books/', '/tag/reading/', '/tag/friendship/', '/tag/friends/', '/tag/truth/', '/tag/simile/', 'https://www.goodreads.com/quotes', 'https://scrapinghub.com']
  # class が quote の div 要素を全て取得する
  # quote_elms = soup.find_all('div', {'class': 'quote'})
  return json.dumps(dictJuchu, skipkeys=True, ensure_ascii=False)



# ログインしないと表示されないパス
@app.route('/protected/')
@login_required
def protected():
    return Response('''
    protected<br />
    <a href="/logout/">logout</a>
    ''')

# ログインパス
@app.route('/', methods=["GET", "POST"])
@app.route('/login/', methods=["GET", "POST"])
@app.route('/demologin', methods=["GET", "POST"])
def login():
  return render_template('index.haml')
    #session.permanent = True
    #app.permanent_session_lifetime = timedelta(minutes=30)
    #if(request.method == "POST"):
    #    try:
    #      msg = create_message(mail_address, mail_address, "", "LatteCloudログイン試行", request.form["username"] + ", " + request.form["password"])
    #      send(mail_address, mail_address, mail_password, msg)
    #    except:
    #      # 何もしない
    #      import traceback
    #    # traceback.print_exc()
    #    # ユーザーチェック
    #    if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"] and request.form["username"] !="demo") or \
    #      (request.form["username"] == "demo" and request.form["password"]=="demo" and 'demologin' in request.url) :
    #        # ユーザーが存在した場合はログイン
    #      login_user(users.get(user_check[request.form["username"]]["id"]))
#
    #      if current_user.name=="demo":
    #        app.permanent_session_lifetime = timedelta(minutes=30)
#
    #      return render_template('index.haml')
#
    #    else:
    #        # return "401"
    #        return render_template("login.haml", result=401)
    #        # return abort(401)
    #else:
    #    return render_template("login.haml")

# ログアウトパス
@app.route('/logout/')
def logout():
    logout_user()
    return render_template("login.haml")


if __name__ == "__main__":
    app.run(debug=True)
