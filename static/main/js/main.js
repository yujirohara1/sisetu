window.onload = function(){

  createTdfkSelectOption();
}

document.getElementById('btnFileImport').addEventListener('click', function() {
  var files = document.querySelector('#inputGroupFile').files
  let formData = new FormData();
  formData.append('excelFile', files[0]);

  fetch('/binaryTest', {
    method: 'PUT',
    body: formData,
  })
  .then(res => res.json())
  .then(jsonData => {
    document.querySelector('#lblFileProperty').innerHTML = "取り込み完了！"; //jsonData.data;
    document.getElementById('btnFileImport').classList.remove("disabled");
  })
  .catch(error => { console.log(error); });
  document.getElementById('btnFileImport').classList.add("disabled");
});




//ファイル取り込みモーダルを起動
//ファイルインプットタグを初期化
//
document.getElementById('modalExcelUpload').addEventListener('shown.bs.modal', function () {
  document.getElementById('inputGroupFile').value="";
  document.getElementById("lblFileProperty").innerHTML = "";
  document.getElementById('btnFileImport').classList.add("disabled");
  
})




document.getElementById("inputGroupFile").addEventListener("change", function(){
  let nBytes = 0,
      oFiles = this.files,
      nFiles = oFiles.length;

  for (let nFileId = 0; nFileId < nFiles; nFileId++) {
    nBytes += oFiles[nFileId].size;
  }
  let sOutput = nBytes + " bytes";
  // 倍数近似のための任意のコード
  const aMultiples = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  for (nMultiple = 0, nApprox = nBytes / 1024; nApprox > 1; nApprox /= 1024, nMultiple++) {
    sOutput = nApprox.toFixed(3) + " " + aMultiples[nMultiple] + " (" + nBytes + " bytes)";
  }
  // 任意コードの末尾
  if(nFiles==1){
    document.getElementById("lblFileProperty").innerHTML = sOutput;
    document.getElementById('btnFileImport').classList.remove("disabled");
  }
}, false);


document.getElementById("selTdfk").addEventListener("change", function(){
  val = document.getElementById("selTdfk").value;
  fetch('/getCityListByTdfkCd/' + val, {
    method: 'GET',
    'Content-Type': 'application/json'
  })
  .then(res => res.json())
  .then(jsonData => {
    list = JSON.parse(jsonData.data)
    createCitySelectOption(list);
    UndispLoading();
    return;
    //document.querySelector('#lblFileProperty').innerHTML = "取り込み完了！"; //jsonData.data;
    //document.getElementById('btnFileImport').classList.remove("disabled");
  })
  .catch(error => { console.log(error); });
  dispLoading();
});


document.getElementById("selCity").addEventListener("change", function(){
  val = document.getElementById("selCity").value;
  fetch('/getFullRecordByDantaiCd/' + val, {
    method: 'GET',
    'Content-Type': 'application/json'
  })
  .then(res => res.json())
  .then(jsonData => {
    list = JSON.parse(jsonData.data);
    createTable(list);
    UndispLoading();
    return;
    //document.querySelector('#lblFileProperty').innerHTML = "取り込み完了！"; //jsonData.data;
    //document.getElementById('btnFileImport').classList.remove("disabled");
  })
  .catch(error => { console.log(error); });
  dispLoading();
});

