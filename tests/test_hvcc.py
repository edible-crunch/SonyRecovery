from repair.hvcc import parse_hvcc

hvcc = parse_hvcc("hvcc.bin")

print()

print("Configuration Version :", hvcc.configuration_version)
print("Profile IDC           :", hvcc.profile_idc)
print("Tier                  :", hvcc.tier_flag)
print("Level                 :", hvcc.level_idc)
print("NAL Length Size       :", hvcc.nalu_length_size)

print()

for array in hvcc.arrays:

    print("Type", array["type"])

    for nal in array["nalus"]:

        print("  Length:", len(nal))