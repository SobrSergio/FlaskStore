
const burgerMenu =  document.querySelector('.menu__burger');
if(burgerMenu) {
    const menuBody =  document.querySelector('.menu__body');
    burgerMenu.addEventListener("click", function(e) { 
        burgerMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
    });
}

const inputsearch = document.querySelector('.input-search');
 const btnsearch = document.querySelector('.btn-search');
 if (btnsearch) {
    btnsearch.addEventListener("click", function(e) {
        btnsearch.classList.toggle('_active');
        inputsearch.classList.toggle('_active');
     })
 }


 function yesnoCheck() {
    var value = document.querySelector("[name='delivery']:checked").value;
  
    if (value === "Доставка курьером +300 рублей") {
      document.querySelector(".display_none").style.display = "flex";
    } else {
      document.querySelector(".display_none").style.display = "none";
    }
  }
  
  var form = document.querySelector("#formId");
  form.addEventListener("change", yesnoCheck);