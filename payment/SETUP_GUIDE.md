# 🚀 Quick Setup Guide - Auto-Phil Shorts Payment Page

This guide will walk you through setting up your payment page step-by-step. **Total time: ~10 minutes**

---

## ✅ Step 1: Get Your Stripe Publishable Key (2 minutes)

1. Go to https://dashboard.stripe.com/apikeys
2. Log in to your Stripe account
3. You'll see two keys:
   - **Publishable key** (starts with `pk_test_` or `pk_live_`)
   - **Secret key** (starts with `sk_test_` or `sk_live_`)
4. **Copy the Publishable key** (the one that starts with `pk_`)
5. Keep this handy - you'll need it in Step 3

> 💡 **Tip:** Start with test mode (`pk_test_`) to test everything before going live

---

## ✅ Step 2: Get Your Stripe Price IDs (3 minutes)

1. Go to https://dashboard.stripe.com/products
2. You should see your 4 products:
   - 10 Pack - Optimized Shorts
   - 25 Pack - Optimized Shorts
   - 50 Pack - Optimized Shorts
   - 100 Pack - Optimized Shorts

3. **For each product:**
   - Click on the product name
   - Scroll down to the "Pricing" section
   - You'll see a Price ID that looks like: `price_1AbCdEfGhIjKlMnO`
   - Copy this ID

4. Write down all 4 Price IDs:
   ```
   10 Pack:  price_________________
   25 Pack:  price_________________
   50 Pack:  price_________________
   100 Pack: price_________________
   ```

---

## ✅ Step 3: Update Your Payment Page (2 minutes)

1. Open the file: `payment/script.js`

2. **Line 2:** Replace the Publishable Key:
   ```javascript
   // BEFORE:
   const STRIPE_PUBLISHABLE_KEY = 'pk_test_YOUR_PUBLISHABLE_KEY_HERE';
   
   // AFTER (use your actual key):
   const STRIPE_PUBLISHABLE_KEY = 'pk_test_51AbCdEfGhIjKlMnO...';
   ```

3. **Lines 5-10:** Replace the Price IDs:
   ```javascript
   // BEFORE:
   const PRICE_IDS = {
       'PRICE_ID_10_PACK': 'price_YOUR_10_PACK_PRICE_ID',
       'PRICE_ID_25_PACK': 'price_YOUR_25_PACK_PRICE_ID',
       'PRICE_ID_50_PACK': 'price_YOUR_50_PACK_PRICE_ID',
       'PRICE_ID_100_PACK': 'price_YOUR_100_PACK_PRICE_ID'
   };
   
   // AFTER (use your actual Price IDs):
   const PRICE_IDS = {
       'PRICE_ID_10_PACK': 'price_1AbCdEfGhIjKlMnO',
       'PRICE_ID_25_PACK': 'price_2PqRsTuVwXyZaBcD',
       'PRICE_ID_50_PACK': 'price_3EfGhIjKlMnOpQrS',
       'PRICE_ID_100_PACK': 'price_4TuVwXyZaBcDeFgH'
   };
   ```

4. **Save the file**

---

## ✅ Step 4: Test Locally (2 minutes)

1. Open `payment/index.html` in your web browser
   - Right-click the file → Open with → Chrome/Firefox/Edge

2. You should see:
   - ✓ Discount banner at the top
   - ✓ Countdown timer ticking
   - ✓ 4 pricing cards with 50% off prices
   - ✓ "Get 50% Off Now" buttons

3. **Test a purchase:**
   - Click any "Get 50% Off Now" button
   - You should be redirected to Stripe Checkout
   - Use test card: `4242 4242 4242 4242`
   - Expiry: `12/34` (any future date)
   - CVC: `123` (any 3 digits)
   - ZIP: `12345` (any 5 digits)
   - Complete the checkout

4. You should see the success page!

> ⚠️ **If buttons don't work:** Check browser console (F12) for errors. Make sure you copied the keys correctly.

---

## ✅ Step 5: Deploy to the Web (3 minutes)

### Option A: Netlify (Easiest - Recommended)

1. Go to https://app.netlify.com/drop
2. Drag and drop the entire `payment` folder
3. Wait 30 seconds for deployment
4. Your site is live! Copy the URL (e.g., `https://random-name-123.netlify.app`)
5. **Optional:** Click "Domain settings" to add a custom domain

### Option B: Vercel

1. Go to https://vercel.com/new
2. Sign up with GitHub/GitLab/Email
3. Click "Deploy" and upload the `payment` folder
4. Your site is live! Copy the URL

### Option C: GitHub Pages

1. Create a new GitHub repository
2. Upload all files from the `payment` folder
3. Go to Settings → Pages
4. Enable Pages from `main` branch
5. Your site is live at `https://yourusername.github.io/repo-name`

---

## ✅ Step 6: Switch to Live Mode (When Ready)

**Only do this when you're ready to accept real payments!**

1. In Stripe Dashboard, toggle from "Test mode" to "Live mode" (top right)
2. Go to https://dashboard.stripe.com/apikeys
3. Copy your **Live Publishable Key** (`pk_live_...`)
4. Update `script.js` with the live key
5. Re-deploy your site

---

## 🎉 You're Done!

Your payment page is now live and ready to accept payments!

### Next Steps:

1. **Share the link** with your leads from the YouTube scraper
2. **Monitor sales** in your Stripe Dashboard
3. **Check email** for payment notifications
4. **Track conversions** - see which package sells best

---

## 🆘 Troubleshooting

### "Stripe not initialized" error
- Double-check your publishable key in `script.js`
- Make sure it starts with `pk_test_` or `pk_live_`
- No extra spaces or quotes

### "Price ID not configured" error
- Verify all 4 Price IDs are correct in `script.js`
- Price IDs should start with `price_`
- Make sure you're using the right mode (test vs live)

### Buttons don't do anything
- Open browser console (F12) to see errors
- Check that you saved `script.js` after editing
- Try hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Checkout page shows wrong prices
- The prices shown in Stripe Checkout come from your Stripe Products
- To change them, edit the products in your Stripe Dashboard
- The prices on the landing page are just for display

---

## 📞 Need Help?

- **Stripe Documentation:** https://stripe.com/docs/checkout/quickstart
- **Stripe Support:** https://support.stripe.com/
- **Test Cards:** https://stripe.com/docs/testing

---

**Happy selling! 🚀**
