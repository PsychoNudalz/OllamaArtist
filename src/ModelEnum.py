from enum import Enum

class ModelNames(str, Enum):
    ChillOut = "chilloutmix_NiPrunedFp32Fix.safetensors"
    Aniverse = "aniverse_v30Pruned.safetensors"
    DreamShaper = "dreamshaper_8.safetensors"
    GhostMix = "ghostmix_v20Bakedvae.safetensors"
    # Add more as needed
