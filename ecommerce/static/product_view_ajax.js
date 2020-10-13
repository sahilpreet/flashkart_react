////////////// function for carousel -cards end ////////////////

document.querySelectorAll('.container-cards-slides .prev').forEach(item => {
// console.log(item)
item.addEventListener('click', (element) => {
console.log(element.srcElement.parentNode)
element.srcElement.parentNode.children[0].scrollBy(-window.innerWidth / 1.3, 0)
});
});
document.querySelectorAll('.container-cards-slides .next').forEach(item => {
// console.log(item)
item.addEventListener('click', (element) => {
console.log(element.srcElement.parentNode)
element.srcElement.parentNode.children[0].scrollBy(window.innerWidth / 1.3, 0)
});
});

////////////// function for carousel -cards start ////////////////

//////////////           function for btn-cart start                 ////////////////
async function postData(product_id){
    url = "{% url 'ecommerce:cart_add_ajax' %}"
    bodyData= {product_id:product_id}
    params={
        method:"post",
        credentials: 'same-origin',
        credentials: 'include',
        body:JSON.stringify(bodyData),
        headers: {
            'X-CSRFToken': "{{csrf_token}}",
            //'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            //'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
    }
    const response=await fetch(url,params)
    const data=await response.json()
    //console.log(data)
    document.querySelector('.cart-value').innerText=data.cart
}

document.querySelector('.btn .btn-cart').addEventListener('click',(element)=>{
    element.preventDefault()
    if("{{request.user}}"=='AnonymousUser'){
        window.location.href = "{% url 'ecommerce:register' %}";
        console.log("redirect")
    }
    //console.log(element.srcElement.parentNode.children[0]);
    product_id=element.srcElement.parentNode.children[0].innerText
    //console.log(product_id)
    postData(product_id)
    
}) 
//////////////         function for btn-cart end                    ////////////////

