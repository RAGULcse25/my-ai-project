// Define constants and variables
const PRODUCTS = [
  {id:1,name:"boAt Airdopes 141",price:1299,mrp:4990,rating:4.1,reviews:12453,img:"https://picsum.photos/seed/boat/300/300",cat:"Electronics",badge:"71% off",brand:"boAt"},
  {id:2,name:"Samsung Galaxy M34",price:16999,mrp:24999,rating:4.3,reviews:8765,img:"https://picsum.photos/seed/samsung/300/300",cat:"Electronics",badge:"Best Seller",brand:"Samsung"},
  {id:3,name:"Nike Air Max 270",price:7495,mrp:12995,rating:4.5,reviews:3210,img:"https://picsum.photos/seed/nike270/300/300",cat:"Fashion",badge:"Trending",brand:"Nike"},
  {id:4,name:"Levi's 511 Slim",price:1999,mrp:3999,rating:4.2,reviews:5432,img:"https://picsum.photos/seed/levis/300/300",cat:"Fashion",badge:"50% off",brand:"Levi's"},
  {id:5,name:"OnePlus Nord CE 3",price:16999,mrp:19999,rating:4.2,reviews:9876,img:"https://picsum.photos/seed/oneplus/300/300",cat:"Electronics",badge:"New",brand:"OnePlus"},
  {id:6,name:"Prestige Mixer",price:2199,mrp:4500,rating:4.0,reviews:4567,img:"https://picsum.photos/seed/mixer/300/300",cat:"Home",badge:"51% off",brand:"Prestige"},
  {id:7,name:"Noise ColorFit Pro",price:1999,mrp:6999,rating:4.1,reviews:7890,img:"https://picsum.photos/seed/noise/300/300",cat:"Electronics",badge:"71% off",brand:"Noise"},
  {id:8,name:"Wildcraft Backpack",price:1299,mrp:2999,rating:4.3,reviews:2345,img:"https://picsum.photos/seed/wildcraft/300/300",cat:"Sports",badge:"Deal",brand:"Wildcraft"},
  {id:9,name:"Atomic Habits",price:299,mrp:599,rating:4.8,reviews:45678,img:"https://picsum.photos/seed/atomic/300/300",cat:"Books",badge:"Bestseller",brand:"Penguin"},
  {id:10,name:"Himalaya Face Wash",price:155,mrp:210,rating:4.4,reviews:12345,img:"https://picsum.photos/seed/himalaya/300/300",cat:"Beauty",badge:"Popular",brand:"Himalaya"},
  {id:11,name:"boAt Rockerz 450",price:1299,mrp:3990,rating:4.2,reviews:8900,img:"https://picsum.photos/seed/rockerz/300/300",cat:"Electronics",badge:"67% off",brand:"boAt"},
  {id:12,name:"Puma Sports Shoes",price:3499,mrp:5999,rating:4.4,reviews:2100,img:"https://picsum.photos/seed/puma/300/300",cat:"Fashion",badge:"Sale",brand:"Puma"},
  {id:13,name:"Instant Pot 6Qt",price:8499,mrp:14999,rating:4.7,reviews:6700,img:"https://picsum.photos/seed/instantpot/300/300",cat:"Home",badge:"Top Pick",brand:"Instant Pot"},
  {id:14,name:"Funskool Lego",price:1499,mrp:2499,rating:4.7,reviews:3456,img:"https://picsum.photos/seed/lego/300/300",cat:"Toys",badge:"Gift",brand:"Funskool"},
  {id:15,name:"Yoga Mat Premium",price:899,mrp:1999,rating:4.5,reviews:4300,img:"https://picsum.photos/seed/yoga/300/300",cat:"Sports",badge:"Popular",brand:"Boldfit"},
  {id:16,name:"Philips Air Fryer",price:6995,mrp:10995,rating:4.6,reviews:1234,img:"https://picsum.photos/seed/airfryer/300/300",cat:"Home",badge:"Deal",brand:"Philips"},
];

