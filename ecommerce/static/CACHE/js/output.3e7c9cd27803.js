document.querySelectorAll('header .menu-wrap .menu ul li.category').forEach(item=>{item.addEventListener('click',(element)=>{if(element.srcElement.children[0].style.display=="block"){console.log(element.srcElement.children[0]);element.srcElement.children[0].style.display="none"}else{element.srcElement.children[0].style.display="block"}})})
document.querySelector(".search-btn .search-symbol").addEventListener('click',(element)=>{element.preventDefault()})
document.querySelector(".search-btn .search-symbol-hide").addEventListener('click',(element)=>{element.preventDefault()
if(document.querySelector(".product-search .search-text").style.display=="none"){document.querySelector(".product-search .search-text").style.display="block"
document.querySelector(".comp-name").style.display="none"}
else{document.querySelector(".product-search").submit();}})
function searchFunction(){if(x.matches){document.querySelector(".product-search .search-text").style.display="none"}else{document.querySelector(".product-search .search-text").style.display="block"}}
var x=window.matchMedia("(max-width: 650px)")
searchFunction(x)
x.addListener(searchFunction);document.querySelectorAll('.container-cards-slides .prev').forEach(item=>{item.addEventListener('click',(element)=>{console.log(element.srcElement.parentNode)
element.srcElement.parentNode.children[0].scrollBy(-window.innerWidth/1.3,0)});});document.querySelectorAll('.container-cards-slides .next').forEach(item=>{item.addEventListener('click',(element)=>{console.log(element.srcElement.parentNode)
element.srcElement.parentNode.children[0].scrollBy(window.innerWidth/1.3,0)});});async function postData(product_id){url="/cart_add_ajax"
bodyData={product_id:product_id}
params={method:"post",credentials:'same-origin',credentials:'include',body:JSON.stringify(bodyData),headers:{'X-CSRFToken':"U3LcwKBITVkiW4IkMZocnf4woRsnshDaQnr1SfawPphHm2WYEwOOY0WxNFSUxM6W",'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Accept':'application/json','X-Requested-With':'XMLHttpRequest'},}
const response=await fetch(url,params)
const data=await response.json()
document.querySelector('.cart-value').innerText=data.cart}
document.querySelector('.btn .btn-cart').addEventListener('click',(element)=>{element.preventDefault()
if("sahilpreetsingh9915545834@gmail.com"=='AnonymousUser'){window.location.href="/register";console.log("redirect")
return;}
product_id=element.srcElement.parentNode.children[0].innerText
postData(product_id)});