function createTable(datalist){
  var tableDiv = document.getElementById("mainTableDiv");
  while(tableDiv.lastChild){
    tableDiv.removeChild(tableDiv.lastChild);
  }

  let table = document.createElement("table");
  let thead = document.createElement('thead');
  let tbody = document.createElement('tbody');

  let trow = document.createElement('tr');
  let head_1 = document.createElement('th');
  head_1.innerHTML = "aaaaa";
  let head_2 = document.createElement('th');
  head_2.innerHTML = "bbbb";
  let head_3 = document.createElement('th');
  head_3.innerHTML = "ccc";
  trow.appendChild(head_1);
  trow.appendChild(head_2);
  trow.appendChild(head_3);
  thead.appendChild(trow);

  var lastIndex = -1;
  var blAddRow = false;
  trow = document.createElement('tr');
  let tdataVal = document.createElement('td');
  for(let i in datalist){

    if(lastIndex != datalist[i].col_index){ //新しく行が始まったときにインデックスと見出し作成
      let tdataA = document.createElement('td');
      tdataA.innerHTML = datalist[i].col_index;
      //trow.appendChild(tdataA);
  
      let tdataB = document.createElement('td');
      tdataB.innerHTML = formatCategory1(datalist[i].col_key1);
      trow.appendChild(tdataB);
  
      let tdataC = document.createElement('td');
      tdataC.innerHTML = formatCategory2(datalist[i].col_key2);
      trow.appendChild(tdataC);
  
      let tdataD = document.createElement('td');
      tdataD.innerHTML = formatCategory3(datalist[i].col_key3);
      trow.appendChild(tdataD);
  
      let tdataE = document.createElement('td');
      tdataE.innerHTML = formatCategory4(datalist[i].col_key4);
      trow.appendChild(tdataE);
  
      let tdataF = document.createElement('td');
      tdataF.innerHTML = formatCategory5(datalist[i].col_key5);
      trow.appendChild(tdataF);
      
      let tdataG = document.createElement('td');
      tdataG.innerHTML = formatCategory6(datalist[i].col_key6);
      trow.appendChild(tdataG);
      
      let tdataH = document.createElement('td');
      tdataH.innerHTML = datalist[i].col_key7;
      trow.appendChild(tdataH);
    }


    let tdataVal = document.createElement('td');
    tdataVal.innerHTML = formatCategoryValue(datalist[i].val_num);
    tdataVal.classList.add("text-end"); //
    trow.appendChild(tdataVal);
    
    if(IsSameTR_NextRow(datalist, i)){
      ; //継続
    } else {
      tbody.appendChild(trow);
      trow = document.createElement('tr');
    }
    lastIndex = datalist[i].col_index;

  }
  table.appendChild(thead);
  table.appendChild(tbody);
  table.classList.add("table");
  table.classList.add("table-bordered");
  table.classList.add("table_sticky");
  table.classList.add("fs-7"); //text-end
  table.id = "mainTable";
  document.getElementById('mainTableDiv').appendChild(table);
  //table = new DataTable(mainTable);
}

function IsSameTR_NextRow(datalist, i){
  try{
    if (datalist[i].col_index == datalist[Number(i)+1].col_index){
      return true;
    }
  }catch(e){

  }
  return false;
}

//var table = new DataTable("table");

function createCitySelectOption(datalist){
  var select = document.getElementById("selCity");
  while(select.lastChild){
    select.removeChild(select.lastChild);
  }
  var option = document.createElement("option");
  option.value = "0";
  option.text = "（市区町村選択）";
  select.appendChild(option);  
  for(let i in datalist){
    var option = document.createElement("option");
    option.value = datalist[i].dantai_cd;
    option.text = datalist[i].city_nm;
    select.appendChild(option);
  }
}


// 都道府県プルダウンの作成
// べた書きでいくよ
// selTdfk
function createTdfkSelectOption(){
  var select = document.getElementById("selTdfk");
  for(let i=1; i<=47; i++){
    
    if(i==2 || i==8 || i==16 || i==19 || i==25 || i==31 || i==36 || i==40){ //東北
      var separator = document.createElement("option");
      separator.value =  (i==2 ? '91' : (i==8 ? '92' : (i==16 ? '93' : (i==19 ? '94' : (i==25 ? '95' : (i==31 ? '96' : (i==36 ? '97' : (i==40 ? '97' : '')))))))); //"91";
      separator.text = (i==2 ? '─── 東北地方 ───' : (i==8 ? '─── 関東地方 ───' : (i==16 ? '─── 北陸地方 ───' : (i==19 ? '─── 中部地方 ───' : (i==25 ? '─── 関西地方 ───' : (i==31 ? '─── 中国地方 ───' : (i==36 ? '─── 四国地方 ───' : (i==40 ? '─── 九州地方 ───' : '')))))))); //"91";
      separator.setAttribute("disabled","disabled");
      select.appendChild(separator);
    }

    var option = document.createElement("option");
    var val = ( '0' + i).slice(-2);
    option.value = val;
    option.text = c_tdfk[val];
    select.appendChild(option);
  }
}

