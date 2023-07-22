import React, { SyntheticEvent, useState, useEffect, PropsWithRef } from 'react'
import Layout from './Layout'
import { Navigate, useLocation } from 'react-router-dom';
import { Product } from '../interfaces/product';

const ProductsEdit = () => {
    const location = useLocation()
    const productId = location.state;

    const [title, setTitle] = useState("");
    const [image, setImage] = useState("");
    const [redirect, setRedirect] = useState(false);


    useEffect(() => {
        (
            async () => {
                const response = await fetch(`http://localhost:8000/api/products/${productId}`);
                const product: Product = await response.json();
                setTitle(product.title);
                setImage(product.image);
            }
        )();
    }, []);

    const submit = async (e: SyntheticEvent) => {
        e.preventDefault();
        await fetch(`http://localhost:8000/api/products/${productId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                image
            })
        });

        setRedirect(true);
    }

    if (redirect) {
        return <Navigate to={'/admin/products'} />
    }

    return (
        <Layout>
            <form onSubmit={submit}>
                <h3 className='mt-3 mb-3'>Edit Product</h3>
                <div className='form-group'>
                    <label>Title</label>
                    <input type='text' className='form-control' name='title'
                        defaultValue={title}
                        onChange={e => setTitle(e.target.value)}></input>
                </div>
                <div className='form-group'>
                    <label>Image</label>
                    <input type='text' className='form-control' name='image'
                        defaultValue={image}
                        onChange={e => setImage(e.target.value)}></input>
                </div>
                <button className='btn btn-outline-secondary'>Save</button>
            </form>
        </Layout>
    )
}

export default ProductsEdit