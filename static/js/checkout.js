function placeOrder() {
    showToast("Processing your order...");

    fetch("/api/orders/checkout-session/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]')?.value || ""
        }
    })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => { throw err; });
            }
            return res.json();
        })
        .then(data => {
            if (data.error) {
                showToast(data.error);
                return;
            }

            showToast("Order placed successfully 🎉");
            window.open(`/api/billing/download/${data.order_id}/`, "_blank");
            setTimeout(() => window.location.href = "/", 1800);
        })
        .catch(err => {
            console.error("Checkout failed:", err);
            showToast("Failed to place order – please try again");
        });
}