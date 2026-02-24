import subprocess
import os
import sys

def deploy_to_vercel():
    try:
        # Check if vercel is installed
        result = subprocess.run(['vercel', '--version'], capture_output=True)
        if result.returncode != 0:
            print("Vercel CLI not found. Installing...")
            subprocess.run(['npm', 'install', '-g', 'vercel'], check=True)
        
        # Deploy to Vercel
        print("Deploying to Vercel...")
        subprocess.run(['vercel'], check=True)
        
        # Get deployment URL
        result = subprocess.run(['vercel', '--json'], capture_output=True, text=True)
        import json
        data = json.loads(result.stdout)
        url = data['url']
        print(f"Deployment successful! URL: {url}")
        
    except Exception as e:
        print(f"Error during deployment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    deploy_to_vercel()