const c_tdfk = {
  "01" : "北海道"   ,"02" : "青森県"   ,"03" : "岩手県"   ,"04" : "宮城県"   ,"05" : "秋田県"   ,"06" : "山形県"   ,"07" : "福島県"   ,"08" : "茨城県"   ,
  "09" : "栃木県"   ,"10" : "群馬県"   ,"11" : "埼玉県"   ,"12" : "千葉県"   ,"13" : "東京都"   ,"14" : "神奈川県" ,"15" : "新潟県"   ,"16" : "富山県"   ,
  "17" : "石川県"   ,"18" : "福井県"   ,"19" : "山梨県"   ,"20" : "長野県"   ,"21" : "岐阜県"   ,"22" : "静岡県"   ,"23" : "愛知県"   ,"24" : "三重県"   ,
  "25" : "滋賀県"   ,"26" : "京都府"   ,"27" : "大阪府"   ,"28" : "兵庫県"   ,"29" : "奈良県"   ,"30" : "和歌山県" ,"31" : "鳥取県"   ,"32" : "島根県"   ,
  "33" : "岡山県"   ,"34" : "広島県"   ,"35" : "山口県"   ,"36" : "徳島県"   ,"37" : "香川県"   ,"38" : "愛媛県"   ,"39" : "高知県"   ,"40" : "福岡県"   ,
  "41" : "佐賀県"   ,"42" : "長崎県"   ,"43" : "熊本県"   ,"44" : "大分県"   ,"45" : "宮崎県"   ,"46" : "鹿児島県" ,"47" : "沖縄県"
};







function dispLoading(){
  var bg = document.getElementById('loader-bg');
  var loader = document.getElementById('loader');
  bg.classList.remove('is-hide');
  loader.classList.remove('is-hide');
  bg.classList.remove('fadeout-bg');
  loader.classList.remove('fadeout-loader');
}



//dispLoading();

/* 読み込み完了 */
//window.addEventListener('load', UndispLoading);

/* 10秒経ったら強制的にロード画面を非表示にする */
//setTimeout('UndispLoading()',10000);

/* ロード画面を非表示にする処理 */
function UndispLoading(){
  var bg = document.getElementById('loader-bg');
  var loader = document.getElementById('loader');
    bg.classList.add('fadeout-bg');
    loader.classList.add('fadeout-loader');
    bg.classList.add('is-hide');
    loader.classList.add('is-hide');
}









function formatCategory1(str){
  var ret = str;
  var ind = ret.indexOf("(");
  if(ind >= 0){
    ret = ret.substring(0,ind);
  }
  ret = ret.replace("十六　","16 ");
  ret = ret.replace("十五　","15 ");
  ret = ret.replace("十四　","14 ");
  ret = ret.replace("十三　","13 ");
  ret = ret.replace("十二　","12 ");
  ret = ret.replace("十一　","11 ");
  ret = ret.replace("十　","10 ");
  ret = ret.replace("九　","9 ");
  ret = ret.replace("八　","8 ");
  ret = ret.replace("七　","7 ");
  ret = ret.replace("六　","6 ");
  ret = ret.replace("五　","5 ");
  ret = ret.replace("四　","4 ");
  ret = ret.replace("三　","3 ");
  ret = ret.replace("二　","2 ");
  ret = ret.replace("一　","1 ");

  return ret;
}

function formatCategory2(str){
  var ret = str;
  ret = ret.replace("十六　","16 ");
  ret = ret.replace("十五　","15 ");
  ret = ret.replace("十四　","14 ");
  ret = ret.replace("十三　","13 ");
  ret = ret.replace("十二　","12 ");
  ret = ret.replace("十一　","11 ");
  ret = ret.replace("十　","10 ");
  ret = ret.replace("九　","9 ");
  ret = ret.replace("八　","8 ");
  ret = ret.replace("七　","7 ");
  ret = ret.replace("六　","6 ");
  ret = ret.replace("五　","5 ");
  ret = ret.replace("四　","4 ");
  ret = ret.replace("三　","3 ");
  ret = ret.replace("二　","2 ");
  ret = ret.replace("一　","1 ");

  ret = ret.replace("公有財産(土地・建物)","土地・建物");

  return ret;
}



function formatCategory3(str){
  var ret = str;
  var ind = ret.indexOf("(");
  if(ind < 0 ){
    ind = ret.indexOf("（");
  }

  if(ind >= 0){
    ret = ret.substring(0,ind);
  }

  return ret;
}



function formatCategory4(str){
  var ret = str;
  if(!isNaN(ret)){
    ret  = "";
  }
  ret = ret.substring(0,12);
  return ret;
}


function formatCategory5(str){
  var ret = str;
  if(!isNaN(ret)){
    ret  = "";
  }
  ret = ret.replace("土地（地積　㎡）","土地（㎡）");
  ret = ret.replace("建物（延面積　㎡）","建物（㎡）");
  return ret;
}




function formatCategory6(str){
  var ret = str;
  if(!isNaN(ret)){
    ret  = "";
  }
  ret = ret.replace("土地（地積　㎡）","土地（㎡）");
  ret = ret.replace("建物（延面積　㎡）","建物（㎡）");
  return ret;
}



function formatCategoryValue(str){
  var ret = Number(str);
  if(!isNaN(ret)){
    ret = ret.toLocaleString();
  }
  return ret;
}


