import torch


def remove_projection(hidden: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    unit = direction / direction.norm()
    return hidden - torch.einsum("...d,d->...", hidden, unit).unsqueeze(-1) * unit


def add_direction(hidden: torch.Tensor, direction: torch.Tensor, alpha: float = 1.0) -> torch.Tensor:
    unit = direction / direction.norm()
    return hidden + alpha * unit


def patch_component(hidden: torch.Tensor, component: torch.Tensor, alpha: float = 1.0) -> torch.Tensor:
    return hidden + alpha * component


def norm_matched_random(direction: torch.Tensor, seed: int = 17) -> torch.Tensor:
    generator = torch.Generator(device=direction.device).manual_seed(seed)
    random = torch.randn(direction.shape, generator=generator, device=direction.device, dtype=direction.dtype)
    return random / random.norm() * direction.norm()


def orthogonal_random(direction: torch.Tensor, seed: int = 17) -> torch.Tensor:
    random = norm_matched_random(direction, seed)
    unit = direction / direction.norm()
    orth = random - torch.dot(random, unit) * unit
    return orth / orth.norm() * direction.norm()
