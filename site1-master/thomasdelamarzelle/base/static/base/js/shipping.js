var shipping = '{{order.shipping}}'
console.log("'{{order.shipping}}'")
console.log(shipping)

    if (shipping == 'False' ){
        document.getElementById('shipping-info').innerHTML = ''
        console.log('shipping is False')
        }
    else{
    console.log('shipping is True')}