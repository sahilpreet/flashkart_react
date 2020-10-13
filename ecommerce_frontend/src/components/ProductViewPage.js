import React, { useState, useEffect } from 'react'
import { Link,useHistory } from 'react-router-dom'
import axios from 'axios'
import "./css/product_view.css"
import FooterComponent from "./Footer";
import HeaderComponent from './Header'
import CarouselCards from "./CarouselCards";

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ProductViewPage({ match }) {
    const [productapi, setproductapi] = useState({})
    const [categoryapi, setcategoryapi] = useState('')
    const [cartvalue, setcartvalue] = useState(0)
    const [productscards, setproductscards] = useState([])
    const history=useHistory()
    //console.log(match.params)
    useEffect(() => {
        const csrftoken = getCookie('csrftoken');
        //console.log("productview")
        try {
            axios.get(`http://127.0.0.1:8000/api/product_view_func/${match.params.id}`, {
                headers: {
                    'Authorization': `${getCookie('token')}`,
                    'X-CSRFToken': csrftoken,
                    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
                    //'Content-Type': 'application/json',
                    Accept: 'application/json',
                    "X-Requested-With": 'XMLHttpRequest',
                    //credentials: 'same-origin',
                    //credentials: 'include',
                    //Host: "127.0.0.1:8000",
                    //"Sec-Fetch-User": "?1",
                }
            })
                .then((response) => {
                    //console.log(response.data.product, "out")
                    // setcategoryapi(JSON.parse(response.data.categories))
                    setcategoryapi(response.data.categories.dictionary)
                    setcartvalue(response.data.cart)
                    setproductapi(response.data.product)
                    setproductscards(response.data.products)
                })
                .catch((error) => {
                    console.log(error)
                })
        } catch (error) {
            return
        }
        return () => { }
    }, [match.params.id])
    // < form action = "{% url 'ecommerce:product_view' object.id %}" method = "post" >
    //     <input className="product-id" type="text" name="product_id" value="{{object.id}}" />
    //     <input className="btn-cart" type="submit" value="Add to Cart" />
    //     <input className="btn-cart" type="submit" value="Buy Now" />
    //                 </form >
    const handleAddToCart = (event) => {
        if (getCookie("token")){
            console.log()
        }else{
            history.push("/register_react")
        }
        // console.log("click", event.target.name)
        const csrftoken = getCookie('csrftoken');
        const url = "http://127.0.0.1:8000/api/cart_add_remove"
        const bodyData = {
            action: "add",
            product_id: event.target.name
        }
        const params = {
            method: "post",
            //credentials: 'same-origin',
            //credentials: 'include',
            body: JSON.stringify(bodyData),
            headers: {
                'Authorization': `${getCookie('token')}`,
                'X-CSRFToken': csrftoken,
                //'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                //'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
        }
        fetch(url, params)
            .then((response) => {
                response.json()
                    .then((response) => {
                        // console.log(respoknse)
                        setcartvalue(response.cart)
                        // document.cookie=`token=${response.token}`
                        // setCookie("token", response.token, 300)
                        // history.push('/react')
                    })
            })
            .catch((error) => {
                console.log(error)
            })
    }
    return (
        <>
            <HeaderComponent categoryapi={categoryapi} cartvalue={cartvalue} />
            {productapi &&
                <ul className="breadcrumb">
                    <li key="0"><Link to="/react">Home</Link></li>
                    <li key="1"><Link to={`/category_react/${productapi.category}`}>{productapi.category}</Link></li>
                    <li key="2"><Link to={`/sub_category_react/${productapi.sub_category}`}>{productapi.sub_category}</Link></li>
                    <li key="3">{productapi.name}</li>
                </ul>
            }
            {productapi &&
                <section className="product-container">
                    <div className="product-image">
                        <img src={`${productapi.image}`} alt={`${productapi.name}`} />
                    </div>
                    <div className="product-details">
                        <span className="product-name">
                            {productapi.name}
                        </span>
                        <span className="product-regularprice">$ {productapi.regular_price}</span>
                        <span className="product-discountedprice"><s>$ {productapi.discounted_price}</s></span>
                        <span className="btn">
                            <button className="btn-cart" name={productapi.id} onClick={handleAddToCart}>Add To Cart</button>
                        </span>
                    </div>
                </section>}
            {productscards && <CarouselCards products={productscards} />}
            <FooterComponent />
        </>
    )
}

export default React.memo(ProductViewPage)
