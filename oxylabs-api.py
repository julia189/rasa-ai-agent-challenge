from oxylabs import RealtimeClient

print("hello world")

# Set your Oxylabs API Credentials.
username = "username"
password = "password"

# Initialize the ProxyClient with your credentials.
proxy = oxylabs.ProxyClient(username, password)

# Customize headers for specific requirements (optional).
proxy.add_user_agent_header("desktop_chrome")
proxy.add_geo_location_header("Germany")
proxy.add_render_header("html")

# Use the proxy to make a request.
result = proxy.get("https://www.example.com")

print(result.text)