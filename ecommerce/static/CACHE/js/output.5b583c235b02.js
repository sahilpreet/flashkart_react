document.querySelectorAll('header .menu-wrap .menu ul li.category').forEach(item=>{item.addEventListener('click',(element)=>{if(element.srcElement.children[0].style.display=="block"){console.log(element.srcElement.children[0]);element.srcElement.children[0].style.display="none"}else{element.srcElement.children[0].style.display="block"}})})
document.querySelector(".search-btn .search-symbol").addEventListener('click',(element)=>{element.preventDefault()})
document.querySelector(".search-btn .search-symbol-hide").addEventListener('click',(element)=>{element.preventDefault()
if(document.querySelector(".product-search .search-text").style.display=="none"){document.querySelector(".product-search .search-text").style.display="block"
document.querySelector(".comp-name").style.display="none"}
else{document.querySelector(".product-search").submit();}})
function searchFunction(){if(x.matches){document.querySelector(".product-search .search-text").style.display="none"}else{document.querySelector(".product-search .search-text").style.display="block"}}
var x=window.matchMedia("(max-width: 650px)")
searchFunction(x)
x.addListener(searchFunction);;function slide_with_time(){let i=1;setInterval(()=>{document.getElementById(`i${i++}`).checked=true;if(i>3){i=1;}},5000)}
slide_with_time()
document.querySelectorAll('.container-cards-slides .prev').forEach(item=>{item.addEventListener('click',(element)=>{console.log(element.srcElement.parentNode)
element.srcElement.parentNode.children[0].scrollBy(-window.innerWidth/1.3,0)});});document.querySelectorAll('.container-cards-slides .next').forEach(item=>{item.addEventListener('click',(element)=>{console.log(element.srcElement.parentNode)
element.srcElement.parentNode.children[0].scrollBy(window.innerWidth/1.3,0)});});