document.addEventListener("DOMContentLoaded", () => {
    console.log("PAIRO Home – Loading street-ready vibes...");
    loadProducts(); // must work
    // loadSubCategories(); // still commented – no 404
});

function loadProducts() {
    fetch("/api/products/", {
        credentials: "same-origin",
        headers: { "Accept": "application/json" }
    })
        .then(res => {
            if (!res.ok) {
                throw new Error(`Products API failed: ${res.status}`);
            }
            return res.json();
        })
        .then(products => {
            renderProducts(products);
        })
        .catch(err => {
            console.error("PRODUCT LOAD ERROR:", err);
            const loader = document.getElementById("loader");
            if (loader) {
                loader.innerHTML = `
                    <div class="text-center text-danger py-5">
                        <i class="fas fa-exclamation-triangle fa-3x mb-3"></i><br>
                        Failed to load products
                    </div>
                `;
            }
            showToast("Couldn't load products. Try refreshing.");
        });
}

function filterBySubCategory(slug) {
    fetch(`/api/products/?subcategory=${encodeURIComponent(slug)}`, {
        credentials: "same-origin"
    })
        .then(res => {
            if (!res.ok) return [];
            return res.json();
        })
        .then(products => {
            renderProducts(products);
            showToast(`Showing ${products.length} items in this category`);
        })
        .catch(() => {
            renderProducts([]);
            showToast("No items found in this category");
        });
}

function renderProducts(products) {
    const loader = document.getElementById("loader");
    const list = document.getElementById("product-list");

    if (!list || !loader) return;

    loader.classList.add("d-none");
    list.classList.remove("d-none");
    list.innerHTML = "";

    if (!products || products.length === 0) {
        list.innerHTML = `
            <div class="col-12 text-center py-5">
                <h5 class="text-muted">No products found</h5>
                <small>Try another category or check back later</small>
            </div>
        `;
        return;
    }

    products.forEach((p, index) => {
        const img = p.images && p.images.length
            ? p.images[0].image
            : "https://via.placeholder.com/400x400?text=PAIRO";

        const card = document.createElement("div");
        card.className = "col-md-4 col-lg-3 mb-4";
        card.innerHTML = `
  <div class="product-card h-100">
    <img src="${img}" alt="${p.name}">
    <div class="card-body">
      <h6>${p.name}</h6>
      <p class="price">₹${p.base_price}</p>
      <a href="/product/${p.id}/" class="btn btn-neon w-100">View</a>
    </div>
  </div>
`;
                <div class="card-body text-center p-4">
                    <h6 class="fw-bold mb-2">${p.name}</h6>
                    <p class="price fs-5 fw-bold gradient-text mb-3">₹${p.base_price}</p>
                    <a href="/product/${p.id}/" class="btn btn-outline-neon btn-sm w-100 rounded-pill">
                        View Details
                    </a>
                </div>
            </div>
        `;
        list.appendChild(card);
    });
}