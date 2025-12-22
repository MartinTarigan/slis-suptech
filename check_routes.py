from slis import create_app
app = create_app()

print("\n=== DAFTAR URL AKTIF ===")
for rule in app.url_map.iter_rules():
    if "screening" in str(rule) or "jobs" in str(rule) or "bulk" in str(rule):
        print(f"{rule} -> {rule.endpoint}")
print("========================\n")