let cart = JSON.parse(localStorage.getItem('cart')||'[]');
let wishlist = JSON.parse(localStorage.getItem('wishlist')||'[]');

// Function to render products
function renderProducts(filter, sortBy) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';
  let filteredProducts = PRODUCTS;
  if (filter) {
    filteredProducts = filteredProducts.filter(product => product.cat === filter);
  }
  if (sortBy) {
    if (sortBy === 'price') {
      filteredProducts.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'rating') {
      filteredProducts.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === 'discount') {
      filteredProducts.sort((a, b) => (a.mrp - a.price) / a.mrp - (b.mrp - b.price) / b.mrp);
    }
  }
  filteredProducts.forEach(product => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productCard.innerHTML = `
      <img src="${product.img}" alt="${product.name}">
      <h2>${product.name}</h2>
      <p>Price: ₹${product.price}</p>
      <p>MRP: ₹${product.mrp}</p>
      <p>Rating: ${product.rating}/5</p>
      <p>Reviews: ${product.reviews}</p>
      <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
      <button class="wishlist" data-id="${product.id}"><i class="fa fa-heart"></i></button>
    `;
    productGrid.appendChild(productCard);
  });
}

// Function to add to cart
function addToCart(id) {
  const product = PRODUCTS.find(product => product.id === id);
  if (cart.includes(product)) {
    showToast('Product already in cart', 'error');
  } else {
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
    showToast('Product added to cart', 'success');
  }
}

// Function to toggle wishlist
function toggleWishlist(id) {
  const product = PRODUCTS.find(product => product.id === id);
  if (wishlist.includes(product)) {
    wishlist = wishlist.filter(item => item.id !== id);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showToast('Product removed from wishlist', 'error');
  } else {
    wishlist.push(product);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showToast('Product added to wishlist', 'success');
  }
}

// Function to open product modal
function openProduct(id) {
  const product = PRODUCTS.find(product => product.id === id);
  const productModal = document.getElementById('product-modal');
  productModal.innerHTML = `
    <h2>${product.name}</h2>
    <p>Price: ₹${product.price}</p>
    <p>MRP: ₹${product.mrp}</p>
    <p>Rating: ${product.rating}/5</p>
    <p>Reviews: ${product.reviews}</p>
    <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
    <button class="wishlist" data-id="${product.id}"><i class="fa fa-heart"></i></button>
  `;
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
  const cartList = document.getElementById('cart-list');
  cartList.innerHTML = '';
  cart.forEach(product => {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart-item');
    cartItem.innerHTML = `
      <img src="${product.img}" alt="${product.name}">
      <h2>${product.name}</h2>
      <p>Price: ₹${product.price}</p>
      <button class="remove-from-cart" data-id="${product.id}">Remove</button>
    `;
    cartList.appendChild(cartItem);
  });
  const cartTotal = document.getElementById('cart-total');
  cartTotal.innerHTML = `Total: ₹${cart.reduce((acc, product) => acc + product.price, 0)}`;
}

// Function to place order
function placeOrder() {
  if (cart.length === 0) {
    showToast('Cart is empty', 'error');
  } else {
    const paymentModal = document.getElementById('payment-modal');
    paymentModal.style.display = 'block';
  }
}

// Function to handle payment
function handlePayment(method) {
  const paymentModal = document.getElementById('payment-modal');
  paymentModal.style.display = 'none';
  const successModal = document.getElementById('success-modal');
  successModal.style.display = 'block';
  cart = [];
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartUI();
}

// Function to search products
function searchProducts(query) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';
  const filteredProducts = PRODUCTS.filter(product => product.name.toLowerCase().includes(query.toLowerCase()));
  filteredProducts.forEach(product => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productCard.innerHTML = `
      <img src="${product.img}" alt="${product.name}">
      <h2>${product.name}</h2>
      <p>Price: ₹${product.price}</p>
      <p>MRP: ₹${product.mrp}</p>
      <p>Rating: ${product.rating}/5</p>
      <p>Reviews: ${product.reviews}</p>
      <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
      <button class="wishlist" data-id="${product.id}"><i class="fa fa-heart"></i></button>
    `;
    productGrid.appendChild(productCard);
  });
}

