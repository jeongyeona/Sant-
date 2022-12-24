   const form = document.querySelector('#starform');
   
   form.addEventListener('submit', event => {
   const selectedRadio = document.querySelector('input[type="radio"]:checked');
   
     if (!selectedRadio) {
       alert('아직 선택하지 않았습니다.');
      event.preventDefault();
       return;
     }
   });
   
   const wineid = document.querySelector('#id')

   form.addEventListener('submit', event => {
       if (wineid.value === "") {
          event.preventDefault();
           alert("로그인해주세요");
         }
    });
   
    // DB에서 당도,산미,바디,탄닌을 받아서 시각화
    let sweet=document.querySelector("#WineDetailInfSweet")
    let acidity=document.querySelector("#WineDetailInfacidity")
    let body=document.querySelector("#WineDetailInfbody")
    let tainnin=document.querySelector("#WineDetailInftainnin")  
    let nation=document.querySelector("#winelalanation")
    let nullcount=document.querySelector("#nullcount")
    
    if(nullcount.textContent == 0){
       nullcount.innerHTML= "정보없음"
    }
    
    
      $('#WDclickme3').click(function() {
        $('html, body').animate({
          scrollTop: $('#WDclickme1').offset().top
        }, 1);
      });
    
      $('#WDclickme2').click(function() {
        $('html, body').animate({
          scrollTop: $('#WDclickme4').offset().top
        }, 1);
      });
    
    // 음식 이름 자르기
      nation.textContent = nation.textContent.replace(/-/g, '>');

    let oneicon='<div class="asjoui1h989"><div class="winedetailicon" id="winedetailiconid1"></div><div class="winedetailicon"></div><div class="winedetailicon"></div><div class="winedetailicon"></div><div class="winedetailicon"></div></div>'
    let twoicon='<div class="asjoui1h989"><div class="winedetailicon" id="winedetailiconid1"></div><div class="winedetailicon" id="winedetailiconid2"></div><div class="winedetailicon"></div><div class="winedetailicon"></div><div class="winedetailicon"></div></div>'
    let threeicon='<div class="asjoui1h989"><div class="winedetailicon" id="winedetailiconid1"></div><div class="winedetailicon" id="winedetailiconid2"></div><div class="winedetailicon" id="winedetailiconid3" ></div><div class="winedetailicon"></div><div class="winedetailicon"></div></div>'
    let fouricon='<div class="asjoui1h989"><div class="winedetailicon" id="winedetailiconid1"></div><div class="winedetailicon" id="winedetailiconid2"></div><div class="winedetailicon" id="winedetailiconid3"></div><div class="winedetailicon4" id="winedetailiconid"></div><div class="winedetailicon"></div></div>'
    let fiveicon='<div class="asjoui1h989"><div class="winedetailicon" id="winedetailiconid1"></div><div class="winedetailicon" id="winedetailiconid2"></div><div class="winedetailicon" id="winedetailiconid3"></div><div class="winedetailicon4" id="winedetailiconid"></div><div class="winedetailicon" id="winedetailiconid5"></div></div>'
      
    if(sweet.innerText == 1){
       sweet.innerHTML=oneicon;
    }else if(sweet.innerText == 2){
       sweet.innerHTML=twoicon;
    }else if(sweet.innerText == 3){
       sweet.innerHTML=threeicon;
    }else if(sweet.innerText == 4){
       sweet.innerHTML=fouricon;
    }else{
       sweet.innerHTML=fiveicon;
    }
    
    if(acidity.innerText == 1){
       acidity.innerHTML=oneicon;
    }else if(acidity.innerText == 2){
       acidity.innerHTML=twoicon;
    }else if(acidity.innerText == 3){
       acidity.innerHTML=threeicon;
    }else if(acidity.innerText == 4){
       acidity.innerHTML=fouricon;
    }else{
       acidity.innerHTML=fiveicon;
    }
    
    if(body.innerText == 1){
       body.innerHTML=oneicon;
    }else if(body.innerText == 2){
       body.innerHTML=twoicon;
    }else if(body.innerText == 3){
       body.innerHTML=threeicon;
    }else if(body.innerText == 4){
       body.innerHTML=fouricon;
    }else{
       body.innerHTML=fiveicon;
    }
    
    if(tainnin.innerText == 1){
       tainnin.innerHTML=oneicon;
    }else if(tainnin.innerText == 2){
       tainnin.innerHTML=twoicon;
    }else if(tainnin.innerText == 3){
       tainnin.innerHTML=threeicon;
    }else if(tainnin.innerText == 4){
       tainnin.innerHTML=fouricon;
    }else{
       tainnin.innerHTML=fiveicon;
    }