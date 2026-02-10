# Auto-Phil Shorts Payment Page

Professional payment page with Stripe integration for your YouTube Shorts repurposing service.

## 🎯 Features

- ✅ 4 pricing tiers (10, 25, 50, 100 pack)
- ✅ 50% discount prominently displayed
- ✅ Countdown timer to February 28, 2026
- ✅ Stripe Checkout integration (secure, PCI-compliant)
- ✅ Mobile-responsive design
- ✅ Success and cancellation pages
- ✅ Professional UI with conversion optimization

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Your Stripe Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
2. Copy your **Publishable Key** (starts with `pk_test_` or `pk_live_`)
3. Open `script.js` and replace `pk_test_YOUR_PUBLISHABLE_KEY_HERE` with your actual key

### Step 2: Get Your Price IDs

1. Go to [Stripe Products](https://dashboard.stripe.com/products)
2. Click on each product (10 Pack, 25 Pack, etc.)
3. Copy the **Price ID** (starts with `price_`)
4. Open `script.js` and update the `PRICE_IDS` object:

```javascript
const PRICE_IDS = {
    'PRICE_ID_10_PACK': 'price_1AbCdEfGhIjKlMnO',  // Your actual Price ID
    'PRICE_ID_25_PACK': 'price_2PqRsTuVwXyZaBcD',
    'PRICE_ID_50_PACK': 'price_3EfGhIjKlMnOpQrS',
    'PRICE_ID_100_PACK': 'price_4TuVwXyZaBcDeFgH'
};
```

### Step 3: Test in Test Mode

1. Make sure you're using **test mode** keys (pk_test_...)
2. Open `index.html` in your browser
3. Click any "Get 50% Off Now" button
4. Use Stripe's test card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
   - ZIP: Any 5 digits
5. Complete the test checkout

### Step 4: Deploy (Choose One)

#### Option A: Netlify (Recommended - Free & Easy)

1. Go to [Netlify](https://www.netlify.com/)
2. Sign up for free account
3. Drag and drop the `payment` folder
4. Your site is live! (e.g., `your-site.netlify.app`)
5. Optional: Add custom domain in Netlify settings

#### Option B: Vercel (Also Free & Easy)

1. Go to [Vercel](https://vercel.com/)
2. Sign up for free account
3. Import the `payment` folder
4. Deploy with one click
5. Your site is live! (e.g., `your-site.vercel.app`)

#### Option C: GitHub Pages (Free)

1. Create a GitHub repository
2. Upload the `payment` folder contents
3. Go to Settings → Pages
4. Enable GitHub Pages
5. Your site is live at `username.github.io/repo-name`

## 📝 Configuration Options

### Auto-Apply 50% Discount Coupon

To automatically apply a discount coupon at checkout:

1. Create a coupon in [Stripe Dashboard → Coupons](https://dashboard.stripe.com/coupons)
2. Set it to 50% off
3. Copy the coupon code
4. In `script.js`, uncomment and update this section:

```javascript
discounts: [{
    coupon: 'FEBRUARY50'  // Your coupon code
}]
```

### Update Pricing

If you need to change the displayed prices:

1. Open `index.html`
2. Find the pricing cards
3. Update the `price-original` and `price-current` values
4. Update the `price-per-unit` calculation

### Customize Branding

**Colors:** Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #6772e5;  /* Change to your brand color */
    --primary-dark: #5469d4;
}
```

**Logo:** Replace the text logo in `index.html` with an image:
```html
<div class="logo">
    <img src="your-logo.png" alt="Auto-Phil Shorts">
</div>
```

**Contact Email:** Update email addresses in:
- `success.html` (support link)
- `cancel.html` (support link)

## 🔒 Security Best Practices

✅ **DO:**
- Use HTTPS (automatic with Netlify/Vercel)
- Keep your **Secret Key** private (never put in frontend code)
- Use test mode keys during development
- Switch to live mode keys only when ready for real payments

❌ **DON'T:**
- Never commit your secret key to Git
- Never use live mode keys in test environments
- Never handle credit card data directly (Stripe does this)

## 🧪 Testing Checklist

Before going live, test:

- [ ] All 4 pricing buttons redirect to Stripe Checkout
- [ ] Test payment completes successfully
- [ ] Success page displays after payment
- [ ] Cancel page shows when backing out
- [ ] Countdown timer shows correct time
- [ ] Page looks good on mobile (test on phone)
- [ ] All links work correctly
- [ ] Email addresses are correct

## 📊 Stripe Test Cards

Use these cards in test mode:

| Card Number | Result |
|-------------|--------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 9995 | Decline (insufficient funds) |
| 4000 0000 0000 0002 | Decline (card declined) |

## 🎨 File Structure

```
payment/
├── index.html          # Main pricing page
├── styles.css          # All styling
├── script.js           # Stripe integration + countdown
├── success.html        # Post-purchase page
├── cancel.html         # Checkout cancelled page
├── .env.example        # Configuration template
└── README.md           # This file
```

## 🔧 Troubleshooting

**"Stripe not initialized" error:**
- Check that you've added your publishable key to `script.js`
- Make sure the key starts with `pk_test_` or `pk_live_`

**"Price ID not configured" error:**
- Verify you've updated all 4 Price IDs in `script.js`
- Price IDs should start with `price_`
- Make sure there are no typos

**Checkout doesn't redirect:**
- Check browser console for errors (F12)
- Verify your Price IDs are correct
- Make sure you're using the right mode (test vs live)

**Success page doesn't show order details:**
- This is normal - full details are in the Stripe confirmation email
- You can enhance this by adding a backend to fetch session details

## 📈 Next Steps

After deployment:

1. **Add Analytics:** Insert Google Analytics or Plausible tracking code
2. **Email Collection:** Set up email capture on success page
3. **A/B Testing:** Test different headlines, pricing order, CTAs
4. **Monitor Conversions:** Track which package sells best
5. **Customer Support:** Set up email forwarding for support@

## 💡 Tips for Maximum Conversions

1. **Urgency:** The countdown timer creates urgency - keep it visible
2. **Social Proof:** Add testimonials or client logos if you have them
3. **Clear Value:** The per-video pricing helps justify bulk packages
4. **Trust Signals:** Stripe badge and SSL certificate build confidence
5. **Mobile First:** 60%+ of traffic is mobile - test thoroughly on phones

## 🆘 Support

Need help? Contact:
- Email: support@autophilshorts.com
- Stripe Support: https://support.stripe.com/

## 📄 License

This payment page is for Auto-Phil Shorts business use.

---

**Ready to launch?** Follow the Quick Setup steps above and you'll be accepting payments in minutes! 🚀
