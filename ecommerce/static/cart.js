/* /////////////////////////         first function then call func               /////////////////////////////*/
async function postData(product_id){
    url = "{% url 'ecommerce:cart_remove_ajax' %}"
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
    //console.log(data,'aaaa')
    if(data){
        if(data.cart){

        }else{
            data.cart=0
        }
        //console.log(data.cart)
        document.querySelector(`#product-${product_id}`).style.display='none'
        document.querySelector('.cart-value').innerText=data.cart
        //for price decrease
        total_price=parseFloat(total_price_obj.innerText)
        //console.log(total_price)
        product_to_subtract=parseFloat(document.querySelector(`#product-price-${product_id}`).innerText)
        //console.log(total_price,product_to_subtract)
        total_price=total_price - product_to_subtract
        if(total_price<=0){
            total_price=0
        }
        total_price_obj.innerText=total_price.toFixed(2)
    }
}
//////////////           function for btn-cart start                 ////////////////
var total_price_obj=document.querySelector('#total-price')

document.querySelectorAll('.btn-cart').forEach(item => {
    // console.log(item)
    item.addEventListener('click',(element)=>{
        element.preventDefault()
        if(total_price_obj.innerText <= 0){
            //console.log("returning")
            return;
        }
        if(element.srcElement.id=='remove-all'){
            products_all=document.querySelectorAll(".btn-cart")
            for (element of products_all) {
                if(element.id=='remove-all'){
                    document.querySelector('.cart-value').innerText=0
                    continue;
                }
                //console.log(element)
                element.click()
            }
        }
        try{
            product_id=element.srcElement.parentNode.children[0].innerText
            //console.log(product_id)
            postData(product_id)
        }catch(TypeError){
            //console.log("error"+product_id)            
            return;
        }
    })
})
//////////////         function for btn-cart end                    ////////////////