// Function to filter by category
function filterByCategory(cat) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';
  const filteredProducts = PRODUCTS.filter(product => product.cat === cat);
  filteredProducts.forEach(product => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productCard.innerHTML = `
      <img src="${product.img}" alt="${product.name}">
      <h2>${product.name}</h2>
      <p>Price: ₹${product.price}</p>
      <p>MRP: ₹${product.mrp}</p>
      <p>Rating: ${product.rating}/5</p>
      <p>Reviews: ${product.reviews}</p>
      <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
      <button class="wishlist" data-id="${product.id}"><i class="fa fa-heart"></i></button>
    `;
    productGrid.appendChild(productCard);
  });
}

// Function to sort products
function sortProducts(by) {
  const productGrid = document.getElementById('product-grid');
  productGrid.innerHTML = '';
  let sortedProducts = PRODUCTS;
  if (by === 'price') {
    sortedProducts.sort((a, b) => a.price - b.price);
  } else if (by === 'rating') {
    sortedProducts.sort((a, b) => b.rating - a.rating);
  } else if (by === 'discount') {
    sortedProducts.sort((a, b) => (a.mrp - a.price) / a.mrp - (b.mrp - b.price) / b.mrp);
  }
  sortedProducts.forEach(product => {
    const productCard = document.createElement('div');
    productCard.classList.add('product-card');
    productCard.innerHTML = `
      <img src="${product.img}" alt="${product.name}">
      <h2>${product.name}</h2>
      <p>Price: ₹${product.price}</p>
      <p>MRP: ₹${product.mrp}</p>
      <p>Rating: ${product.rating}/5</p>
      <p>Reviews: ${product.reviews}</p>
      <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
      <button class="wishlist" data-id="${product.id}"><i class="fa fa-heart"></i></button>
    `;
    productGrid.appendChild(productCard);
  });
}

// Function to show toast notification
function showToast(msg, type) {
  const toast = document.getElementById('toast');
  toast.innerHTML = msg;
  toast.classList.add(type);
  setTimeout(() => {
    toast.classList.remove(type);
  }, 2000);
}

// Function to banner carousel
function bannerCarousel() {
  const banners = document.querySelectorAll('.banner');
  let currentBanner = 0;
  setInterval(() => {
    banners[currentBanner].style.display = 'none';
    currentBanner = (currentBanner + 1) % banners.length;
    banners[currentBanner].style.display = 'block';
  }, 3000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
  renderProducts();
  updateCartUI();
  bannerCarousel();
});

document.getElementById('product-grid').addEventListener('click', (e) => {
  if (e.target.classList.contains('add-to-cart')) {
    addToCart(parseInt(e.target.dataset.id));
  } else if (e.target.classList.contains('wishlist')) {
    toggleWishlist(parseInt(e.target.dataset.id));
  }
});

document.getElementById('cart-panel').addEventListener('click', (e) => {
  if (e.target.classList.contains('remove-from-cart')) {
    cart = cart.filter(product => product.id !== parseInt(e.target.dataset.id));
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
  }
});

document.getElementById('place-order').addEventListener('click', () => {
  placeOrder();
});

document.getElementById('payment-modal').addEventListener('click', (e) => {
  if (e.target.classList.contains('pay-now')) {
    handlePayment(e.target.dataset.method);
  }
});

document.getElementById('search-input').addEventListener('input', (e) => {
  searchProducts(e.target.value);
});

document.getElementById('filter-by-category').addEventListener('change', (e) => {
  filterByCategory(e.target.value);
});

document.getElementById('sort-by').addEventListener('change', (e) => {
  sortProducts(e.target.value);
});