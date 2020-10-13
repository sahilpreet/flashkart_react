////////////// for sub-category ul start ////////////////
document.querySelectorAll('header .menu-wrap .menu ul li.category').forEach(item => {
    item.addEventListener('click', (element) => {
        // element.preventDefault()
        // console.log(element.srcElement.children[0])
        if (element.srcElement.children[0].style.display == "block") {
            console.log(element.srcElement.children[0]);
            element.srcElement.children[0].style.display = "none"
        } else {
            element.srcElement.children[0].style.display = "block"
        }
    })
})
////////////// for sub-category ul end ////////////////

/*////////////////////              seach bar start                /////////////////////////*/
document.querySelector(".search-btn .search-symbol").addEventListener('click',(element)=>{
    element.preventDefault()
})
document.querySelector(".search-btn .search-symbol-hide").addEventListener('click',(element)=>{
    element.preventDefault()
    if(document.querySelector(".product-search .search-text").style.display=="none"){
        document.querySelector(".product-search .search-text").style.display="block"
        document.querySelector(".comp-name").style.display="none"
    }
    else{
        document.querySelector(".product-search").submit();
    }
})
function searchFunction(){
    if (x.matches) { // If media query matches
        document.querySelector(".product-search .search-text").style.display="none"
    } else {
        document.querySelector(".product-search .search-text").style.display="block"
    }
}
var x = window.matchMedia("(max-width: 650px)")
searchFunction(x) // Call listener function at run time
x.addListener(searchFunction) // Attach listener function on state changes
/*///////////////              seach bar end                /////////////////////////*/