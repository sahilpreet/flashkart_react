import React,{useEffect,useState} from 'react'
import { Link } from "react-router-dom";
import './css/cart.css'
import axios from 'axios'
import FooterComponent from "./Footer";
import HeaderComponent from './Header'

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

function AboutPage() {
    const [categoryapi, setcategoryapi] = useState([])
    const [cartvalue, setcartvalue] = useState(0)
    useEffect(() => {
        const csrftoken = getCookie('csrftoken');
        axios.get("http://127.0.0.1:8000/api/cart", {
            headers: {
                'Authorization': `${getCookie('token')}`,
                'X-CSRFToken': csrftoken,
                // "Cookie":document.cookie
                //withCredentials: true
            },
        })
            .then((response) => {
                // console.log(response.data, "ajsflkn")
                setcategoryapi(response.data.categories.dictionary)
                // console.log(response.data)
                // setproductlistapi(response.data)
                // setcategoryapi(JSON.parse(response.data.categories))
                // setcartproducts(response.data.cart_all)
                setcartvalue(response.data.cart)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [])
    return (
        <>
        <HeaderComponent categoryapi={categoryapi} cartvalue={cartvalue} />
        <section className="main-about">
        <ul className="breadcrumb">
        <li><Link to="/react">Home</Link></li>
        <li>about</li>
        </ul>
        <p className="para-about">
        This site is in develpoment and has been created by sahilpreet singh
        <br></br>
        <br></br>
        for business queries contact us
        <br></br>
        <br></br>
        Email : sahilpreetsingh9915545834@gmail.com
        </p>
        </section>
        <FooterComponent />
        </>
    )
}

export default React.memo(AboutPage)
