#!/usr/bin/env python3
"""
Docker Connection Fix for Ubuntu Server
This script fixes Docker connection issues on Ubuntu server deployment
"""

import os
import subprocess
import sys

def fix_docker_permissions():
    """Fix Docker socket permissions for the application"""
    print("🔧 Fixing Docker permissions...")
    
    try:
        # Check if docker.sock exists
        docker_sock = "/var/run/docker.sock"
        if not os.path.exists(docker_sock):
            print(f"❌ Docker socket not found at {docker_sock}")
            return False
        
        # Set proper permissions
        subprocess.run(["sudo", "chmod", "666", docker_sock], check=True)
        print("✅ Docker socket permissions fixed")
        
        # Add current user to docker group
        user = os.getenv("USER")
        if user:
            subprocess.run(["sudo", "usermod", "-aG", "docker", user], check=True)
            print(f"✅ User {user} added to docker group")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fixing Docker permissions: {e}")
        return False

def test_docker_connection():
    """Test Docker connection"""
    print("🧪 Testing Docker connection...")
    
    try:
        import docker
        
        # Try different connection methods
        methods = [
            ("Environment", lambda: docker.from_env()),
            ("Unix Socket", lambda: docker.DockerClient(base_url='unix://var/run/docker.sock')),
        ]
        
        for method_name, method_func in methods:
            try:
                client = method_func()
                client.ping()
                print(f"✅ Docker connection successful using {method_name}")
                
                # List containers
                containers = client.containers.list(all=True)
                print(f"📋 Found {len(containers)} containers:")
                
                target_containers = ['Yuva_Positions_trading_bot', 'Shan_Positions_trading_bot', 'log-reader']
                found_targets = []
                
                for container in containers:
                    if container.name in target_containers:
                        found_targets.append(container.name)
                        print(f"  ✅ {container.name}: {container.status}")
                    else:
                        print(f"  ℹ️  {container.name}: {container.status}")
                
                missing = set(target_containers) - set(found_targets)
                if missing:
                    print(f"⚠️  Missing target containers: {', '.join(missing)}")
                else:
                    print("✅ All target containers found!")
                
                return True
                
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
                continue
        
        print("❌ All Docker connection methods failed")
        return False
        
    except ImportError:
        print("❌ Docker Python library not installed")
        return False

def main():
    print("🚀 Docker Connection Fix for Trading Dashboard")
    print("=" * 50)
    
    # Fix permissions
    if not fix_docker_permissions():
        print("❌ Failed to fix Docker permissions")
        sys.exit(1)
    
    # Test connection
    if not test_docker_connection():
        print("❌ Docker connection test failed")
        print("\n📋 Troubleshooting steps:")
        print("1. Make sure Docker is running: sudo systemctl start docker")
        print("2. Add your user to docker group: sudo usermod -aG docker $USER")
        print("3. Log out and log back in")
        print("4. Restart the application")
        sys.exit(1)
    
    print("\n✅ Docker connection fix completed successfully!")
    print("🔄 Please restart the trading dashboard application")

if __name__ == "__main__":
    main()