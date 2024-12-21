// Cart object to keep track of added items
let cart = [];
let totalAmount = 0; // Variable to keep track of the total amount

// Function to add item to cart
function addToCart(itemName, itemPrice, quantity) {
    // Validate quantity
    quantity = parseInt(quantity);
    if (isNaN(quantity) || quantity <= 0) {
        alert("Please enter a valid quantity.");
        return;
    }

    const totalPrice = itemPrice * quantity;
    
    // Create item object
    const cartItem = {
        name: itemName,
        price: itemPrice,
        quantity: quantity,
        totalPrice: totalPrice
    };
    
    // Add item to cart array
    cart.push(cartItem);

    // Update total amount
    totalAmount += totalPrice;

    // Update cart display
    updateCart();
}

// Function to update the cart display
function updateCart() {
    const cartItemsDiv = document.getElementById('cart-items');
    const cartTotalDiv = document.getElementById('cart-total');

    // Clear current cart display
    cartItemsDiv.innerHTML = "";

    // Add items to cart display
    cart.forEach(item => {
        cartItemsDiv.innerHTML += `
            <div class="cart-item">
                <span class="item-name">${item.name}</span>
                <span class="item-quantity">x ${item.quantity}</span>
                <span class="item-total">$${item.totalPrice.toFixed(2)}</span>
            </div>
        `;
    });

    // Update total
    cartTotalDiv.innerHTML = `Total: $${totalAmount.toFixed(2)}`;
}

// Checkout function
function checkout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    // Proceed to checkout (for now just display alert)
    alert("Proceeding to checkout...");
    // Here you could redirect to a checkout page or handle the checkout process.
}
