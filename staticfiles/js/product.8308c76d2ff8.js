const productId = window.location.pathname.split("/")[2];

fetch("/api/products/filter/")
  .then(res => res.json())
  .then(products => {
    const product = products.find(p => p.id == productId);
    const div = document.getElementById("product-detail");

    div.innerHTML = `<h3 class="mb-3">${product.name}</h3>`;

    product.variants.forEach(v => {
      div.innerHTML += `
        <div class="card mb-3 p-3">
          <p><strong>Size:</strong> ${v.size}</p>
          <p><strong>Color:</strong> ${v.color}</p>
          <p class="price">₹${v.price}</p>
          <button class="btn btn-dark" onclick="addToCart(${v.id})">
            Add to Cart
          </button>
        </div>
      `;
    });
  });

function addToCart(variantId) {
  fetch("/api/cart/add-session/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `variant_id=${variantId}`,
  })
  .then(res => res.json())
  .then(() => {
    showToast("Added to cart 🛒");
  });
}


