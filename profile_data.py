from helper import load_data, generate_profile  

df = load_data()

if df is not None:
    profile_file = generate_profile(df)
    print(f"Profiling report saved as {profile_file}")
else:
    print("❌ Error: Could not load dataset.")