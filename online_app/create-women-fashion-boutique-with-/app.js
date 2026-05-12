// Define the PRODUCTS array
const PRODUCTS = [
  // ... (your products array)
];

// Initialize cart and wishlist from local storage
let cart = JSON.parse(localStorage.getItem('cart') || '[]');
let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');

// Function to render products
function renderProducts(filter, sortBy) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';

  const filteredProducts = PRODUCTS.filter((product) => {
    if (filter === 'all') return true;
    return product.cat === filter;
  });

  const sortedProducts = filteredProducts.sort((a, b) => {
    if (sortBy === 'price') return a.price - b.price;
    if (sortBy === 'rating') return b.rating - a.rating;
    if (sortBy === 'discount') return (a.mrp - a.price) / a.mrp - (b.mrp - b.price) / b.mrp;
  });

  sortedProducts.forEach((product) => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');

    const productImage = document.createElement('img');
    productImage.src = product.img;
    productCard.appendChild(productImage);

    const productInfo = document.createElement('div');
    productInfo.classList.add('product-info');
    productCard.appendChild(productInfo);

    const productName = document.createElement('h2');
    productName.textContent = product.name;
    productInfo.appendChild(productName);

    const productPrice = document.createElement('p');
    productPrice.textContent = `Price: $${product.price}`;
    productInfo.appendChild(productPrice);

    const productRating = document.createElement('p');
    productRating.textContent = `Rating: ${product.rating}/5`;
    productInfo.appendChild(productRating);

    const addToCartButton = document.createElement('button');
    addToCartButton.textContent = 'Add to Cart';
    addToCartButton.onclick = () => addToCart(product.id);
    productInfo.appendChild(addToCartButton);

    const wishlistButton = document.createElement('button');
    wishlistButton.textContent = 'Add to Wishlist';
    wishlistButton.onclick = () => toggleWishlist(product.id);
    productInfo.appendChild(wishlistButton);

    productGrid.appendChild(productCard);
  });
}

// Function to add to cart
function addToCart(id) {
  const product = PRODUCTS.find((product) => product.id === id);
  if (cart.includes(product)) {
    showToast('Product already in cart', 'error');
    return;
  }
  cart.push(product);
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
  showToast('Product added to cart', 'success');
}

// Function to toggle wishlist
function toggleWishlist(id) {
  const product = PRODUCTS.find((product) => product.id === id);
  if (wishlist.includes(product)) {
    wishlist = wishlist.filter((product) => product.id !== id);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showToast('Product removed from wishlist', 'success');
  } else {
    wishlist.push(product);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showToast('Product added to wishlist', 'success');
  }
}

// Function to open product modal
function openProduct(id) {
  const product = PRODUCTS.find((product) => product.id === id);
  const productModal = document.getElementById('product-modal');
  productModal.innerHTML = '';

  const productImage = document.createElement('img');
  productImage.src = product.img;
  productModal.appendChild(productImage);

  const productInfo = document.createElement('div');
  productInfo.classList.add('product-info');
  productModal.appendChild(productInfo);

  const productName = document.createElement('h2');
  productName.textContent = product.name;
  productInfo.appendChild(productName);

  const productPrice = document.createElement('p');
  productPrice.textContent = `Price: $${product.price}`;
  productInfo.appendChild(productPrice);

  const productRating = document.createElement('p');
  productRating.textContent = `Rating: ${product.rating}/5`;
  productInfo.appendChild(productRating);

  const productDescription = document.createElement('p');
  productDescription.textContent = 'This is a product description';
  productInfo.appendChild(productDescription);

  productModal.style.display = 'block';
}

// Function to open cart
function openCart() {
  const cartPanel = document.getElementById('cart-panel');
  cartPanel.style.display = 'block';
}

// Function to close cart
function closeCart() {
  const cartPanel = document.getElementById('cart-panel');
  cartPanel.style.display = 'none';
}

