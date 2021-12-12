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

// function dispLoading(){
//   document.querySelector('.container-fluid').style.display = "block";
//   //document.querySelector('#loading').
//   //document.querySelector('#spinner').
//   //$('#wrap').css('display', 'block');
//   //$('#loading').delay(500).fadeOut(500);
//   //$('#spinner').delay(300).fadeOut(300);
// }

// function hideLoading(){
//   document.querySelector('.container-fluid').style.display = "block";
//   //$('#wrap').css('display','block');
//   //$('#loading').delay(500).fadeOut(500);
//   //$('#spinner').delay(300).fadeOut(300);
// }

// $(function() {
//   var h = $(window).height();

//   $('#wrap').css('display','none');
//   $('#loading ,#spinner').height(h).css('display','block');
// });

// function dispLoading(){
//   document.querySelector('.container-fluid').style.display = "block";
//   //$('#loading').delay(500).fadeOut(500);
//   //$('#spinner').delay(300).fadeOut(300);
// }

// setTimeout('stopload()',5000);

// function stopload(){
//   document.querySelector('.container-fluid').style.display = "block";
//   // $('#loading').delay(500).fadeOut(500);
//   // $('#spinner').delay(300).fadeOut(300);
// }



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
  //document.querySelector('.container-fluid').style.display = "none";
  document.querySelector('#loading').style.display = "block";
  //document.querySelector('#spinner').style.display = "block";
}




function UndispLoading(){
  document.querySelector('.container-fluid').style.display = "";
  document.querySelector('#loading').style.display = "none";
  document.querySelector('#loading').delay(500).fadeOut(500);
  //document.querySelector('#spinner').style.display = "none";
}











  // //ローディングロゴエリアとウインドウの高さを取得
  // let loadlogo = document.querySelector('.loading-logo'),
  //     winH = window.innerHeight;

  // //スマホでアドレスバーの分ロゴの位置がずれるので高さを調整
  // loadlogo.style.height = winH + 'px';

  // //ページ読み込み完了でローディング画面を非表示
  // window.addEventListener('load', stopload);

  // //10秒経過で強制的にローディング画面を非表示
  // setTimeout('stopload()',10000);

  // //ローディング画面を非表示にする処理
  // function stopload() {
  //   //ローディング画面とページを取得
  //   let loader = document.querySelector('#loading'),
  //       page = document.querySelector('#page');

  //   //ローディング画面とページにクラスを追加
  //   page.classList.add('is-loaded');
  //   loader.classList.add('is-loaded');
  // }



  var bg = document.getElementById('loader-bg'),
    loader = document.getElementById('loader');
/* ロード画面の非表示を解除 */
bg.classList.remove('is-hide');
loader.classList.remove('is-hide');

/* 読み込み完了 */
window.addEventListener('load', stopload);

/* 10秒経ったら強制的にロード画面を非表示にする */
setTimeout('stopload()',10000);

/* ロード画面を非表示にする処理 */
function stopload(){
    bg.classList.add('fadeout-bg');
    loader.classList.add('fadeout-loader');
}