document.querySelectorAll('header .menu-wrap .menu ul li.category').forEach(item=>{item.addEventListener('click',(element)=>{if(element.srcElement.children[0].style.display=="block"){console.log(element.srcElement.children[0]);element.srcElement.children[0].style.display="none"}else{element.srcElement.children[0].style.display="block"}})})
document.querySelector(".search-btn .search-symbol").addEventListener('click',(element)=>{element.preventDefault()})
document.querySelector(".search-btn .search-symbol-hide").addEventListener('click',(element)=>{element.preventDefault()
if(document.querySelector(".product-search .search-text").style.display=="none"){document.querySelector(".product-search .search-text").style.display="block"
document.querySelector(".comp-name").style.display="none"}
else{document.querySelector(".product-search").submit();}})
function searchFunction(){if(x.matches){document.querySelector(".product-search .search-text").style.display="none"}else{document.querySelector(".product-search .search-text").style.display="block"}}
var x=window.matchMedia("(max-width: 650px)")
searchFunction(x)
x.addListener(searchFunction);async function postData(product_id){url="/cart_remove_ajax"
bodyData={product_id:product_id}
params={method:"post",credentials:'same-origin',credentials:'include',body:JSON.stringify(bodyData),headers:{'X-CSRFToken':"PrRn0fwLnGGgIARCFsQxtdy78uBCG7H3LLxcmK5zjaDF8y5gxZg94Yq8xi19LCaP",'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Accept':'application/json','X-Requested-With':'XMLHttpRequest'},}
const response=await fetch(url,params)
const data=await response.json()
if(data){if(data.cart){}else{data.cart=0}
document.querySelector(`#product-${product_id}`).style.display='none'
document.querySelector('.cart-value').innerText=data.cart
total_price=parseFloat(total_price_obj.innerText)
product_to_subtract=parseFloat(document.querySelector(`#product-price-${product_id}`).innerText)
total_price=total_price-product_to_subtract
if(total_price<=0){document.querySelector('.cart-value').innerText=0
total_price=0}
total_price_obj.innerText=total_price.toFixed(2)}}
var total_price_obj=document.querySelector('#total-price')
document.querySelectorAll('.btn-cart').forEach(item=>{item.addEventListener('click',(element)=>{element.preventDefault()
if(total_price_obj.innerText<=0){return;}
if(element.srcElement.id=='remove-all'){products_all=document.querySelectorAll(".btn-cart")
for(element of products_all){if(element.id=='remove-all'){continue;}
element.click()}}
try{product_id=element.srcElement.parentNode.children[0].innerText
postData(product_id)}catch(TypeError){return;}})});