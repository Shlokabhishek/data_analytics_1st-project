# Deploying to Vercel

This project is configured for deployment on Vercel. Follow these steps:

## Prerequisites

1. A [Vercel account](https://vercel.com/signup) (free tier available)
2. [Vercel CLI](https://vercel.com/cli) installed (optional, for command-line deployment)

## Deployment Options

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub** (already done!)
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **Import to Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Project"
   - Select your GitHub repository: `Shlokabhishek/data_analytics_1st-project`
   - Click "Import"

3. **Configure (if needed):**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. **Deploy:**
   - Click "Deploy"
   - Wait 1-2 minutes for deployment to complete
   - Your app will be live at: `https://your-project-name.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```
   - Follow the prompts
   - Select your project settings
   - Deployment link will be provided

4. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

## Configuration Files

The following files have been added for Vercel deployment:

- **`vercel.json`**: Vercel configuration for Python/Flask app
- **`.vercelignore`**: Files to exclude from deployment
- **`requirements.txt`**: Python dependencies (automatically installed)

## Environment Variables

If you need to add environment variables:

1. Go to your project on Vercel Dashboard
2. Navigate to: Settings → Environment Variables
3. Add variables as needed

## Testing Your Deployment

Once deployed, test these endpoints:

- `/` - Main dashboard
- `/api/summary` - Summary statistics
- `/api/content-distribution` - Content distribution data
- `/api/lifecycle-trends` - Lifecycle trends
- `/api/saturation-analysis` - Saturation analysis
- `/api/investment-plan` - Investment plan
- `/api/insights` - Key insights

## Automatic Deployments

Vercel automatically deploys your app when you push to GitHub:

- **Production**: Pushes to `main` branch
- **Preview**: Pushes to other branches or pull requests

## Troubleshooting

### Cold Starts
Serverless functions on Vercel may have cold starts (1-3 second delay on first request after inactivity). This is normal for free tier.

### File Size Limits
- Maximum deployment size: 100 MB
- Serverless function size: 50 MB
- If you encounter size issues, consider hosting the Excel file separately

### Build Errors
- Check the deployment logs in Vercel Dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility (Vercel uses Python 3.9)

## Local Testing

To test locally before deploying:

```bash
python app.py
```

Visit: http://localhost:5000

## Custom Domain (Optional)

To add a custom domain:

1. Go to: Project Settings → Domains
2. Add your domain
3. Follow DNS configuration instructions

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Support](https://vercel.com/docs/runtimes#official-runtimes/python)
