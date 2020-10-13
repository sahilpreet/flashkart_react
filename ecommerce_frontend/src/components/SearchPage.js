import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './css/category.css'
import axios from 'axios'
import HeaderComponent from "./Header";
import FooterComponent from "./Footer";
import PaginationComponent from "./PaginationComponent";
import CategoryList from "./CategoryList";

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

function SearchPage(props) {
    const [urlparams, seturlparams] = useState(`http://127.0.0.1:8000/api/search/${props.location.search.replace("?", "")}`)
    // seturlparams(`http://127.0.0.1:8000/api/search/${locationsearch}`)
    const [categoryapi, setcategoryapi] = useState('')
    const [cartvalue, setcartvalue] = useState(0)
    const [pageno, setpageno] = useState(1)
    const [prevurl, setprevurl] = useState('')
    const [nexturl, setnexturl] = useState('')
    const [productapi, setproductapi] = useState([])
    useEffect(() => {
        seturlparams((prevState)=>`http://127.0.0.1:8000/api/search/${props.location.search.replace("?", "")}`)
        // console.log(urlparams,props.location.search.replace("?", ""))
        if (props.location.search.replace("?", "")) {
            const csrftoken = getCookie('csrftoken')
            axios.get(`${urlparams}`, {
                headers: {
                    'Authorization': `${getCookie('token')}`,
                    'X-CSRFToken': csrftoken,
                    // "Cookie":document.cookie
                    //withCredentials: true
                },
            }).then((response) => {
                //console.log(response.data, "in cat")
                setproductapi(response.data.results.products)
                // setcategoryapi(JSON.parse(response.data.results.categories))
                setcategoryapi(response.data.results.categories.dictionary)
                setcartvalue(response.data.results.cart)
                setprevurl(response.data.previous)
                setnexturl(response.data.next)
                if (response.data.next) {
                    const reg = /offset=[0-9]+/i
                    const reg_pageno = /[0-9]/i
                    let match_offset_page_value = 1
                    try {
                        match_offset_page_value = parseInt(reg_pageno.exec(reg.exec(response.data.next)[0])[0])
                    } catch (error) {
                        return
                    }
                    setpageno(match_offset_page_value)
                } else if (response.data.next === null && response.data.previous === null) {
                    setpageno(1)
                }
                else {
                    setpageno((prev) => prev + 1)
                }
            })
                .catch((error) => {
                    console.log(error)
                })
        }
        return () => { }
        //use props carefully with urlparams
    }, [props.location,urlparams])
    const HandleUrlParams = (params) => {
        // console.log(params, "clicked")
        seturlparams(params)
    }
    return (
        <>
            <HeaderComponent categoryapi={categoryapi} cartvalue={cartvalue} />
            {productapi &&
                <ul className="breadcrumb">
                    <li key="0"><Link to="/react">Home</Link></li>
                    <li key="1">Search</li>
                </ul>
            }
            <CategoryList productapi={productapi} />
            <PaginationComponent prevurl={prevurl} nexturl={nexturl} pageno={pageno} clickfunc={HandleUrlParams} />
            <FooterComponent />
        </>
    )
}

export default React.memo(SearchPage)


