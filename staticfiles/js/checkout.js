function placeOrder() {
    console.log("Placing order...");
    showToast("Processing your order...");

    fetch("/api/orders/checkout-session/", {
        method: "POST",
        credentials: "same-origin"
    })
        .then((res) => {
            if (!res.ok) {
                throw new Error("Checkout request failed");
            }
            return res.json();
        })
        .then((data) => {
            console.log("Checkout success:", data);

            if (data.error) {
                showToast(data.error);
                return;
            }

            showToast("Order placed successfully 🎉");

            // Optional: download bill / invoice if exists
            if (data.order_id) {
                window.open(`/api/billing/download/${data.order_id}/`, "_blank");
            }

            // Redirect to home after short delay
            setTimeout(() => {
                window.location.href = "/";
            }, 1500);
        })
        .catch((err) => {
            console.error("Checkout failed:", err);
            showToast("Failed to place order – please try again");
        });
}