// Function to update cart UI
function updateCartUI() {
  const cartPanel = document.getElementById('cart-panel');
  cartPanel.innerHTML = '';

  const cartItems = document.createElement('div');
  cartItems.classList.add('cart-items');
  cartPanel.appendChild(cartItems);

  cart.forEach((product) => {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart-item');
    cartItems.appendChild(cartItem);

    const productImage = document.createElement('img');
    productImage.src = product.img;
    cartItem.appendChild(productImage);

    const productInfo = document.createElement('div');
    productInfo.classList.add('product-info');
    cartItem.appendChild(productInfo);

    const productName = document.createElement('h2');
    productName.textContent = product.name;
    productInfo.appendChild(productName);

    const productPrice = document.createElement('p');
    productPrice.textContent = `Price: $${product.price}`;
    productInfo.appendChild(productPrice);

    const removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.onclick = () => {
      cart = cart.filter((product) => product.id !== product.id);
      localStorage.setItem('cart', JSON.stringify(cart));
      updateCartUI();
    };
    productInfo.appendChild(removeButton);
  });

  const total = document.createElement('p');
  total.textContent = `Total: $${cart.reduce((acc, product) => acc + product.price, 0)}`;
  cartPanel.appendChild(total);
}

// Function to place order
function placeOrder() {
  if (cart.length === 0) {
    showToast('Cart is empty', 'error');
    return;
  }
  const paymentModal = document.getElementById('payment-modal');
  paymentModal.style.display = 'block';
}

// Function to handle payment
function handlePayment(method) {
  const paymentModal = document.getElementById('payment-modal');
  paymentModal.style.display = 'none';
  const successScreen = document.getElementById('success-screen');
  successScreen.style.display = 'block';
  cart = [];
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
}

// Function to search products
function searchProducts(query) {
  const searchResults = PRODUCTS.filter((product) => product.name.toLowerCase().includes(query.toLowerCase()));
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';

  searchResults.forEach((product) => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productGrid.appendChild(productCard);

    const productImage = document.createElement('img');
    productImage.src = product.img;
    productCard.appendChild(productImage);

    const productInfo = document.createElement('div');
    productInfo.classList.add('product-info');
    productCard.appendChild(productInfo);

    const productName = document.createElement('h2');
    productName.textContent = product.name;
    productInfo.appendChild(productName);

    const productPrice = document.createElement('p');
    productPrice.textContent = `Price: $${product.price}`;
    productInfo.appendChild(productPrice);

    const productRating = document.createElement('p');
    productRating.textContent = `Rating: ${product.rating}/5`;
    productInfo.appendChild(productRating);
  });
}

// Function to filter by category
function filterByCategory(cat) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';

  const filteredProducts = PRODUCTS.filter((product) => product.cat === cat);

  filteredProducts.forEach((product) => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productGrid.appendChild(productCard);

    const productImage = document.createElement('img');
    productImage.src = product.img;
    productCard.appendChild(productImage);

    const productInfo = document.createElement('div');
    productInfo.classList.add('product-info');
    productCard.appendChild(productInfo);

    const productName = document.createElement('h2');
    productName.textContent = product.name;
    productInfo.appendChild(productName);

    const productPrice = document.createElement('p');
    productPrice.textContent = `Price: $${product.price}`;
    productInfo.appendChild(productPrice);

    const productRating = document.createElement('p');
    productRating.textContent = `Rating: ${product.rating}/5`;
    productInfo.appendChild(productRating);
  });
}

// Function to sort products
function sortProducts(by) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';

  const sortedProducts = PRODUCTS.sort((a, b) => {
    if (by === 'price') return a.price - b.price;
    if (by === 'rating') return b.rating - a.rating;
    if (by === 'discount') return (a.mrp - a.price) / a.mrp - (b.mrp - b.price) / b.mrp;
  });

  sortedProducts.forEach((product) => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productGrid.appendChild(productCard);

    const productImage = document.createElement('img');
    productImage.src = product.img;
    productCard.appendChild(productImage);

    const productInfo = document.createElement('div');
    productInfo.classList.add('product-info');
    productCard.appendChild(productInfo);

    const productName = document.createElement('h2');
    productName.textContent = product.name;
    productInfo.appendChild(productName);

    const productPrice = document.createElement('p');
    productPrice.textContent = `Price: $${product.price}`;
    productInfo.appendChild(productPrice);

    const productRating = document.createElement('p');
    productRating.textContent = `Rating: ${product.rating}/5`;
    productInfo.appendChild(productRating);
  });
}

