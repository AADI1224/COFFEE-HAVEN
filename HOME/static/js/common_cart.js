// Get CSRF token from the form or meta tag
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

// Update cart count based on session/cart
function updateCartCount() {
    fetch("/get_cart_count/")
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.getElementById('cart-count');
            if (cartCountElement) {
                cartCountElement.textContent = data.cartCount || 0; // Fallback to 0 if undefined
            } else {
                console.error("Cart count element not found.");
            }
        })
        .catch(error => console.error("Error fetching cart count:", error));
}

// Show notification

// Call showCartNotification when an item is added to the cart
function addToCart(name, price, img, itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    const quantity = quantityElement ? quantityElement.value : 1;

    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
        },
        body: `name=${name}&price=${price}&img=${img}&quantity=${quantity}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.cart) {
            console.log('Item added to cart:', data.cart);
            updateCartCount(); // Update the cart count
            showCartNotification(); // Show the "Added to Cart" message
        } else {
            console.error('Failed to add item to cart:', data.error);
        }
    })
    .catch(error => console.error('Error adding to cart:', error));
}

// Function to remove an item from the cart
function removeFromCart(itemName) {
    const csrfToken = getCsrfToken();

    fetch("/remove_from_cart/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: `item_name=${itemName}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.cart) {
            // Remove the item from the DOM
            const itemDiv = document.getElementById(`cart-item-${itemName}`);
            if (itemDiv) {
                itemDiv.remove();
            }

            // Update total price
            const totalPriceElement = document.querySelector('.total-price h3');
            if (totalPriceElement) {
                totalPriceElement.textContent = `Total: ₹${data.total_price}`;
            }

            // Check if the cart is empty
            if (data.cart.length === 0) {
                document.getElementById('cart').innerHTML = '<p>Your cart is empty.</p>';
            }

            // Update the cart count dynamically
            updateCartCount();
        } else {
            console.error(data.error || 'Error removing item');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Ensure updateCartCount is called on page load and whenever needed
document.addEventListener("DOMContentLoaded", updateCartCount);

document.querySelector('.cart-icon a').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    
    fetch(this.href, { method: 'GET' })
        .then(response => {
            if (response.status === 403) {
                // User is not logged in
                return response.json().then(data => {
                    alert(data.error); // Display an alert or use a modal
                });
            } else {
                // User is logged in, redirect to the cart page
                window.location.href = this.href;
            }
        })
        .catch(error => console.error('Error fetching cart:', error));
});