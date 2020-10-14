import React,{useState} from 'react'
import { Link } from 'react-router-dom'
import absolute_url from "./AbsoluteUrl"

function CategoryList({ productapi }) {
    const date=new Date()
    let months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    const [saledate, setsaledate] = useState({
        date:date.getDate()+10,
        month:months[date.getMonth()],
    })
    return (
        <section className="main-category">
            <ul className="products-list">
                {productapi && productapi.map((product, index) => {
                    return (
                        <li key={product.id} className="product">
                            <div className="image">
                                <img src={`${absolute_url}/${product.image}`} alt={`${product.name}`} />
                            </div>
                            <Link to={`/product_react/${product.id}`} className="product-view">
                                <span className="product-name">{product.name}</span>
                                <span className="product-regularprice">$ {product.regular_price}</span>
                                <span className="product-discountedprice"><s>$ {product.discounted_price}</s></span>
                                <span className="delivery-date">Get it by {saledate.month},{saledate.date} <br />
                                    FREE Delivery by Flashkart</span>
                            </Link>
                        </li>
                    )
                })
                }
            </ul>
        </section>
    )
}

export default React.memo(CategoryList)