// Function to show toast notification
function showToast(msg, type) {
  const toast = document.createElement('div');
  toast.classList.add('toast');
  if (type === 'success') toast.classList.add('success');
  if (type === 'error') toast.classList.add('error');
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 2000);
}

// Function to create banner carousel
function bannerCarousel() {
  const banners = [
    'https://picsum.photos/seed/banner1/300/300',
    'https://picsum.photos/seed/banner2/300/300',
    'https://picsum.photos/seed/banner3/300/300',
  ];
  const bannerContainer = document.getElementById('banner-container');
  let currentBanner = 0;

  function showBanner() {
    const banner = document.createElement('img');
    banner.src = banners[currentBanner];
    bannerContainer.innerHTML = '';
    bannerContainer.appendChild(banner);
    currentBanner = (currentBanner + 1) % banners.length;
  }

  showBanner();
  setInterval(showBanner, 3000);
}

// Initialize the application
renderProducts('all', 'price');
updateCartUI();
bannerCarousel();

// Add event listeners
document.getElementById('search-input').addEventListener('input', (e) => {
  searchProducts(e.target.value);
});

document.getElementById('filter-button').addEventListener('click', () => {
  filterByCategory('Electronics');
});

document.getElementById('sort-button').addEventListener('click', () => {
  sortProducts('price');
});

document.getElementById('cart-button').addEventListener('click', () => {
  openCart();
});

document.getElementById('close-cart-button').addEventListener('click', () => {
  closeCart();
});

document.getElementById('place-order-button').addEventListener('click', () => {
  placeOrder();
});

document.getElementById('payment-button').addEventListener('click', () => {
  handlePayment('credit-card');
});

<!-- HTML structure for the application -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ecommerce Site</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <nav>
      <ul>
        <li><a href="#">Home</a></li>
        <li><a href="#">Electronics</a></li>
        <li><a href="#">Fashion</a></li>
        <li><a href="#">Home</a></li>
        <li><a href="#">Toys</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <section id="banner-container"></section>
    <section id="product-grid"></section>
    <section id="cart-panel">
      <h2>Cart</h2>
      <button id="close-cart-button">Close</button>
      <div id="cart-items"></div>
      <p id="total"></p>
      <button id="place-order-button">Place Order</button>
    </section>
    <section id="payment-modal">
      <h2>Payment</h2>
      <button id="payment-button">Pay with Credit Card</button>
    </section>
    <section id="success-screen">
      <h2>Order Placed Successfully!</h2>
    </section>
  </main>
  <script src="script.js"></script>
</body>
</html>

/* CSS styles for the application */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

header {
  background-color: #333;
  color: #fff;
  padding: 1em;
  text-align: center;
}

nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: space-between;
}

nav li {
  margin-right: 20px;
}

nav a {
  color: #fff;
  text-decoration: none;
}

#banner-container {
  height: 300px;
  width: 100%;
  background-size: cover;
  background-position: center;
}

#product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
  padding: 20px;
}

.product-card {
  background-color: #fff;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.product-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 10px 10px 0 0;
}

.product-info {
  padding: 20px;
}

.product-info h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.product-info p {
  font-size: 14px;
  margin-bottom: 20px;
}

#cart-panel {
  position: fixed;
  top: 0;
  right: 0;
  background-color: #fff;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: none;
}

#cart-items {
  padding: 20px;
}

#total {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

#place-order-button {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

#payment-modal {
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  display: none;
  justify-content: center;
  align-items: center;
}

#payment-modal h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

#payment-button {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

#success-screen {
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
  display: none;
  justify-content: center;
  align-items: center;
}

#success-screen h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.toast {
  position: fixed;
  top: 0;
  right: 0;
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border-radius: 10px;
  margin: 10px;
}

.success {
  background-color: #4CAF50;
}

.error {
  background-color: #f44336;
}