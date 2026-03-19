# Deployment Guide: recall-agency.com

Based on the auditing and plan details found in your local `00_System/` vault, your Hostinger plan supports Node.js applications (Next.js) natively with PM2 on your VPS/Managed Environment.

## Step 1: Uploading the Codebase
Because of standard macOS local environment restrictions (EPERM on iCloud mapped `node_modules`), it is best to build the application on the server.

1. SSH into the Hostinger server:
   ```bash
   ssh -p 65002 u965287345@92.113.28.34
   ```
2. Navigate to your root web directory (usually `/home/u965287345/domains/recall-agency.com/public_html` or a dedicated Node app folder).
3. Transfer the `/code` folder contents excluding `node_modules/`.
   *You can push the code to a private GitHub repo and pull it from the server, or use `rsync` / `scp`.*

## Step 2: Building on Hostinger
Once the code is on the server:
```bash
npm install
npm run build
```

## Step 3: Starting the Next.js Server
Since Hostinger supports Next.js, run it via PM2 to ensure it stays online continuously:
```bash
pm2 start npm --name "recall-agency" -- start
pm2 save
```

## Step 4: Cloudflare Routing
1. Login to Cloudflare.
2. Ensure the primary `A` record for `recall-agency.com` points to `92.113.28.34`.
3. Set the Proxy status to **Proxied (Orange Cloud)**.
4. Set SSL/TLS encryption mode to **Full (Strict)** since Hostinger provides a base SSL.
5. In the caching rules, set a rule to bypass cache for `/api/*` if you add backend API routes later.
