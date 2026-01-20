document.addEventListener("DOMContentLoaded", () => {
    console.log("PAIRO Cart – Checking your picks...");
    loadCart();
});

function loadCart() {
    fetch("/api/cart/session/")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("cart-items");
            const totalEl = document.getElementById("cart-total");

            list.innerHTML = "";
            let total = 0;

            if (!data.items || data.items.length === 0) {
                list.innerHTML = `
                    <li class="list-group-item bg-transparent text-center py-5">
                        <h5 class="text-light">Your cart is empty</h5>
                        <small class="text-muted">Start adding your favorite pairs</small>
                    </li>
                `;
                totalEl.innerText = "0";
                return;
            }

            data.items.forEach(item => {
                total += item.subtotal;

                list.innerHTML += `
                    <li class="list-group-item bg-transparent text-light border-bottom py-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong class="fs-5">${item.product}</strong><br>
                                <small class="text-muted">
                                  Size ${item.size} × ${item.quantity}
                                </small>
                            </div>

                            <div class="text-end">
                                <div class="fw-bold fs-5">₹${item.subtotal}</div>
                                <button
                                  class="btn btn-sm btn-danger mt-2"
                                  onclick="removeFromCart(${item.variant_id})">
                                  ❌ Remove
                                </button>
                            </div>
                        </div>
                    </li>
                `;
            });

            totalEl.innerText = total.toFixed(2);
        })
        .catch(err => {
            console.error(err);
            showToast("Failed to load cart 😢");
        });
}

function removeFromCart(variantId) {
    fetch(`/api/cart/remove-session/${variantId}/`)
        .then(res => res.json())
        .then(() => {
            showToast("Item removed 🗑️");
            loadCart(); // 🔥 refresh cart instantly
        });
}
