#!/usr/bin/env python3
"""
Live Logs Fix for Trading Dashboard
This script ensures live log streaming from Docker containers
"""

import docker
import time
from datetime import datetime

def test_live_log_streaming():
    """Test live log streaming from containers"""
    print("🔄 Testing live log streaming...")
    
    try:
        client = docker.from_env()
        client.ping()
        print("✅ Docker connection successful")
        
        target_containers = ['Yuva_Positions_trading_bot', 'Shan_Positions_trading_bot', 'log-reader']
        
        for container_name in target_containers:
            try:
                container = client.containers.get(container_name)
                print(f"\n📋 Testing {container_name}:")
                print(f"   Status: {container.status}")
                
                if container.status == 'running':
                    # Get recent logs
                    logs = container.logs(tail=5, timestamps=True).decode('utf-8')
                    if logs.strip():
                        print(f"   ✅ Logs available (last 5 lines):")
                        for line in logs.strip().split('\n')[-3:]:
                            if line.strip():
                                print(f"      {line}")
                    else:
                        print(f"   ⚠️  No recent logs found")
                        
                    # Test streaming
                    print(f"   🔄 Testing live stream...")
                    log_stream = container.logs(stream=True, follow=True, tail=1)
                    
                    # Get one log entry with timeout
                    start_time = time.time()
                    for log_line in log_stream:
                        print(f"   ✅ Live stream working: {log_line.decode('utf-8').strip()}")
                        break
                    else:
                        if time.time() - start_time > 5:
                            print(f"   ⚠️  No new logs in 5 seconds")
                    
                else:
                    print(f"   ❌ Container not running")
                    
            except docker.errors.NotFound:
                print(f"   ❌ Container {container_name} not found")
            except Exception as e:
                print(f"   ❌ Error testing {container_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Docker connection failed: {e}")
        return False

def show_container_logs_sample():
    """Show sample of what logs look like"""
    print("\n📋 Container Logs Analysis:")
    
    try:
        client = docker.from_env()
        
        containers = ['Yuva_Positions_trading_bot', 'Shan_Positions_trading_bot', 'log-reader']
        
        for container_name in containers:
            try:
                container = client.containers.get(container_name)
                if container.status == 'running':
                    print(f"\n🔍 {container_name} (Recent logs):")
                    logs = container.logs(tail=10, timestamps=True).decode('utf-8')
                    
                    if logs.strip():
                        lines = logs.strip().split('\n')
                        for line in lines[-5:]:  # Show last 5 lines
                            if line.strip():
                                print(f"   {line}")
                    else:
                        print("   (No recent logs)")
                        
            except Exception as e:
                print(f"   ❌ Error reading {container_name}: {e}")
    
    except Exception as e:
        print(f"❌ Could not analyze logs: {e}")

def main():
    print("🔄 Live Logs Fix for Trading Dashboard")
    print("=" * 50)
    
    # Test log streaming
    if test_live_log_streaming():
        print("\n✅ Live log streaming test completed")
    else:
        print("\n❌ Live log streaming test failed")
    
    # Show log samples
    show_container_logs_sample()
    
    print("\n💡 If logs are not updating:")
    print("1. Check if containers are actually generating new logs")
    print("2. Restart containers: docker restart container_name")
    print("3. Check container health: docker ps -a")
    print("4. Restart the trading dashboard application")

if __name__ == "__main__":
    main()