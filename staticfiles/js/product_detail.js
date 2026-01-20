document.addEventListener("DOMContentLoaded", () => {
    console.log("PAIRO Product Detail – Loading your next favorite pair...");

    let selectedVariantId = null;

    // Extract product ID
    let productId = null;
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    if (pathParts.length >= 2) {
        let candidate = pathParts[pathParts.length - 1].replace(/\/$/, '');
        if (/^\d+$/.test(candidate)) {
            productId = parseInt(candidate, 10);
        }
    }

    if (!productId) {
        for (let i = pathParts.length - 1; i >= 0; i--) {
            if (/^\d+$/.test(pathParts[i])) {
                productId = parseInt(pathParts[i], 10);
                break;
            }
        }
    }

    if (!productId || isNaN(productId)) {
        console.error("Invalid product ID:", window.location.pathname);
        showToast("Invalid product page");
        document.getElementById("product-name").textContent = "Error";
        return;
    }

    console.log("Product ID:", productId);

    // Fetch product
    fetch(`/api/products/${productId}/`, {
        credentials: "same-origin"
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status} – ${response.statusText}`);
            }
            return response.json();
        })
        .then(product => {
            console.log("Product loaded:", product);

            // Image with lazy load + placeholder
            const mainImg = document.getElementById("main-product-img");
            mainImg.src = product.images?.length ? product.images[0].image : "https://via.placeholder.com/800x800?text=PAIRO";
            mainImg.classList.add("loaded");

            // Name & price with animation
            document.getElementById("product-name").textContent = product.name || "Premium Pair";
            document.getElementById("product-price").textContent = `₹${product.base_price || "—"}`;

            // Sizes – circular, premium look
            const sizeContainer = document.getElementById("size-options");
            sizeContainer.innerHTML = "";

            if (!product.variants?.length) {
                sizeContainer.innerHTML = '<p class="text-danger fs-5">No sizes available right now</p>';
                return;
            }

            product.variants.forEach(variant => {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "size-btn btn btn-outline-light rounded-circle d-flex align-items-center justify-content-center";
                btn.style.width = "60px";
                btn.style.height = "60px";
                btn.style.fontSize = "1.1rem";
                btn.textContent = variant.size || "—";
                btn.dataset.variantId = variant.id;

                btn.addEventListener("click", () => {
                    selectedVariantId = variant.id;
                    console.log("Selected variant:", selectedVariantId);

                    document.querySelectorAll(".size-btn").forEach(b => b.classList.remove("active"));
                    btn.classList.add("active");

                    document.getElementById("add-to-cart-btn").disabled = false;
                    showToast(`Size ${variant.size} selected`);
                });

                sizeContainer.appendChild(btn);
            });
        })
        .catch(error => {
            console.error("Failed to load product:", error);
            showToast(`Could not load product (${error.message})`);
            document.getElementById("product-name").textContent = "Error loading product";
        });

    // Add to Cart
    document.getElementById("add-to-cart-btn").addEventListener("click", () => {
        if (!selectedVariantId) {
            showToast("Please select a size first");
            return;
        }

        console.log("Adding to cart – variant:", selectedVariantId);

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

        fetch("/api/cart/add-session/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken || ""
            },
            body: `variant_id=${selectedVariantId}`
        })
            .then(res => {
                console.log("Add-to-cart status:", res.status);
                if (!res.ok) {
                    return res.json().then(err => { throw err; });
                }
                return res.json();
            })
            .then(data => {
                if (data.error) {
                    showToast(data.error);
                } else {
                    showToast("Added to cart 🛒");
                    // Optional: animate cart icon in navbar
                    const cartBadge = document.getElementById("cart-count-badge");
                    if (cartBadge) {
                        cartBadge.classList.remove("d-none");
                        cartBadge.textContent = (parseInt(cartBadge.textContent) || 0) + 1;
                    }
                }
            })
            .catch(err => {
                console.error("Add to cart failed:", err);
                showToast("Failed to add to cart – try again");
            });
    });
});