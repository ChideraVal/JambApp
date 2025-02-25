// Make payment on flutterwave

let form = document.getElementById('emailform');
let email = document.getElementById('email');


function makePayment() {
    let emailValue = document.getElementById('email').value;
    FlutterwaveCheckout({
        public_key: "FLWPUBK-4665a5bfdd9fe8535fa8c74f0d845b09-X",
        tx_ref: `cs-${emailValue}`,
        amount: 1500,
        currency: "NGN",
        payment_options: "card, ussd, banktransfer, account, internetbanking, nqr, applepay, googlepay, enaira, opay",
        customer: {
            email: `${emailValue}`,
        },
        customizations: {
            title: "Mune",
            description: "Pay now to get the study questions of all 12 chapters sent to your inbox.",
        },
        callback: function (payment) {
            open(`https://jambapp-szn6.onrender.com/storecookie/${emailValue}/${payment.transaction_id}/`, '_parent')
        },
    });
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    makePayment();
})



