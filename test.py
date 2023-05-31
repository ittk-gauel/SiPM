from pathlib import Path

test_file = Path("/Users/itokawatakumi/Documents/SiPM_datas/RefCurve_2023-04-20_19_074530_57-5.bin")

c_suffix = test_file.with_suffix('.xml')
print(c_suffix)