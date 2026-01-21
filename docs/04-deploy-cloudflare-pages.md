# 04 — Deploy to Cloudflare Pages (Optional)

This repo includes a static viewer in `site/` that renders an audit record for human review.

## Cloudflare Pages

1. Create a new Pages project pointing at your GitHub repo.
2. Set:
   - **Build command:** (none)
   - **Output directory:** `site`
3. Deploy.

The viewer is fully static and runs in the browser. No backend required.

## Optional: host docs
If you want docs online, either:
- point Pages at a separate site build, or
- keep docs in-repo and rely on GitHub rendering.

This project intentionally avoids a heavy build toolchain.
